import unittest
from src.actions.lib import rsync
from src import utils


class RsyncTest(unittest.TestCase):
    def test_rsync_up_command(self):
        c = rsync.rsync_up_command('some@host', '/some/path')
        print(c)
        self.assertListEqual(c, ['rsync', '-a', '--delete', '--verbose', '--exclude-from=.remotedignore', './',
                                 'some@host:/some/path'])

    def test_rsync_down_command(self):
        c = rsync.rsync_down_command('some@host', '/some/path')
        print(c)
        self.assertListEqual(c, ['rsync', '-au', '--verbose', '--exclude-from=.remotedignore', 'some@host:/some/path/',
                                 './'])

    def test_rsync_up(self):
        utils.init_ignore()
        rsync.rsync_up('ta@desktop.dyn.konpat.me', '$(pwd)/Projects/test-remotedocker')
        from os import remove
        remove(utils.path_file_ignore())

    def test_rsync_down(self):
        utils.init_ignore()
        rsync.rsync_down('ta@desktop.dyn.konpat.me', '$(pwd)/Projects/test-remotedocker')
        from os import remove
        remove(utils.path_file_ignore())


