import unittest
from src.actions import run
from src import utils

class RunTest(unittest.TestCase):

    def test_normal_flow(self):

        utils.init_ignore()

        db = [
            utils.Job('test_normal_flow',
                      'ta@desktop.dyn.konpat.me',
                      '~/test_remote_desktop_normal_flow',
                      ['echo', 'test'],
                      None)
        ]

        run.run_job(db[0], db, run.NormalFlow)

        _db = utils.get_db()
        print(_db[0].dict())

        from os import remove
        remove(utils.path_file_ignore())
        remove(utils.path_file_db())

    def test_normal_flow_err(self):

        utils.init_ignore()

        db = [
            utils.Job('test_normal_flow',
                      'ta@desktop.dyn.konpat.me',
                      '~/test_remote_desktop_normal_flow',
                      ['aoeu'],
                      None)
        ]

        self.assertRaises(Exception, run.run_job, db[0], db, run.NormalFlow)

        from os import remove
        remove(utils.path_file_ignore())
        remove(utils.path_file_db())