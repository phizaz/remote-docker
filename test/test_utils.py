import unittest
from src import utils

# remote_host = 'ta@desktop.dyn.konpat.me'
# remote_host = 'ta@konpat.thddns.net:3830'
remote_host = 'ta@192.168.1.106'

class UtilsTest(unittest.TestCase):
    def test_DB_parse(self):
        import arrow
        a = arrow.utcnow()
        d = {
            'latest_job': {
                'tag': 'tag',
                'hosts': ['host1', 'host2'],
                'using_host': 'host1',
                'step': 'step',
                'docker': 'docker',
                'remote_path': 'remote_path',
                'command': 'command',
                'start_time': str(a),
                'container': 'container',
                'oth': dict(a=10),
            },
            'jobs': [
                {
                    'tag': 'tag',
                    'hosts': ['host1', 'host2'],
                    'using_host': 'host1',
                    'step': 'step',
                    'docker': 'docker',
                    'remote_path': 'remote_path',
                    'command': 'command',
                    'start_time': str(a),
                    'container': 'container',
                    'oth': dict(a=10),
                }
            ]
        }
        db = utils.DB.parse(d)
        self.assertDictEqual(db.latest_job.dict(), d['latest_job'])
        self.assertIsInstance(db.jobs[0], utils.Job)
        self.assertEqual(db.jobs[0].tag, 'tag')

    def test_DB_any_running(self):
        import arrow
        a = arrow.utcnow()
        d = {
            'latest_job': {
                'tag': 'tag',
                'hosts': ['host1', 'host2'],
                'using_host': 'host1',
                'step': 'step',
                'docker': 'docker',
                'remote_path': 'remote_path',
                'command': 'command',
                'start_time': str(a),
                'container': 'container',
                'oth': dict(a=10),
            },
            'jobs': [
                {
                    'tag': 'tag',
                    'hosts': ['host1', 'host2'],
                    'using_host': 'host1',
                    'step': 'step',
                    'docker': 'docker',
                    'remote_path': 'remote_path',
                    'command': 'command',
                    'start_time': str(a),
                    'container': 'container',
                    'oth': dict(a=10),
                }
            ]
        }
        db = utils.DB.parse(d)
        self.assertTrue(db.any_running())
        db.jobs[0].step = None
        self.assertFalse(db.any_running())

    def test_DB_get_latest(self):
        from os import remove
        from os.path import exists
        if exists(utils.path_file_db()):
            remove(utils.path_file_db())

        db = utils.DB.load()
        self.assertEqual(db.get_latest('tag'), None)

        import arrow
        a = arrow.utcnow()
        d = {
            'latest_job': {
                'tag': 'tag',
                'hosts': ['host1', 'host2'],
                'using_host': 'host1',
                'step': 'step',
                'docker': 'docker',
                'remote_path': 'remote_path',
                'command': 'command',
                'start_time': str(a),
                'container': 'container',
                'oth': dict(a=10),
            },
            'jobs': [
                {
                    'tag': 'tag',
                    'hosts': ['host1', 'host2'],
                    'using_host': 'host1',
                    'step': 'step',
                    'docker': 'docker',
                    'remote_path': 'remote_path',
                    'command': 'command',
                    'start_time': str(a),
                    'container': 'container',
                    'oth': dict(a=10),
                }
            ]
        }
        db = utils.DB.parse(d)
        self.assertEqual(db.get_latest('tag'), 'tag')
        self.assertEqual(db.get_latest('somethingnotthere'), None)

    def test_DB_load_dict_save(self):
        import arrow
        a = arrow.utcnow()
        d = {
            'latest_job': {
                'tag': 'tag',
                'hosts': ['host1', 'host2'],
                'using_host': 'host1',
                'step': 'step',
                'docker': 'docker',
                'remote_path': 'remote_path',
                'command': 'command',
                'start_time': str(a),
                'container': 'container',
                'oth': dict(a=10),
            },
            'jobs': [
                {
                    'tag': 'tag',
                    'hosts': ['host1', 'host2'],
                    'using_host': 'host1',
                    'step': 'step',
                    'docker': 'docker',
                    'remote_path': 'remote_path',
                    'command': 'command',
                    'start_time': str(a),
                    'container': 'container',
                    'oth': dict(a=10),
                }
            ]
        }
        db = utils.DB.parse(d)
        db.save()

        _db = utils.DB.load()
        self.assertDictEqual(db.dict(), _db.dict())

    def test_DB_remove_job(self):
        import arrow
        a = arrow.utcnow()
        d = {
            'latest_job': {
                'tag': 'tag',
                'hosts': ['host1', 'host2'],
                'using_host': 'host1',
                'step': 'step',
                'docker': 'docker',
                'remote_path': 'remote_path',
                'command': 'command',
                'start_time': str(a),
                'container': 'container',
                'oth': dict(a=10),
            },
            'jobs': [
                {
                    'tag': 'tag',
                    'hosts': ['host1', 'host2'],
                    'using_host': 'host1',
                    'step': 'step',
                    'docker': 'docker',
                    'remote_path': 'remote_path',
                    'command': 'command',
                    'start_time': str(a),
                    'container': 'container',
                    'oth': dict(a=10),
                },
                {
                    'tag': 'tag2',
                    'hosts': ['host1', 'host2'],
                    'using_host': 'host1',
                    'step': 'step',
                    'docker': 'docker',
                    'remote_path': 'remote_path',
                    'command': 'command',
                    'start_time': str(a),
                    'container': 'container',
                    'oth': dict(a=10),
                }
            ]
        }
        db = utils.DB.parse(d)
        db.remove_job(utils.Job('tag', [], None, None, None, None))
        self.assertEqual(len(db.jobs), 1)
        self.assertEqual(db.jobs[0].tag, 'tag2')

    def test_Job_parse(self):
        import arrow
        a = arrow.utcnow()
        d = {
            'tag': 'tag',
            'hosts': ['host1', 'host2'],
            'using_host': 'host1',
            'step': 'step',
            'docker': 'docker',
            'remote_path': 'remote_path',
            'command': 'command',
            'start_time': str(a),
            'container': 'container',
            'oth': dict(a=10),
        }
        job = utils.Job.parse(d)
        self.assertEqual(job.tag, 'tag')
        self.assertListEqual(job.hosts, ['host1', 'host2'])
        self.assertEqual(job.using_host, 'host1')
        self.assertEqual(job.step, 'step')
        self.assertEqual(job.docker, 'docker')
        self.assertEqual(job.remote_path, 'remote_path')
        self.assertEqual(job.command, 'command')
        self.assertEqual(str(job.start_time), str(a))
        self.assertEqual(job.container, 'container')
        self.assertDictEqual(job.oth, dict(a=10))

    def test_Job_dict(self):
        import arrow
        a = arrow.utcnow()
        d = {
            'tag': 'tag',
            'hosts': ['host1', 'host2'],
            'using_host': 'host1',
            'step': 'step',
            'docker': 'nvidia-docker',
            'remote_path': 'remote_path',
            'command': 'command',
            'start_time': str(a),
            'container': 'container',
            'oth': dict(a=10),
        }
        job = utils.Job.parse(d)
        self.assertDictEqual(job.dict(), d)

    def test_Job_init_without_start_time(self):
        import arrow
        j = utils.Job('tag', ['host1', 'host2'], 'host1', 'remote_path', 'command', 'step')
        aa = arrow.get(j.start_time)
        print(aa)

    def test_init_db(self):
        from os import remove
        from os.path import exists
        if exists(utils.path_file_db()):
            remove(utils.path_file_db())
        utils.init_db()
        self.assertTrue(exists(utils.path_file_db()))
        remove(utils.path_file_db())

    def test_init_ignore(self):
        from os import remove
        from os.path import exists
        if exists(utils.path_file_ignore()):
            remove(utils.path_file_ignore())
        utils.init_ignore()
        self.assertTrue(exists(utils.path_file_ignore()))
        remove(utils.path_file_ignore())

    def test_run_local(self):
        code, out = utils.run_local(['echo', 'test'])
        print(code)
        print(out)

        self.assertEqual(code, 0)
        self.assertListEqual(out, ['test'])

    def test_run_local_realtime(self):
        code, out = utils.run_local(['find', utils.path_src(), '-name', 'test'])
        print(code)
        print(out)

    def test_run_local_err(self):
        from os.path import join
        import sys
        file = join(utils.path_test(), 'supplementary', 'err_raise.py')
        code, out = utils.run_local([
            sys.executable,
            file
        ])
        print(code)
        print(out)

    def test_run_local_with_special(self):
        code, out = utils.run_local([
            'echo', '$(pwd)'
        ])
        print(code)
        print(out)

    def test_run_local_check_err(self):
        from os.path import join
        import sys
        file = join(utils.path_test(), 'supplementary', 'err_raise.py')
        self.assertRaises(utils.errors.WrongExitCode, utils.run_local_check, [
            sys.executable,
            file
        ])

    def test_run_remote(self):
        code, out = utils.run_remote(remote_host, '~/Projects/', ['echo', 'test'])
        print(code)
        print(out)
        self.assertEqual(code, 0)
        self.assertListEqual(out, ['test'])

    def test_run_remote_check(self):
        self.assertRaises(utils.errors.WrongExitCode, utils.run_remote_check, remote_host, '~/', ['aoeu'])

    def test_run_local_with_tty(self):
        code, out = utils.run_local_with_tty(['echo', 'test'])
        self.assertEqual(code, 0)
        self.assertListEqual(out, ['test'])

    def test_run_local_with_tty_check_err(self):
        self.assertRaises(utils.errors.WrongExitCode, utils.run_local_with_tty_check, ['aoeu'])

    def test_run_remote_with_tty_check(self):
        out = utils.run_remote_with_tty_check(remote_host, '~/Projects/', ['echo', 'test'])
        print(out)
        self.assertListEqual(out, ['test'])

    def test_run_local_check_return_last(self):
        out = utils.run_local_check_return_last(['echo', 'test'])
        self.assertEqual(out, 'test')

    def test_run_remote_with_tty_check_return_last(self):
        out = utils.run_remote_with_tty_check_return_last(remote_host, '~/Projects', ['echo', 'test'])
        self.assertEqual(out, 'test')
