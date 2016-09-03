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
            ['run', '--docker=nvidia-docker', '--tag', 'sometag', '--host=some@host', '--path=/some/path', 'python', 'test.py', 'a', '--b=c'])
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

    def test_restart(self):
        args = parseargs(['restart', 'tag'])
        print(args)
        self.assertEqual(args.action, Actions.RESTART)
        self.assertEqual(args.tag, 'tag')

    def test_stop(self):
        args = parseargs(['stop', 'tag'])
        print(args)
        self.assertEqual(args.action, Actions.STOP)
        self.assertEqual(args.tag, 'tag')

    def test_rm(self):
        args = parseargs(['rm', 'tag'])
        print(args)
        self.assertEqual(args.action, Actions.REMOVE)
        self.assertEqual(args.tag, 'tag')