import unittest
from src.actions import run
from src import utils

class RunTest(unittest.TestCase):

    def test_normal_flow(self):

        utils.init_ignore()

        db = utils.DB(None, [
            utils.Job(tag='test_normal_flow',
                      hosts=['ta@192.168.1.45', 'ta@desktop.dyn.konpat.me'],
                      using_host='ta@192.168.1.45',
                      remote_path='~/test_remote_desktop_normal_flow',
                      command=['echo', 'test'],
                      step=None)
        ])

        run.run(db.jobs[0], db, run.NormalFlow)

        _db = utils.DB.load()
        print(_db.dict())

        from os import remove
        remove(utils.path_file_ignore())
        remove(utils.path_file_db())

    def test_normal_flow_err(self):

        utils.init_ignore()

        db = utils.DB(None, [
            utils.Job(tag='test_normal_flow',
                      hosts=['ta@192.168.1.45', 'ta@desktop.dyn.konpat.me'],
                      using_host='ta@192.168.1.45',
                      remote_path='~/test_remote_desktop_normal_flow',
                      command=['aoeu'],
                      step=None)
        ])

        self.assertRaises(Exception, run.run, db.jobs[0], db, run.NormalFlow)

        from os import remove
        remove(utils.path_file_ignore())
        remove(utils.path_file_db())