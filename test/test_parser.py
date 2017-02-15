import unittest

from src.parser import parseargs, Actions
from src import utils


class ParserTest(unittest.TestCase):
    def test_list(self):
        args = parseargs(['list'])
        print(args)
        self.assertEqual(args.action, Actions.LIST)

    def test_run_with_alien(self):
        self.assertRaises(utils.errors.ArgumentError, parseargs, [
            'run', '--tag=test', '--host=aoeu', '--path=path', '--alien=10'
        ])

    def test_run_with_host_and_path(self):
        args = parseargs(
            ['run', '--docker=nvidia-docker', '--tag', 'sometag', '--host=some@host', '--path=/some/path', 'python',
             'test.py', 'a', '--b=c'])
        print(args)
        self.assertEqual(args.action, Actions.RUN)
        self.assertEqual(args.docker, 'nvidia-docker')
        self.assertEqual(args.tag, 'sometag')
        self.assertEqual(args.host, 'some@host')
        self.assertEqual(args.path, '/some/path')
        self.assertListEqual(args.command, ['python', 'test.py', 'a', '--b=c'], )

    def test_run_with_host(self):
        args = parseargs(['run', '--tag', 'sometag', '--host=some@host', 'python', 'test.py', 'a', '--b=c'])
        print(args)
        self.assertEqual(args.action, Actions.RUN)
        self.assertEqual(args.tag, 'sometag')
        self.assertEqual(args.host, 'some@host')
        self.assertIsNone(args.path)
        self.assertListEqual(args.command, ['python', 'test.py', 'a', '--b=c'], )

    def test_run_plain(self):
        args = parseargs(['run', '--tag', 'sometag', 'python', 'test.py', 'a', '--b=c'])
        print(args)
        self.assertEqual(args.action, Actions.RUN)
        self.assertEqual(args.tag, 'sometag')
        self.assertIsNone(args.host)
        self.assertIsNone(args.path)
        self.assertListEqual(args.command, ['python', 'test.py', 'a', '--b=c'], )

    def test_restart_with_only_tag(self):
        args = parseargs(['restart', 'tag'])
        self.assertEqual(args.action, Actions.RESTART)
        self.assertEqual(args.tag, 'tag')
        self.assertFalse(args.force)

    def test_restart_force(self):
        args = parseargs(['restart', 'tag', '--force'])
        self.assertEqual(args.action, Actions.RESTART)
        self.assertEqual(args.tag, 'tag')
        self.assertTrue(args.force)

    def test_restart_with_no_tag(self):
        args = parseargs(['restart'])
        print(args)
        self.assertIsNone(args.tag)

    def test_stop_with_only_tag(self):
        args = parseargs(['stop', 'tag'])
        self.assertEqual(args.action, Actions.STOP)
        self.assertEqual(args.tag, 'tag')
        self.assertFalse(args.force)

    def test_stop_with_force(self):
        args = parseargs(['stop', 'tag', '--force'])
        self.assertEqual(args.action, Actions.STOP)
        self.assertEqual(args.tag, 'tag')
        self.assertTrue(args.force)

    def test_stop_with_no_tag(self):
        args = parseargs(['stop'])
        self.assertIsNone(args.tag)

    def test_rm_can_accept_tag(self):
        args = parseargs(['rm', 'tag'])
        self.assertEqual(args.action, Actions.REMOVE)
        self.assertEqual(args.tag, 'tag')
        self.assertFalse(args.force)

    def test_rm_with_force_true(self):
        args = parseargs(['rm', 'tag', '--force'])
        self.assertEqual(args.action, Actions.REMOVE)
        self.assertTrue(args.force)

    def test_rm_no_tag_will_raise(self):
        self.assertRaises(utils.errors.ArgumentError, parseargs, ['rm'])

    def test_ssh(self):
        args = parseargs(['ssh', 'tag'])
        print(args)
        self.assertEqual(args.action, Actions.SSH)
        self.assertEqual(args.tag, 'tag')

        args = parseargs(['ssh'])
        self.assertEqual(args.action, Actions.SSH)

    def test_sync(self):
        args = parseargs(['sync', 'tag'])
        print(args)
        self.assertEqual(args.action, Actions.SYNC)
        self.assertEqual(args.tag, 'tag')

        args = parseargs(['sync'])
        self.assertEqual(args.action, Actions.SYNC)

    def test_sync_up(self):
        args = parseargs(['syncup', 'tag'])
        print(args)
        self.assertEqual(args.action, Actions.SYNC_UP)
        self.assertEqual(args.tag, 'tag')

        args = parseargs(['syncup'])
        self.assertEqual(args.action, Actions.SYNC_UP)
