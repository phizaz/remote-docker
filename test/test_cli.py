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

remotedocker run -t tagname << continue the job, or fetch the updates

remotedocker restart <tag>
remotedocker stop <tag>
remotedocker remove <tag>

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
        test.utils.run_python(file, 'list')

    def test_run_existing(self):
        import arrow
        a = arrow.utcnow()
        d = {
            'latest_host': 'a',
            'jobs': [
                {
                    'tag': 'test_run_existing',
                    'hosts': ['ta@192.168.1.45'],
                    'using_host': 'ta@192.168.1.45',
                    'step': None,
                    'docker': 'docker',
                    'remote_path': '~/Projects/test-remotedocker/run_existing',
                    'command': ['echo', 'test'],
                    'start_time': str(a),
                    'container': 'container',
                    'oth': dict(a=10),
                }
            ]
        }
        from src import utils
        db = utils.DB.parse(d)
        db.save()

        from os.path import join
        file = join(src.utils.path_src(), 'remotedocker.py')
        output = test.utils.run_python(
            file, 'run', '--tag=test_run_existing'
        )

        print('run output:', output)

        from os import remove
        remove(utils.path_file_db())

    def test_run(self):
        from src import utils

        from os.path import join
        file = join(src.utils.path_src(), 'remotedocker.py')
        output = test.utils.run_python(
            file, 'run',
            '--tag=test_run_existing',
            '--host=ta@192.168.1.45',
            '--path=~/Projects/test-remotedocker/run-plain'
            'echo', 'test'
        )

        print('run output:', output)

        from os import remove
        remove(utils.path_file_db())

    def test_run_with_host(self):
        import arrow
        a = arrow.utcnow()
        d = {
            'latest_host': 'a',
            'jobs': [
                {
                    'tag': 'test_run_existing',
                    'hosts': ['ta@192.168.1.45'],
                    'using_host': 'ta@192.168.1.45',
                    'step': None,
                    'docker': 'docker',
                    'remote_path': '~/Projects/test-remotedocker/run-with-host',
                    'command': ['echo', 'test'],
                    'start_time': str(a),
                    'container': 'container',
                    'oth': dict(a=10),
                }
            ]
        }
        from src import utils
        db = utils.DB.parse(d)
        db.save()

        from os.path import join
        file = join(src.utils.path_src(), 'remotedocker.py')
        output = test.utils.run_python(
            file, 'run',
            '--tag=test_run_existing',
            '--host=ta@192.168.1.45',
            'echo', 'test'
        )

        print('run output:', output)

        from os import remove
        remove(utils.path_file_db())

    def test_restart(self):
        raise NotImplementedError

    def test_stop(self):
        raise NotImplementedError

    def test_remove(self):
        raise NotImplementedError

    def test_full(self):
        from src import utils
        from os.path import join
        file = join(src.utils.path_src(), 'remotedocker.py')
        output = test.utils.run_python(
            file, 'run',
            '--tag=test_run_existing',
            '--host=ta@192.168.1.45',
            'echo', 'test'
        )
        raise NotImplementedError



