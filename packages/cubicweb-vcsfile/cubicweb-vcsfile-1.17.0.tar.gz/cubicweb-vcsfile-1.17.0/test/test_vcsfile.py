"template automatic tests"
import os.path as osp
from cubicweb.devtools import testlib

class AutomaticWebTest(testlib.AutomaticWebTest):
    no_auto_populate = ('Repository', 'Revision', 'VersionedFile',
                        'VersionContent', 'DeletedVersionContent',)
    ignored_relations = set(('at_revision', 'parent_revision',
                             'from_repository', 'from_revision', 'content_for',))

    def to_test_etypes(self):
        return set(('Repository',
                    'Revision',
                    'VersionedFile',
                    'DeletedVersionContent',
                    'VersionContent'))

    def custom_populate(self, how_many, cnx):
        cnx.create_entity('Repository', type=u'mercurial',
                          path=unicode(osp.join(self.datadir, 'testrepohg')),
                          encoding=u'latin1')

if __name__ == '__main__':
    from logilab.common.testlib import unittest_main
    unittest_main()
