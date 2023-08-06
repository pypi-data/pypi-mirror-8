"""repository abstraction for a mercurial repository

:organization: Logilab
:copyright: 2007-2013 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
:contact: http://www.logilab.fr/ -- mailto:contact@logilab.fr
"""

from __future__ import with_statement

__docformat__ = "restructuredtext en"

import urllib2
from os import umask, makedirs
from os.path import split, exists, dirname
from datetime import datetime
from contextlib import contextmanager
import time
import re

from mercurial import (hg, ui, context, util, encoding,
                       commands as hgcmd, phases, obsolete)
from mercurial.node import nullid, short as short_hex
from mercurial import scmutil
from mercurial.__version__ import version as hgversion

from logilab.common import tempattr

from cubicweb import Binary, QueryError, ValidationError, ExecutionError
from cubicweb.server.ssplanner import EditedEntity

from cubes.vcsfile import repo, bridge
from cubes.vcsfile.entities import remove_authinfo

hg31 = tuple(int(x) for x in re.split('[^0-9]+', hgversion)[:2]) >= (3, 1)

_DELETED = object()

def monkeypatch_mercurial_url():
    from mercurial.url import httphandler
    if hasattr(httphandler, '__del__'):
        del httphandler.__del__
monkeypatch_mercurial_url()

def spop(aset, item):
    try:
        aset.remove(item)
    except KeyError:
        pass

@contextmanager
def force_mercurial_utf8():
    old_encoding = encoding.encoding
    encoding.encoding = 'utf-8'
    yield
    encoding.encoding = old_encoding

# mercurial 2.4 at least does not contain any code to get
# the precursors ...
def iter_direct_known_precursors(ctx):
    obsstore = getattr(ctx._repo, 'obsstore', None)
    if obsstore is None:
        return
    nodemap = ctx._repo.changelog.nodemap
    markers = obsstore.precursors.get(ctx.node(), ())
    candidates = set(mark[0] for mark in markers)
    seen = set(candidates)
    # we traverse chains of markers which may refer to
    # nodes not known from the repo (because they were
    # not pushed/pulled)
    while candidates:
        current = candidates.pop()
        crev = nodemap.get(current)
        # is the marked revision known from the repo ?
        if crev is not None:
            yield ctx._repo[crev]
            continue
        # if not, let's continue until we reach a known precursor
        for mark in obsstore.precursors.get(current, ()):
            if mark[0] not in seen:
                candidates.add(mark[0])
                seen.add(mark[0])

# mercurial 2.4 at least does not contain any code to get
# the precursors ...
def iter_direct_known_successors(ctx):
    obsstore = getattr(ctx._repo, 'obsstore', None)
    if obsstore is None:
        return
    nodemap = ctx._repo.changelog.nodemap
    markers = obsstore.successors.get(ctx.node(), ())
    candidates = set()
    for mark in markers:
        candidates.update(set(mark[1]))
    seen = set(candidates)
    # we traverse chains of markers which may refer to
    # nodes not known from the repo (because they were
    # not pushed/pulled)
    while candidates:
        current = candidates.pop()
        crev = nodemap.get(current)
        # is the marked revision known from the repo ?
        if crev is not None:
            yield ctx._repo[crev]
            continue
        # if not, let's continue until we reach a known precursor
        for mark in obsstore.precursors.get(current, ()):
            for succ in mark[1]:
                if succ not in seen:
                    candidates.add(succ)
                    seen.add(succ)

class vcsfile_ui(ui.ui):
    """ redirect output to cubicweb log """
    def __init__(self, loggable):
        ui.ui.__init__(self)
        self.cw_loggable = loggable

    def copy(self):
        return self

    def interactive(self):
        return False

    # XXX beware encoding issues wrt localized outputs ...
    def write(self, *args, **kwargs):
        if self._buffers:
            self._buffers[-1].extend([str(a) for a in args])
        else:
            for a in args:
                self.cw_loggable.debug(str(a).strip())

    def write_err(self, *args, **kwargs):
        for a in args:
            self.cw_loggable.error(str(a).strip())


def bw_nb_revisions(changelog):
    """return the number of revisions in a repository's changelog,
    assuring mercurial < 1.1 compatibility
    """
    try:
        return len(changelog)
    except AttributeError: # hg < 1.1
        return changelog.count()


class HGRepository(repo.VCSRepository):
    type = 'hg'

    def pull_or_clone_cache(self, url, config):
        vui = vcsfile_ui(self)
        if not exists(self.path):
            pdir = dirname(self.path)
            if not exists(pdir):
                makedirs(pdir)
            self.info('cloning %s into %s', url, self.path)
            try:
                hgcmd.clone(vui, str(url),
                            dest=self.path, stream='compressed', noupdate=True)
            except (util.Abort, urllib2.URLError), ex:
                raise bridge.VCSException(self.eid, 'url', '%s (%s)', (ex, url))
        else:
            self.debug('pulling from %s into %s', remove_authinfo(url), self.path)
            try:
                hgcmd.pull(vui, hg.repository(vui, self.path), source=str(url))
            except (util.Abort, urllib2.URLError), ex:
                raise bridge.VCSException(self.eid, 'path', '%s (%s)', (ex, url,))
        if obsolete._enabled:
            # Wait 15s after a pull and re-pull the null revision, to make it
            # less likely we're missing in-flight obsolescence markers.
            # see #2818315
            if config.mode != 'test':
                time.sleep(15)
            try:
                hgcmd.pull(vui, hg.repository(vui, self.path), source=str(url), rev=('null',))
            except (util.Abort, urllib2.URLError), ex:
                raise bridge.VCSException(self.eid, 'path', '%s (%s)', (ex, url))

    def import_content(self, repoentity, commitevery=1000):
        """import content from the mercurial repository"""
        assert self.eid == repoentity.eid
        cnx = repoentity._cw
        if not exists(self.path):
            self.pull_or_clone_cache(repoentity.source_url,
                                     cnx.vreg.config)

        with force_mercurial_utf8():
            try:
                repo = self.hgrepo()
                # mercurial 2.5
                if hasattr(repo, 'unfiltered'):
                    repo = repo.unfiltered()
            except Exception, ex:
                self.exception('Impossible to open repository %s (%s)', self, ex)
                return

            rset = cnx.execute(
                    'Any CSET, REV WHERE R eid %(r)s, X from_repository R, '
                    'NOT CREV parent_revision X, X changeset CSET, X revision REV',
                    {'r': self.eid})
            knownheads = [(str(r[0]), r[1]) for r in rset]

            # detect stripped branches
            needsstrip = False
            needsrenumbering = False
            for cset, rev in knownheads:
                if cset not in repo:
                    needsstrip = True
                    self.warning('%s: strip detected. %s is unknown in local cache',
                                 self.path, cset)
            if not needsstrip:
                incoming = list(repo.revs("not ::%ls", [cset for cset, _rev in knownheads]))
                if incoming:
                    needsrenumbering = cnx.execute('Any R WHERE R is Revision, '
                                                   'R from_repository REPO, '
                                                   'REPO eid %%(reid)s, R revision IN (%s)'
                                                   % ','.join([str(rev) for rev in incoming]),
                                                   {'reid': repoentity.eid})
                if not needsrenumbering:
                    for cset, rev in knownheads:
                        if rev not in repo.revs("id(%s)" % str(cset)):
                            needsrenumbering = True
                            break

            if needsstrip or needsrenumbering:
                self.warning('%s: strip and renumbering from %s.',
                             repoentity.dc_title(), self.path)
                # clean all 'revision' attribute to please unicity
                # constraint when renumbering
                cnx.execute('SET R revision -1-REV WHERE R revision REV, R from_repository REPO, '
                            'REPO eid %(reid)s', {'reid': repoentity.eid})
                revs = cnx.execute('Any R WHERE R is Revision, R from_repository REPO, '
                                   'REPO eid %(reid)s', {'reid': repoentity.eid})
                for reventity in revs.entities():
                    if str(reventity.changeset) not in repo:
                        reventity.cw_delete()
                    else:
                        rev = repo[str(reventity.changeset)].rev()
                        reventity.cw_set(revision=rev)

                if cnx.execute('Revision R WHERE R revision < 0, R from_repository REPO, '
                               'REPO eid %(reid)s', {'reid': repoentity.eid}):
                    cnx.rollback()
                    self.error('Abort stripping and renumbering of Repository %s: '
                               'detected remaining Revision with negative revision number',
                               repoentity.eid)
                    return
                cnx.commit()
                cnx.execute(
                    'DELETE VersionedFile X WHERE X from_repository R, R eid %(r)s, '
                    'NOT VC content_for X', {'r': repoentity.eid})
                cnx.commit()

            # update phases and visibility of already known revisions
            self.update_phases(cnx, repoentity, repo)
            self.update_hidden(cnx, repoentity, repo)
            # XXX we need to update obsolescence markers without new revision
            #     involved.
            rset = cnx.execute(
                    'Any CSET WHERE R eid %(r)s, X from_repository R, '
                    'NOT CREV parent_revision X, X changeset CSET',
                    {'r': self.eid})
            knownheads = [str(r[0]) for r in rset]
            missing = list(repo.revs("not ::%ls", knownheads))
            missing.sort()
            while missing:
                for rev in missing[:commitevery]:
                    try:
                        self.import_revision(repoentity, repo, rev)
                    except Exception:
                        self.critical('error while importing revision %s of %s',
                                      rev, self.path, exc_info=True)
                        raise
                cnx.commit()
                del missing[:commitevery] # pop iterated value
            # if missing was empty we still need to commit phases and visibility changes
            cnx.commit()

    def update_phases(self, cnx, repoentity, repo):
        """ update all phases (this potentially affects all revs since
        phase changes are not transactional) """
        notpublic = set(str(ctx) for ctx in repo.set('not public()'))
        if notpublic:
            cnx.execute('SET R phase "public" WHERE NOT R changeset IN (%s),'
                        'NOT R phase "public", R from_repository REPO,'
                        'REPO eid %%(repo)s' %
                        ','.join(repr(rev) for rev in notpublic),
                        {'repo': repoentity.eid})
            for phase in ('draft', 'secret'):
                revs = set(str(ctx) for ctx in repo.set('%s()' % phase))
                if revs:
                    cnx.execute('SET R phase "%s" WHERE R changeset IN (%s),'
                                'NOT R phase "%s", R from_repository REPO,'
                                'REPO eid %%(repo)s' %
                                (phase, ','.join(repr(rev) for rev in revs), phase),
                                {'repo': repoentity.eid})
        else:
            cnx.execute('SET R phase "public" WHERE R from_repository REPO, '
                        'NOT R phase "public", REPO eid %(repo)s',
                        {'repo': repoentity.eid})



    def update_hidden(self, cnx, repoentity, repo):
        """ maintain hidden status for all revs """
        oldhidden = set(num for num, in cnx.execute('Any N WHERE R hidden True, '
                                                    'R from_repository H, '
                                                    'R revision N, H eid %(hg)s',
                                                    {'hg': repoentity.eid}).rows)
        newhidden = set(repo.revs('hidden()'))
        hide = newhidden - oldhidden
        show = oldhidden - newhidden
        for revs, setto in ((hide, 'True'), (show, 'False')):
            if revs:
                cnx.execute('SET R hidden %s WHERE R from_repository H,'
                                'H eid %%(hg)s, R revision IN (%s)' %
                                (setto, ','.join(str(revnum) for revnum in revs)),
                                {'hg': repoentity.eid})

        # very partial handling of obsolescence relation added after a revision
        # issue #2731056
        # this tries to find explanation for changeset that becomes hidden
        # - does not work for changesets already hidden
        # - does not work for public changesets
        for new_hide in hide:
            ctx = repo[new_hide]
            RQL = '''SET S obsoletes P
                     WHERE R eid %(r)s,
                           P from_repository R,
                           P changeset %(p)s,
                           S from_repository R,
                           S changeset %(s)s,
                           NOT S obsoletes P
            '''
            # unknown successors will create the relation at insertion time
            data = {'r': repoentity.eid,
                    'p': str(ctx)}
            for succ in iter_direct_known_successors(ctx):
                data['s'] = str(succ)
                cnx.execute(RQL, data)


    def import_revision(self, repoentity, repo, i):
        self.info('importing revision %s from %s', i, repoentity.dc_title())
        cnx = repoentity._cw
        execute = cnx.execute
        node = repo.changelog.node(i)
        changeset = unicode(short_hex(node))
        if execute('Any X WHERE X from_repository R, R eid %(repo)s, X changeset %(cs)s',
                   {'repo': repoentity.eid, 'cs': changeset}):
            self.warning('skip revision %s, seems already imported',
                         changeset)
            return
        ctx = repo.changectx(i)
        date = datetime.fromtimestamp(ctx.date()[0])
        #taglist = ctx.tags() #repo.nodetags(node)
        revdata = {'date': date, 'revision': i,
                   'author': unicode(ctx.user(), 'utf-8'),
                   'description': unicode(ctx.description(), 'utf-8'),
                   'changeset': changeset,
                   'phase': unicode(ctx.phasestr()),
                   'branch': unicode(ctx.branch()),
                   'hidden': ctx.hidden()
                   }
        parent_changesets = [short_hex(n)
                             for n in repo.changelog.parents(node)
                             if n != nullid]
        precursors_changesets = [str(p) for p in iter_direct_known_precursors(ctx)]
        if not precursors_changesets:
            precursors = ()
        else:
            precursors = execute(
                'Any X WHERE X revision XR, X changeset XC, '
                'X changeset IN (%s), X from_repository R, R eid %%(r)s'
                % ','.join("'%s'" % cs for cs in precursors_changesets),
                {'r': self.eid})
        revdata['precursors'] = [r[0] for r in precursors]
        if not parent_changesets:
            parents = ()
        elif len(parent_changesets) == 1:
            parents = execute(
                'Any X,XC,XR WHERE X revision XR, X changeset XC, '
                'X changeset %(cs)s, X from_repository R, R eid %(r)s',
                {'cs': parent_changesets[0], 'r': self.eid})
        else:
            parents = execute(
                'Any X,XC,XR WHERE X revision XR, X changeset XC, '
                'X changeset IN (%s), X from_repository R, R eid %%(r)s'
                % ','.join("'%s'"%cs for cs in parent_changesets),
                {'r': self.eid})
        revdata['parents'] = [r[0] for r in parents]
        reveid = bridge.import_revision(cnx, self.eid, **revdata)
        if not repoentity.import_revision_content:
            return
        changes = repo.status(ctx.parents()[0].node(), ctx.node())[:3]
        modified, added, removed = changes
        path_filter = repoentity.subpath
        for path in modified + added:
            upath = unicode(path, self.encoding, 'replace')
            if not (path_filter is None or upath.startswith(path_filter)):
                continue
            self._import_version_content(cnx, changeset, reveid, removed,
                                         path, upath, date, repo, ctx)
        for path in removed:
            upath = unicode(path, self.encoding, 'replace')
            if not (path_filter is None or upath.startswith(path_filter)):
                continue
            bridge.import_deleted_version_content(cnx, self.eid, reveid,
                                                  upath, date)
        parent_idx = dict( ((cs, lrev) for _, cs, lrev in parents) )
        parent_lrevs = [parent_idx[cs] for cs in parent_changesets]
        bridge.set_at_revision(cnx, reveid, parent_lrevs)

    def _import_version_content(self, cnx, changeset, reveid, removed, path, upath,
                                date, repo, ctx):
        directory, fname = split(path)
        cnx.transaction_data['vcs_importing'] = self.eid, directory, fname, changeset
        filectx = ctx[path]
        vcdata = {'data': Binary(filectx.data())}
        renameinfo = filectx.renamed()
        if renameinfo:
            pvc, oldfile = self._renamed_vc_rset(cnx, repo, renameinfo)
            if pvc:
                assert len(pvc) == 1
                if oldfile in removed:
                    vcdata['vc_rename'] = pvc[0][0]
                else:
                    vcdata['vc_copy'] = pvc[0][0]
            else:
                self.error('detected copy or rename of %s@%s but unable'
                           ' to find associated version content',
                           oldfile, pvc.args['cs'])
        return bridge.import_version_content(cnx, self.eid, reveid, upath,
                                             date, **vcdata)

    def _renamed_vc_rset(self, cnx, repo, renameinfo):
        oldfile, fileid = renameinfo
        pfctx = repo.filectx(oldfile, fileid=fileid)
        pcs = short_hex(pfctx.node())
        dir, name = split(unicode(oldfile, self.encoding, 'replace'))
        return cnx.execute('VersionContent X WHERE '
                           'X from_revision REV, REV changeset %(cs)s, '
                           'REV from_repository R, R eid %(r)s, '
                           'X content_for VF, VF directory %(dir)s, VF name %(name)s',
                           {'cs':  pcs, 'r': self.eid,
                            'dir': dir, 'name': name}), oldfile

    def hgrepo(self):
        repo = hg.repository(ui.ui(), self.path)
        return getattr(repo, 'unfiltered', lambda: repo)()

    def _file_content(self, path, rev):
        """extract a binary string with the content of the file at `path` for
        revision `rev` in the repository
        """
        ctx = self.hgrepo().changectx(rev)
        return Binary(ctx[path].data())

    def revision_transaction(self, cnx, entity):
        """open a transaction to create a new revision corresponding to the
        given entity
        """
        return HGTransaction(self, cnx, entity)

    def add_versioned_file_content(self, cnx, transaction, vf, entity,
                                   data):
        """add a new revision of a versioned file"""
        vfpath = self.encode(vf.path)
        if hg31:
            transaction.changes[vfpath] = context.memfilectx(
                transaction.repo, vfpath, data.getvalue(), islink=False, isexec=False, copied=None)
        else:
            transaction.changes[vfpath] = context.memfilectx(
                vfpath, data.getvalue(), islink=False, isexec=False, copied=None)
        return vf.path

    def add_versioned_file_deleted_content(self, cnx, transaction, vf,
                                           entity):
        """add a new revision of a just deleted versioned file"""
        transaction.changes[self.encode(vf.path)] = _DELETED
        return vf.path


class HGTransaction(object):
    def __init__(self, repohdlr, cnx, revision):
        self.repohdlr = repohdlr
        self.cnx = cnx
        self.revision = revision
        self.repo = repohdlr.hgrepo()
        # see http://mercurial.selenic.com/wiki/LockingDesign
        self._lock = self.repo.lock()
        self.extra = {}
        self.changes = {}

    @property
    def rev(self):
        """newly created revision number"""
        return bw_nb_revisions(self.repo.changelog)

    def _filectx(self, repo, memctx, path):
        """callable receiving the repository, the current memctx object and the
        normalized path of requested file, relative to repository root. It is
        fired by the commit function for every file in 'files', but calls order
        is undefined. If the file is available in the revision being committed
        (updated or added), filectxfn returns a memfilectx object. If the file
        was removed, filectxfn raises an IOError. Moved files are represented by
        marking the source file removed and the new file added with copy
        information (see memfilectx).
        """
        if self.changes[path] is _DELETED:
            raise IOError()
        return self.changes[path]

    def precommit(self):
        if not self.changes:
            raise QueryError('nothing changed')
        # XXX to what commit does here + strip in revert_precommit
        branch = self.repohdlr.encode(
            self.revision.cw_attr_cache.get('branch') or u'default')
        if branch != u'default':
            self.extra['branch'] = branch
        if getattr(self.repo, 'branchtags', None) is None:
            # hg 2.9, branchtags is gone
            try:
                self.hgparent = p1 = self.repo.branchmap().branchtip(branch)
            except KeyError:
                # new branch
                self.hgparent = p1 = self.repo.branchmap().branchtip('default')
        else:
            try:
                self.hgparent = p1 = self.repo.branchtags()[branch]
            except KeyError:
                # new branch
                self.hgparent = p1 = self.repo.branchtags().get('default')
        if p1:
            if not self.revision.parent_revision:
                raise ValidationError(self.revision.eid,
                                      {'parent_revision': 'missing expected parent'})
            if [short_hex(p1)] != [r.changeset for r in self.revision.parent_revision]:
                raise ValidationError(None, {None: ('concurrency error, please '
                                                    're-upload the revision')})

    def commit(self):
        # XXX: make umask configurable
        oldumask = umask(022)
        try:
            self._commit()
        finally:
            umask(oldumask)

    def _commit(self):
        # XXX merging branches
        repohdlr = self.repohdlr
        revision = self.revision
        author = repohdlr.encode(revision.cw_attr_cache.get('author', u''))
        msg = repohdlr.encode(revision.cw_attr_cache.get('description', u''))
        # ensure mercurial will use configured repo encoding, not locale's
        # encoding
        # XXX modifying module's global is not very nice but I've no other idea
        old_encoding = encoding.encoding
        try:
            encoding.encoding = repohdlr.encoding
            ctx = context.memctx(self.repo, (self.hgparent, None), msg,
                                 self.changes.keys(), self._filectx, author,
                                 extra=self.extra)
            node = self.repo.commitctx(ctx)
            # update revision's record to set correct changeset
            #
            # take care, self.repo != self.cnx.repo (mercurial repo
            # instance vs rql repository)
            source = self.cnx.repo.system_source
            # remove previous cached value to only save the changeset
            with tempattr(revision, 'cw_edited', EditedEntity(revision)) as rev:
                rev.cw_edited['changeset'] = unicode(short_hex(node))
                rev.cw_edited['phase'] = unicode(self.repo[node].phasestr())
                source.update_entity(self.cnx, rev)
            # we need to explicitly commit the connection to the database since
            # this method is actually called from a postcommit event, i.e. once
            # cnxset has already been commited
            self.cnx.cnxset.commit()
            # XXX restore entity's dict?
            self.rollback()
        finally:
            encoding.encoding = old_encoding

    def rollback(self):
        try:
            from mercurial.lock import release
            release(self._lock)
        except ImportError:
            try:
                # mercurial >= 1.3.1
                self._lock.release()
            except AttributeError:
                del self._lock


from logging import getLogger
from cubicweb import set_log_methods
set_log_methods(HGRepository, getLogger('cubicweb.sources.hg'))
