import unittest
from src import utils
from src.actions.list import print_list

class ListTest(unittest.TestCase):

    def test_print_list(self):
        db = utils.DB('ta@192.168.1.45', [
            utils.Job(tag='firstjob',
                      hosts=['ta@192.168.1.45', 'ta@desktop.dyn.konpat.me'],
                      using_host='ta@192.168.1.45',
                      remote_path='~/Projects/test/this/is/the/path',
                      command=['python', 'test_test_test.py'],
                      step=None)
        ])

        print_list(db)
