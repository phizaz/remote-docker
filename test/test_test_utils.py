import unittest

class TestUtilsTest(unittest.TestCase):

    def test_run_python(self):
        import src.utils
        import test.utils
        from os.path import join
        path = join(src.utils.path_test(), 'supplementary')
        file = join(path, 'hello.py')
        r = test.utils.run_python(file)
        self.assertEqual(r, 'hello world!\n')
        file = join(path, 'echo.py')
        r = test.utils.run_python(file, 'a', 'b', aa='aa')
        self.assertEqual(r, "['a', 'b', '--aa=aa']\n")
        file = join(path, 'err_errcode.py')
        self.assertRaises(Exception, test.utils.run_python, file)
        file = join(path, 'err_raise.py')
        self.assertRaises(Exception, test.utils.run_python, file)

