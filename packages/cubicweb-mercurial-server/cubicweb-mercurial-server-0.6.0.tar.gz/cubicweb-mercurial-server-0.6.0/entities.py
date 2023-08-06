"""cubicweb-mercurial-server entity's classes"""

import sys, os, os.path as osp, shutil, tempfile, time, re
from contextlib import contextmanager
from urllib import quote_plus
from urlparse import urlparse

import hglib

from logilab.common.shellutils import tempdir
from logilab.common.decorators import monkeypatch, cachedproperty

from cubicweb.entities import AnyEntity, authobjs
from cubicweb import ValidationError

from cubes.vcsfile.hooks import clone_to_local_cache
from cubes.vcsfile.entities import Repository


class CWUser(authobjs.CWUser):

    def format_name_for_mercurial(self):
        if self.firstname and self.surname:
            result = u'{firstname} {surname}'.format(
                     firstname=self.firstname,
                     surname=self.surname)
        else:
            result = u'CWuser "{login}"'.format(login=self.login)
        if self.primary_email:
            result += u' <{email}>'.format(email=self.primary_email[0].address)
        return result.encode('utf-8')


@contextmanager
def fs_lock(req, lockpath):
    max_tries = req.vreg.config['hg-server-max-tries']
    seconds_wait = req.vreg.config['hg-server-lock-wait-seconds']
    seconds_kill = req.vreg.config['hg-server-lock-kill-seconds']
    for i in xrange(max_tries + 1):
        if osp.exists(lockpath):
            if os.stat(lockpath).st_mtime + seconds_kill < time.time():
                req.warning('forced removal of mercurial-server lock %s',
                            lockpath)
                os.unlink(lockpath)
            else:
                time.sleep(seconds_wait)
                continue
        # note that we may never reach this point
        yield open(lockpath, 'w').close()
        break
    else: # we tried hard, but nope
        error = req._('Could not acquire lock after %(no_tries)s tries '
                      '(%(seconds)s seconds wait)' % {'no_tries': max_tries,
                                                      'seconds': seconds_wait})
        raise IOError(error)
    try: # unconditional clean-up
        os.unlink(lockpath)
    except:
        pass


class HGSRepository(Repository):

    @property
    def fs_repo_lock_path(self):
        return osp.join(self._cw.vreg.config.appdatahome,
                        'repo_cache', 'mercurial_server_lock-%d' % self.eid)

    @contextmanager
    def pull_push(self, message, **commitopts):
        """ Allows edition of a repository between a pull/push
        Use at your own risks.
        """
        if not osp.exists(self.localcachepath):
            clone_to_local_cache(self)
        commitopts.update(message=message)
        with fs_lock(self._cw, self.fs_repo_lock_path):
            repo = hglib.open(str(self.localcachepath))
            repo.pull(source=self.source_url.encode('ascii'))
            repo.update()
            yield repo
            try:
                repo.commit(**commitopts)
            except hglib.error.CommandError as exc:
                if exc.ret == 1 and exc.out.strip() == 'nothing changed':
                    # do not fail if nothing had to be commited
                    return
                raise
            else:
                repo.push(dest=self.source_url.encode('ascii'))

    @property
    def push_url(self):
        if self.source_url.startswith(self.hosted_by[0].base_url + '/'):
            return self.source_url
        # XXX this assumes that the root of the (probably) http source_url is
        # the same as the mercurial-server base_url
        path = urlparse(self.source_url).path
        return self.hosted_by[0].base_url + path


class MercurialServerConfig(AnyEntity):
    __regid__ = 'MercurialServerConfig'

    def dc_long_title(self):
        return u'%s (%s)' % (self.name, self.base_url)

    @property
    def hgadmin_repo(self):
        return self.hgadmin_repository[0]

    @cachedproperty
    def conf_filename_str(self):
        return self.conf_filename.encode(sys.getfilesystemencoding())

    def access_conf_path(self, repo):
        return osp.join(repo.root_str, self.conf_filename)

    @cachedproperty
    def hgadmin_repopath(self):
        return str(self.hgadmin_repository[0].localcachepath)

    @contextmanager
    def exec_in_hgadmin_clone(self, message, **commitopts):
        with self.hgadmin_repo.pull_push(message, **commitopts) as repo:
            yield repo

    def write_access_conf(self, repo, access_line):
        access_conf_path = self.access_conf_path(repo)
        with open(access_conf_path, 'a') as access_file:
            access_file.write(access_line)
        repo.add(access_conf_path)

    def generate_access_conf(self):
        """ Generate the contents of the access.conf file """
        access_conf = []
        for repo in self.reverse_hosted_by:
            assert repo.push_url.startswith(self.base_url + '/')
            repo_path = repo.push_url[len(self.base_url) + 1:]
            for perm in repo.reverse_granted_on:
                key_path = perm.access_key[0].pathtuple
                conf_line = '{level} user={key} repo={repo}'.format(
                            level=perm.permission_level,
                            key=osp.join(self.keys_subdir, *key_path),
                            repo=repo_path)
                access_conf.append(conf_line)
        return '\n'.join(access_conf) + '\n'


class MercurialServerPermission(AnyEntity):
    __regid__ = 'MercurialServerPermission'

    def dc_title(self):
        """Concatenate permission name with user dc_title."""
        try:
            user = self.access_key[0].reverse_public_key[0]
        except IndexError:
            return self._cw._(self.permission_level)
        else:
            return self._cw._('%s for %s') % (self.permission_level, user.dc_title())

    @property
    def pubkey(self):
        return self.access_key[0].data

    @property
    def server_config(self):
        return self.granted_on[0].hosted_by[0]


class SshPubKey(AnyEntity):
    __regid__ = 'SshPubKey'

    def dc_title(self):
        return (self.name or
                self._cw._('%s public key') % self.reverse_public_key[0].dc_title())

    @property
    def mercurial_server_configs(self):
        perms = self.reverse_access_key
        return [perm.server_config for perm in perms]

    @property
    def pathtuple(self):
        """ Implements naming convention <login>/<keyeid>"""
        return  (self.reverse_public_key[0].login.encode('ascii'), str(self.eid))
