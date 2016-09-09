import unittest
from src import utils
from src.actions.ssh import ssh

class SSHTest(unittest.TestCase):

    def test_ssh(self):
        remote_host = 'ta@konpat.thddns.net:3830'
        ssh(remote_host, '~')