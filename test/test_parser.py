import unittest

from src.parser import parseargs, Actions


class ParserTest(unittest.TestCase):
    def test_list(self):
        args = parseargs(['list'])
        print(args)
        self.assertEqual(args.action, Actions.LIST)

    def test_default(self):
        args = parseargs(['default', 'some@host'])
        print(args)
        self.assertEqual(args.action, Actions.DEFAULT)
        self.assertEqual(args.host, 'some@host')

    def test_new_host(self):
        args = parseargs(['new', 'host', 'some@host', '/some/path'])
        print(args)
        self.assertEqual(args.action, Actions.NEW_HOST)
        self.assertEqual(args.host, 'some@host')
        self.assertEqual(args.path, '/some/path')

    def test_new_alias(self):
        args = parseargs(['new', 'alias', 'some@host', 'old@host'])
        print(args)
        self.assertEqual(args.action, Actions.NEW_ALIAS)
        self.assertEqual(args.alias, 'some@host')
        self.assertEqual(args.host, 'old@host')

    def test_run_with_host_and_path(self):
        args = parseargs(['run', '--tag', 'sometag', '--host=some@host', '--path=/some/path', 'python', 'test.py', 'a', '--b=c'])
        print(args)
        self.assertEqual(args.action, Actions.RUN)
        self.assertEqual(args.tag, 'sometag')
        self.assertEqual(args.host, 'some@host')
        self.assertEqual(args.path, '/some/path')
        self.assertListEqual(args.command, ['python', 'test.py', 'a', '--b=c'],)

    def test_run_with_host(self):
        args = parseargs(['run', '--tag', 'sometag', '--host=some@host', 'python', 'test.py', 'a', '--b=c'])
        print(args)
        self.assertEqual(args.action, Actions.RUN)
        self.assertEqual(args.tag, 'sometag')
        self.assertEqual(args.host, 'some@host')
        self.assertListEqual(args.command, ['python', 'test.py', 'a', '--b=c'],)

    def test_run_plain(self):
        args = parseargs(['run', '--tag', 'sometag', 'python', 'test.py', 'a', '--b=c'])
        print(args)
        self.assertEqual(args.action, Actions.RUN)
        self.assertEqual(args.tag, 'sometag')
        self.assertListEqual(args.command, ['python', 'test.py', 'a', '--b=c'],)

    def test_run_err_without_tag(self):
        import argparse
        self.assertRaises(argparse.ArgumentError, parseargs, ['run', 'python', 'test.py', 'a', '--b=c'])
