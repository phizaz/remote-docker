import unittest
from src.actions import run
from src import utils

# remote_host = 'ta@desktop.dyn.konpat.me'
remote_host = 'ta@192.168.1.104'

class RunTest(unittest.TestCase):

    def test_normal_flow(self):

        utils.init_ignore()

        db = utils.DB(None, [
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
        self.assertDictEqual(_db.latest_job.dict(), db.jobs[0].dict())

        from os import remove
        remove(utils.path_file_ignore())
        remove(utils.path_file_db())

    def test_normal_flow_update_mode(self):
        utils.init_ignore()

        db = utils.DB(None, [
            utils.Job(tag='test_normal_flow',
                      hosts=[remote_host],
                      using_host=remote_host,
                      remote_path='~/Projects/test-remotedocker/normal-flow',
                      command=['cat', 'supplementary/hello.py'],
                      step=None),
            utils.Job(tag='another_task',
                      hosts=[remote_host],
                      using_host=remote_host,
                      remote_path='~/Projects/test-remotedocker/normal-flow',
                      command=['cat', 'supplementary/hello.py'],
                      step='running')
        ])

        log = run.run(db.jobs[0], db, run.NormalFlow)
        print('run output:', log)
        self.assertEqual(log, 'print(\'hello world!\')')

        _db = utils.DB.load()
        print(_db.dict())
        self.assertDictEqual(_db.latest_job.dict(), db.jobs[0].dict())

        from os import remove
        remove(utils.path_file_ignore())
        remove(utils.path_file_db())


    def test_normal_flow_err(self):

        utils.init_ignore()

        db = utils.DB(None, [
            utils.Job(tag='test_normal_flow_err',
                      hosts=[remote_host],
                      using_host=remote_host,
                      remote_path='~/Projects/test-remotedocker/normal-flow-err',
                      command=['aoeu'],
                      step=None)
        ])

        self.assertRaises(utils.errors.WrongExitCode, run.run, db.jobs[0], db, run.NormalFlow)

        _db = utils.DB.load()
        self.assertDictEqual(_db.latest_job.dict(), db.jobs[0].dict())

        from os import remove
        remove(utils.path_file_ignore())
        remove(utils.path_file_db())

