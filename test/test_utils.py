import unittest
from src import utils


class UtilsTest(unittest.TestCase):
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
        code, out = utils.run_global('ta@desktop.dyn.konpat.me', '~/Projects/', ['echo', 'test'])
        print(code)
        print(out)
        self.assertEqual(code, 0)
        self.assertEqual(out, 'test\n')

    def test_run_global_check(self):
        self.assertRaises(AssertionError, utils.run_global_check, 'ta@desktop.dyn.konpat.me', '~/', ['aoeu'])
