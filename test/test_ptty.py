import unittest
from src.lib.ptty import PTY

class PttyTest(unittest.TestCase):
    def test(self):
        code, out = PTY().spawn(['echo', 'test'])
        print(code)
        print(out)
        self.assertEqual(code, 0)
        self.assertEqual(out, 'test\r\n')

    def test_err(self):
        code, out = PTY().spawn(['aoeu'])
        print(code)
        print(out)

    def test_err_late(self):
        code, out = PTY().spawn(['/bin/sh', 'aoeu'])

    def test_err_ssh(self):
        remote_host = 'ta@desktop.dyn.konpat.me'
        code, out = PTY().spawn([
            'ssh', '-t', remote_host, 'aoeu'
        ])
        print((code, out))
