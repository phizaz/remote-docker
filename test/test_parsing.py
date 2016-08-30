import unittest
import test.utils
import src.utils

class ParsingTest(unittest.TestCase):

    def test_run(self):
        import argparse

        def list(args):
            print('list')

        def run(args):
            print(args)

        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers()

        parser_list = subparsers.add_parser('list')
        parser_list.set_defaults(func=list)

        parser_run = subparsers.add_parser('run')
        parser_run.add_argument('--tag', required=True)
        parser_run.set_defaults(func=run)

        args = parser.parse_args(['run', '--tag=10'])
        args.func(args)
