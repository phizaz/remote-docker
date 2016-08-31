import unittest

'''
Usage:

remotedocker list
$ tag           host        step                time elapsed
$ firstrun      ta@home     sync to remote      5 minute
$ secondrun     test@remote building            3 seconds

remotedocker run [options] [cmd [args...]]
remotedocker run -t tagname python test.py [args...] << using the latest host
remotedocker run -t tagname -h old@host python test.py [args...] << using a given host
remotedocker run -t tagname -h new@host -p /remote/path python test.py [args...] << using a given (new) host

remotedocker run -t tag -h alias@host ...
remotedocker run -t tag -h some@host ... << point to the same thing


# conflict
remotedocker run -t tagname xxxxxxx
$ tag conflicted !
$ do you want to discard to old run ? (y/n) y
-> docker rm --force {container_name}
-> reset the step to 'start'
-> run the designated 'run'

remotedocker run -t tagname << continue the job, or fetch the updates

Steps:

1. sync to the remote (rsync -a --delete)
2. docker-compose build env
3. docker-compose run env {command here} >> {container_name}
4. docker logs {container_name}
5. docker rm {container_name}
6. sync back from the remote (rsync -au << using update mode)

'''

import src.utils
import test.utils

class CLITest(unittest.TestCase):
    def test_list(self):
        from os.path import join
        file = join(src.utils.path_src(), 'remotedocker.py')
        output = test.utils.run_python(file, 'list')
        print(output)
        raise NotImplementedError

    def test_run_without_conflict(self):
        from os.path import join
        file = join(src.utils.path_src(), 'remotedocker.py')
        output = test.utils.run_python(file, 'run', '-t', 'test_tag', 'python', '')

