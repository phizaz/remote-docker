import unittest
from src.lib.ptty import PTY

class PttyTest(unittest.TestCase):
    def test(self):
        output = PTY().spawn(['echo', 'test'])
        self.assertEqual(output.strip(), 'test')