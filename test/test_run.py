import unittest
from src.actions import run
from src import utils

# remote_host = 'ta@desktop.dyn.konpat.me'
remote_host = 'ta@192.168.1.45'

class RunTest(unittest.TestCase):

    def test_normal_flow(self):

        utils.init_ignore()

        db = utils.DB(None, None, [
            utils.Job(tag='test_normal_flow',
                      hosts=[remote_host],
                      using_host=remote_host,
                      remote_path='~/Projects/test-remotedocker/normal-flow',
                      command=['cat', 'supplementary/hello.py'],
                      step=None)
        ])

        log = run.run(db.jobs[0], db, run.NormalFlow)
        print('run output:', log)
        self.assertEqual(log, 'print(\'hello world!\')')

        _db = utils.DB.load()
        print(_db.dict())
        self.assertEqual(_db.latest_host, remote_host)
        self.assertEqual(_db.latest_tag, 'test_normal_flow')

        from os import remove
        remove(utils.path_file_ignore())
        remove(utils.path_file_db())

    def test_normal_flow_err(self):

        utils.init_ignore()

        db = utils.DB(None, None, [
            utils.Job(tag='test_normal_flow_err',
                      hosts=[remote_host],
                      using_host=remote_host,
                      remote_path='~/Projects/test-remotedocker/normal-flow-err',
                      command=['aoeu'],
                      step=None)
        ])

        self.assertRaises(utils.errors.WrongExitCode, run.run, db.jobs[0], db, run.NormalFlow)

        _db = utils.DB.load()
        self.assertEqual(_db.latest_tag, 'test_normal_flow_err')
        self.assertEqual(_db.latest_host, remote_host)

        from os import remove
        remove(utils.path_file_ignore())
        remove(utils.path_file_db())

