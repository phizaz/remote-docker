import unittest
from src import utils


class UtilsTest(unittest.TestCase):
    def test_Job(self):
        import arrow
        a = arrow.utcnow()
        j = utils.Job('tag', 'host', 'step', a)
        print(j.dict())
        self.assertDictEqual(j.dict(), {
            'tag': 'tag',
            'host': 'host',
            'step': 'step',
            'start_time': str(a)
        })

        j = utils.Job('tag', 'host', 'step')
        aa = arrow.get(j.start_time)
        print(aa)

    def test_Host(self):
        h = utils.Host('some@host', '/some/path')
        self.assertDictEqual(h.dict(), {
            'host': 'some@host',
            'remote_path': '/some/path'
        })

    def test_Alias(self):
        h = utils.Host('some@host', '/some/path')
        a = utils.Alias('alias@host', h)
        self.assertDictEqual(a.dict(), {
            'host': 'some@host',
            'alias': 'alias@host'
        })

    def test_init_hosts(self):
        from os import remove
        from os.path import exists
        if exists(utils.path_file_hosts()):
            remove(utils.path_file_hosts())
        utils.init_hosts()
        self.assertTrue(exists(utils.path_file_hosts()))
        remove(utils.path_file_hosts())

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

    def test_get_hosts(self):
        with open(utils.Files.HOSTS, 'w') as handle:
            import yaml
            yaml.safe_dump([
                { 'host': 'a@a', 'remote_path': '/path/a'},
                { 'alias': 'b@b', 'host': 'a@a'}
            ], handle)

        from os import remove
        hosts = utils.get_hosts()
        self.assertEqual(hosts[0].host, 'a@a')
        self.assertEqual(hosts[0].remote_path, '/path/a')
        self.assertEqual(hosts[1].host, 'a@a')
        self.assertEqual(hosts[1].alias, 'b@b')
        self.assertEqual(hosts[1].remote_path, '/path/a')
        print(hosts)
        remove(utils.Files.HOSTS)

    def test_save_hosts(self):
        host = utils.Host('a@a', '/path/a')
        utils.save_hosts([
            host,
            utils.Alias('b@b', host)
        ])

        with open(utils.path_file_hosts()) as handle:
            import yaml
            content = yaml.load(handle)

        self.assertListEqual(content, [
            {'host': 'a@a', 'remote_path': '/path/a'},
            {'alias': 'b@b', 'host': 'a@a'}
        ])



    def test_run_local(self):
        code, out = utils.run_local(['echo', 'test'])
        print(code)
        print(out)

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

    def test_run_local_check_err(self):
        from os.path import join
        import sys
        file = join(utils.path_test(), 'supplementary', 'err_raise.py')
        self.assertRaises(Exception, utils.run_local_check, [
            sys.executable,
            file
        ])

    def test_run_global(self):
        code, out = utils.run_remote('ta@desktop.dyn.konpat.me', '~/Projects/', ['echo', 'test'])
        print(code)
        print(out)
        self.assertEqual(code, 0)
        self.assertEqual(out, 'test\n')

    def test_run_global_check(self):
        self.assertRaises(AssertionError, utils.run_remote_check, 'ta@desktop.dyn.konpat.me', '~/', ['aoeu'])
