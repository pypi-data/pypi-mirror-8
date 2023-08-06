# -*- coding: utf-8 -*-
# copyright 2011 Florent Cayré (FRANCE), all rights reserved.
# contact florent.cayre@gmail.com
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.
"""cubicweb-mercurial-server specific hooks and operations"""

import sys
import os
import os.path as osp
import shutil
from collections import defaultdict

import hglib

from cubicweb import ValidationError
from cubicweb.predicates import is_instance, match_user_groups
from cubicweb.server import Service
from cubicweb.server.hook import Hook, Operation, DataOperationMixIn, match_rtype

# MercurialServerConfig

class MSCCreateHook(Hook):
    """ MSC creation -> automatically create its hgadmin Repository
    Deletion: the mercurial-server data will be out-of sync until
    a new MSC is created again, which will reset its keys & configs.
    """
    __regid__ = 'mercurialserver.config'
    __select__ = Hook.__select__ & is_instance('MercurialServerConfig')
    events = ('before_add_entity',)

    def __call__(self):
        edit = self.entity.cw_edited
        base_url = edit.get('base_url')
        hgadmin_path = edit.get('hgadmin_path')
        if not base_url or not hgadmin_path:
            return # standard validation will catch this, let's bail out
        base_url = edit['base_url'] = base_url.rstrip('/')
        url = '/'.join((base_url, hgadmin_path))
        repo = self._cw.create_entity('Repository',
                                      title=u'%s_repository_for_%s' % (hgadmin_path,
                                                                       self.entity.eid),
                                      type=u'mercurial',
                                      source_url=unicode(url),
                                      has_anonymous_access=False)
        edit['hgadmin_repository'] = repo.eid


class MSCUpdateHook(Hook):
    """strip trailing /s from base_url, if modified"""
    __regid__ = 'mercurialserver.config.update'
    __select__ = Hook.__select__ & is_instance('MercurialServerConfig')
    events = ('before_update_entity',)

    def __call__(self):
        edit = self.entity.cw_edited
        if 'base_url' not in edit:
            return
        edit['base_url'] = edit['base_url'].rstrip('/')


class MercurialServerRepositoryCreation(Hook):
    """ When a Repository is linked to a MercurialServerConfig
    through hosted_by, we try to initialize its remote location
    Failing to do so because the remote repo already exists is not
    a failure.
    """
    __regid__ = 'mercurialserver.initrepo'
    __select__ = Hook.__select__ & match_rtype('hosted_by')
    events = ('after_add_relation', )
    category = 'mercurialserver.fs'

    def __call__(self):
        # we need to refresh user's relations cache and cw_clear_cache is not
        # thread safe while _cw.user is a shared object. Prefer this method.
        user = self._cw.entity_from_eid(self._cw.user.eid)
        repo = self._cw.entity_from_eid(self.eidfrom)
        if not user.public_key:
            msg = (self._cw._('To create a hosted repository, %s must have a public key')
                   % user.login)
            raise ValidationError(self.eidfrom, {'hosted_by': msg})
        try:
            uri = repo.push_url.encode('ascii')
        except UnicodeEncodeError:
            msg = self._cw._('source_url must be ASCII encodable')
            raise ValidationError(self.eidfrom, {'source_url': msg})

        try:
            hglib.init(uri, ssh=self._cw.vreg.config['hg-ssh'] or None)
            self.warning('init-ed repository %s', uri)
            # prepare possible rollback (destroy remote repository)
            MSRepoRollbackOnInit.get_instance(self._cw).add_data(uri)
        except hglib.error.CommandError as exc:
            if re.match(r'^mercurial-server: .+ exists$', exc.err.splitlines()[0]):
                self.warning('repo %s seems to be already there: cannot init', uri)
            else:
                raise ValidationError(self.eidfrom, {'source_url': exc.err})
        # let's create a hg server permission right away
        self._cw.create_entity('MercurialServerPermission',
                               access_key=user.public_key,
                               granted_on=self.eidfrom,
                               permission_level=u'write')


class MSRepoRollbackOnInit(DataOperationMixIn, Operation):
    """ If a repo is init-ed per the hook above we may want
    to wipe it on transaction rollback.
    Alas, there is no method to do this currently except asking
    help to people of the managers group.

    Sending them some mail would be nice.
    """

    def rollback_event(self):
        for uri in self.get_data():
            self.critical('Admin: this repository should be wiped %s', uri)


class MSCDeletion(Hook):
    """ On config deletion, we wipe the parts that are under its control
    in the hgadmin repository. We commit and push immediately, before
    we lose track of the hgadmin_repository relation.
    """
    __regid__ = 'mercurialserver.msc_deletion'
    __select__ = Hook.__select__ & is_instance('MercurialServerConfig')
    events = ('before_delete_entity',)
    category = 'mercurialserver.fs'

    def __call__(self):
        msc = self.entity
        hgrepo = hglib.open(msc.hgadmin_repopath)
        try:
            with open(osp.join(hgrepo.root(), msc.conf_filename), 'wb') as conf_file:
                conf_file.write('\n')
        except OSError, err:
            self.error('critical filesystem operation failure')
            msg = _('could not alter the hgadmin repository content (%s)' % err)
            raise ValidationError(msc.eid, {'hgadmin_repository': msg})
        try:
            hgrepo.remove(osp.join(hgrepo.root(), 'keys', msc.keys_subdir))
            msctitle = msc.dc_title().encode('utf-8')
            message = ('server config `%s` (eid %s) deletion' % (msctitle, msc.eid))
            hgrepo.commit(message=message)
            cset = hgrepo.parents()[0][1]
            hgrepo.push(dest=msc.hgadmin_repo.source_url, rev=cset)
            rbdata = (msc.eid, msc.hgadmin_repo.source_url, msctitle,
                      hgrepo.root(), cset)
            MSCRollbackOnDelete.get_instance(self._cw).add_data(rbdata)
        except Exception, exc:
            self.error('error while handling the hgadmin repository')
            raise ValidationError(msc.eid, {'hgadmin_repo': _('error: %s') % exc})


class MSCRollbackOnDelete(DataOperationMixIn, Operation):
    """ When an msc deletion fail, we must undo the changes made to
    the hgadmin repository.
    """

    def rollback_event(self):
        for msceid, pushurl, msctitle, reporoot, cset in self.get_data():
            hgrepo = hglib.open(reporoot)
            hgrepo.backout(rev=cset,
                           message='backout `%s` (eid %s) deletion' % (msctitle, msceid))
            cset = hgrepo.parents()[0][1]
            hgrepo.push(dest=pushurl, rev=cset)


# SshPubKey

def schedule_key_sync(cnx, event, keyeid):
    key = cnx.entity_from_eid(keyeid)
    if not key.reverse_public_key and event == 'delete':
        # user has been deleted
        return
    for conf in key.mercurial_server_configs:
        SynchronizeAccesKeysOperation.get_instance(cnx).add_data(
            (event, conf.eid, osp.join('keys', conf.keys_subdir, *key.pathtuple),
             key.data.getvalue()))

class CWUSerDeletion(Hook):
    __regid__ = 'mercurialserver.cwuser_deletion'
    __select__ = Hook.__select__ & is_instance('CWUser')
    events = ('before_delete_entity',)

    def __call__(self):
        # we can't destroy remote repositories but we'll wipe the keys at least
        for key in self.entity.public_key:
            CWUserDeleteOp.get_instance(self._cw)

class CWUserDeleteOp(DataOperationMixIn, Operation):

    def postcommit_event(self):
        regenerator = self.cnx.vreg['services'].select('regenerate_hgadmin_repo', self.cnx)
        with self.cnx.repo.internal_cnx() as cnx:
            for msceid, in cnx.execute('MercurialServerConfig M').rows:
                regenerator.call(msceid)
            cnx.commit()

class SshPubKeyUpdate(Hook):
    __regid__ = 'mercurialserver.accesskeyupdatehook'
    __select__ = Hook.__select__ & is_instance('SshPubKey')
    events = ('after_update_entity',  # all relations are set
              'before_delete_entity') # all relations are _still_ set

    def __call__(self):
        event = 'add' if 'delete' not in self.event else 'delete'
        schedule_key_sync(self._cw, event, self.entity.eid)


class SshPubKeyLinkUnlink(Hook):
    """ Schedule an update operation for the access key on update.
    All MercurialServerConfigurations using this key must be updated.
    """
    __regid__ = 'mercurialserver.accesskeylinkunlink'
    __select__ = Hook.__select__ & match_rtype('public_key', 'access_key')
    events = ('after_add_relation',)     # key just got created
              # 'before_delete_relation') # key just got deleted

    def __call__(self):
        permeid = self.eidto
        event = 'add' if 'add' in self.event else 'delete'
        if event == 'add':
            # wait till everything is in place
            NewAccessKey.get_instance(self._cw).add_data((event, permeid))
        else:
            # do it asap
            schedule_key_sync(self._cw, event, permeid)


class NewAccessKey(DataOperationMixIn, Operation):

    def precommit_event(self):
        for event, keyeid in self.get_data():
            schedule_key_sync(self.cnx, event, keyeid)


# Permission

class MercurialServerPermission(Hook):
    """Schedule a re-generation operation for the access conf
    The permission level (read, write, ...) has been changed.
    """
    __regid__ = 'mercurialserver.permissionupdatehook'
    __select__ = Hook.__select__ & is_instance('MercurialServerPermission')
    events = ('after_update_entity', 'before_delete_entity')

    def __call__(self):
        if 'delete' in self.event:
            if (not self.entity.granted_on
                or self._cw.deleted_in_transaction(self.entity.granted_on[0].eid)):
                # we are being wiped
                return
        RegenerateAccesConfOperation.get_instance(self._cw).add_data(self.entity.server_config.eid)


# Operations

def remove_key(cnx, repo, keypath):
    filename = osp.join(repo.root(), keypath)
    cnx.warning('remove public key %s', filename)
    repo.remove(filename)

def add_key(cnx, repo, keypath, pubkey):
    filename = osp.join(repo.root(), keypath)
    dirpath = osp.dirname(filename)
    if not osp.isdir(dirpath):
        os.makedirs(dirpath)
    with open(filename, 'wb') as keyfile:
        keyfile.write(pubkey)
        cnx.warning('add public key %s', filename)
        repo.add(str(filename))


def sync_access_keys(cnx, server_config, op_path_pubkey):
    msg = ('Access keys sync from cube mercurial-server for %s' %
           ', '.join([x[1] for x in op_path_pubkey]))
    userdesc = cnx.user.format_name_for_mercurial()
    with server_config.exec_in_hgadmin_clone(msg, user=userdesc) as repo:
        for op, path, pubkey in op_path_pubkey:
            if op == 'add':
                add_key(cnx, repo, path, pubkey)
            else:
                remove_key(cnx, repo, path)


class SynchronizeAccesKeysOperation(DataOperationMixIn, Operation):
    """ Regenerate the mercurial-server `keys` directory

    add_data takes a tuple of (msc.eid, keypath, pubkey)

    key_path is a tuple representing the path associated to the key
    within the `keys` directory of the `hgadmin` repository.
    """

    def precommit_event(self):
        # Group the operations by MercurialServerConfig
        by_config = defaultdict(list)
        for operation, config_eid, path, pubkey in self.get_data():
            by_config[config_eid].append((operation, path, pubkey))

        for configeid, op_path_pubkey in by_config.iteritems():
            RegenerateAccesConfOperation.get_instance(self.cnx).add_data(config_eid)
            server_config = self.cnx.entity_from_eid(configeid)
            sync_access_keys(self.cnx, server_config, op_path_pubkey)

def write_access_conf(cnx, msc):
    msg = ('Regenerate access configuration %s from cube mercurial-server' %
           msc.dc_title())
    with msc.exec_in_hgadmin_clone(msg) as repo:
        access_conf_contents = msc.generate_access_conf()
        filename = osp.join(repo.root(), msc.conf_filename_str)
        already_exists = osp.exists(filename)
        with open(filename, 'w') as fobj:
            fobj.write(access_conf_contents)
        if not already_exists:
            cnx.warning('write %s', filename)
            repo.add(filename)

class RegenerateAccesConfOperation(DataOperationMixIn, Operation):
    """ Regenerate the mercurial-server <access.conf> file"""

    def precommit_event(self):
        for configeid in self.get_data():
            if self.cnx.deleted_in_transaction(configeid):
                continue
            server_config = self.cnx.entity_from_eid(configeid)
            write_access_conf(self.cnx, server_config)



# Misc.

class CheckAsciiLoginFromRtype(Hook):
    __regid__ = 'mercurial_server.check_ascii_login_from_rtype'
    __select__ = Hook.__select__ & match_rtype('public_key')
    events = ('after_add_relation',)

    def __call__(self):
        validate_ascii_login(self._cw, self.eidto, self.eidfrom)


def validate_ascii_login(cnx, msaeid, usereid):
    login = cnx.execute('Any L WHERE U login L, U eid %(u)s',
                        {'u': usereid}).rows[0][0]
    try:
        login.encode('ascii')
    except UnicodeEncodeError:
        msg = _('The user login must be ascii encodable (%s is not).') % login
        raise ValidationError(msaeid, {'public_key': msg})


class RegenerateMSCRepoService(Service):
    __regid__ = 'regenerate_hgadmin_repo'
    __select__ = Service.__select__ & match_user_groups('managers')

    def call(self, eid):
        msc = self._cw.entity_from_eid(eid)
        # first, clean
        msg = "Regenerate cfg and keys"
        userdesc = self._cw.user.format_name_for_mercurial()
        with msc.exec_in_hgadmin_clone(msg, user=userdesc) as hgrepo:
            hgrepo.remove(osp.join(hgrepo.root(), 'keys', msc.keys_subdir))
            RegenerateAccesConfOperation.get_instance(self._cw).add_data(eid)
            rset = self._cw.execute('Any K WHERE K is SshPubKey, P access_key K, '
                                    'P granted_on R, R hosted_by M, M eid %(eid)s',
                                    {'eid':eid})
            for key in rset.entities():
                filename = osp.join(hgrepo.root(), 'keys', msc.keys_subdir, *key.pathtuple)
                dirpath = osp.dirname(filename)
                if not osp.isdir(dirpath):
                    os.makedirs(dirpath)
                with open(filename, 'wb') as keyfile:
                    keyfile.write(key.data.getvalue())
                hgrepo.add(str(filename))
        # ... just in case, we don't really know who is responsible for this
        self._cw.commit()
