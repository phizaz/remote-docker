import unittest
from src.actions import run
from src import utils

remote_host = 'ta@desktop.dyn.konpat.me'

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
        self.assertEqual(log, 'print(\'hello world!\')\n')

        _db = utils.DB.load()
        print(_db.dict())

        from os import remove
        remove(utils.path_file_ignore())
        remove(utils.path_file_db())

    def test_normal_flow_err(self):

        utils.init_ignore()

        db = utils.DB(None, [
            utils.Job(tag='test_normal_flow',
                      hosts=[remote_host],
                      using_host=remote_host,
                      remote_path='~/Projects/test-remotedocker/normal-flow',
                      command=['aoeu'],
                      step=None)
        ])

        self.assertRaises(utils.errors.WrongDockerExitcode, run.run, db.jobs[0], db, run.NormalFlow)

        from os import remove
        remove(utils.path_file_ignore())
        remove(utils.path_file_db())

