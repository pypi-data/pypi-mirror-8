import os.path as osp

from logilab.common.decorators import classproperty

from cubicweb.devtools.testlib import CubicWebTC

from cubes.vcsfile import bridge

def init_vcsrepo(repo, commitevery=1):
    bridge._REPOHDLRS.clear()
    with repo.internal_cnx() as cnx:
        bridge.import_content(cnx, commitevery=commitevery,
                              raise_on_error=True)

class VCSRepositoryTC(CubicWebTC):
    """base class for test which should import a repository during setup"""
    _repo_path = None
    repo_type = u'mercurial'
    repo_encoding = u'utf-8'
    repo_subpath = None
    repo_import_revision_content = True
    repo_title = None

    commitevery = 3

    @classproperty
    def test_db_id(cls):
        if cls._repo_path is None:
            return None
        ids = [cls._repo_path]
        if cls.repo_subpath:
            ids.append(cls.repo_subpath)
        if not cls.repo_import_revision_content:
            ids.append('nocontent')
        return '-'.join(ids)

    @classproperty
    def repo_path(cls):
        assert cls._repo_path, 'you must set repository through _repo_path first'
        return osp.join(cls.datadir, cls._repo_path)

    @classmethod
    def _create_repo(cls, cnx):
        return cnx.create_entity(
            'Repository', type=cls.repo_type, path=cls.repo_path,
            subpath=cls.repo_subpath, encoding=cls.repo_encoding,
            title=cls.repo_title,
            import_revision_content=cls.repo_import_revision_content)

    @classmethod
    def grant_write_perm(cls, session, group, vcsrepoeid=None):
        if vcsrepoeid is None:
            vcsrepoeid = cls.vcsrepoeid
        cls.grant_permission(session, vcsrepoeid, 'managers', 'write',
                             u'repo x write perm')

    @classmethod
    def pre_setup_database(cls, cnx, config):
        bridge._REPOHDLRS.clear()
        # don't use cls.vcsrepo in regular test, only in pre_setup_database
        cls.vcsrepoeid = cls._create_repo(cnx).eid
        cnx.commit()
        init_vcsrepo(cnx.repo, cls.commitevery)

    def setUp(self):
        bridge._REPOHDLRS.clear()
        super(VCSRepositoryTC, self).setUp()
        with self.admin_access.repo_cnx() as cnx:
            self.vcsrepoeid = cnx.execute('Repository X')[0][0]
