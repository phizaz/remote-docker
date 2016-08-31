import unittest
import arrow

class ArrowTest(unittest.TestCase):

    def test_init(self):
        a = arrow.utcnow()
        print(a, str(a))

    def test_parse(self):
        s = str(arrow.utcnow())
        a = arrow.get(s)
        print(a)

    def test_human_time_elapsed(self):
        a = arrow.utcnow()
        print(a.humanize())