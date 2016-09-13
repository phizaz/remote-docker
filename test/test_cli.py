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

# remote_host = 'ta@desktop.dyn.konpat.me'
remote_host = 'ta@192.168.1.104'


class CLITest(unittest.TestCase):
    def test_list(self):
        from os.path import join
        file = join(src.utils.path_src(), 'remotedocker.py')
        test.utils.run_python(file, 'list')

    def test_run_err_without_tag(self):
        src.utils.init_ignore()

        from os.path import join
        file = join(src.utils.path_src(), 'remotedocker.py')
        self.assertRaises(Exception, test.utils.run_python,
                          file, 'run', '--host=something', '--path=somepath', 'echo', 'test'
                          )

        from os import remove
        remove(src.utils.path_file_ignore())

    def test_run_existing(self):
        src.utils.init_ignore()
        import arrow
        a = arrow.utcnow()
        d = {
            'latest_host': 'a',
            'jobs': [
                {
                    'tag': 'test_run_existing',
                    'hosts': [remote_host],
                    'using_host': remote_host,
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
        remove(utils.path_file_ignore())

    def test_run(self):
        from src import utils
        utils.init_ignore()

        from os.path import join
        file = join(src.utils.path_src(), 'remotedocker.py')
        output = test.utils.run_python(
            file, 'run',
            '--tag=test_run',
            '--host={}'.format(remote_host),
            '--path=~/Projects/test-remotedocker/run-plain',
            'echo', 'test'
        )

        print('run output:', output)

        from os import remove
        remove(utils.path_file_db())
        remove(utils.path_file_ignore())

    def test_run_with_host(self):
        import arrow
        a = arrow.utcnow()
        d = {
            'latest_host': 'a',
            'jobs': [
                {
                    'tag': 'test_run_existing',
                    'hosts': [remote_host],
                    'using_host': remote_host,
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
        utils.init_ignore()
        db = utils.DB.parse(d)
        db.save()

        from os.path import join
        file = join(src.utils.path_src(), 'remotedocker.py')
        output = test.utils.run_python(
            file, 'run',
            '--tag=test_run_with_host',
            '--host={}'.format(remote_host),
            'echo', 'test'
        )

        print('run output:', output)

        from os import remove
        remove(utils.path_file_db())
        remove(utils.path_file_ignore())

    def test_run_by_adding_new_hots(self):
        import arrow
        a = arrow.utcnow()
        d = {
            'latest_host': 'a',
            'jobs': [
                {
                    'tag': 'test_run_adding_new_host',
                    'hosts': ['someexistinghost'],
                    'using_host': 'someexistinghost',
                    'step': None,
                    'docker': 'docker',
                    'remote_path': '~/Projects/test-remotedocker/run-adding-new-host',
                    'command': ['echo', 'test'],
                    'start_time': str(a),
                    'container': 'container',
                    'oth': dict(a=10),
                }
            ]
        }
        from src import utils
        utils.init_ignore()
        db = utils.DB.parse(d)
        db.save()

        from os.path import join
        file = join(src.utils.path_src(), 'remotedocker.py')
        output = test.utils.run_python(
            file, 'run',
            '--tag=test_run_adding_new_host',
            '--host={}'.format(remote_host)
        )

        print('run output:', output)

        from os import remove
        remove(utils.path_file_db())
        remove(utils.path_file_ignore())

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

        utils.init_ignore()
        utils.init_db()

        '''
        Init run
        $ remotedocker run --tag=tag --host=host --path=path echo test
        '''
        print('=====INIT RUN=====')
        test.utils.run_python(file, 'run',
                              '--tag=test_full_first',
                              '--host', remote_host,
                              '--path', '~/Projects/test-remotedocker/full',
                              'echo', 'test')

        '''
        Sync
        '''
        print('=====SYNC DOWN=====')
        test.utils.run_python(file, 'sync')

        '''
        Run again
        $ remotedocker run --tag=tag
        '''
        print('=====RUN AGAIN=====')
        test.utils.run_python(file, 'run',
                              '--tag=test_full_first')

        '''
        Add a host to the same run
        $ remotedocker run --tag=tag --host=newhost
        '''
        print('=====ADD HOST TO THE EXISTING RUN=====')
        db = utils.DB.load()
        db.jobs[0].host = 'somehost'
        db = utils.DB.parse(db.dict())
        db.save()

        db = utils.DB.load()

        print('current host:', db.jobs[0].using_host)

        another_host = remote_host
        test.utils.run_python(file, 'run',
                              '--tag=test_full_first',
                              '--host={}'.format(another_host))

        '''
        Start another run with the same host (latest) (same path)
        $ remotedocker run --tag=newtag echo test2
        '''
        print('=====START ANOTHER RUN WITH THE SAME HOST=====')
        test.utils.run_python(file, 'run',
                              '--tag=test_full_second',
                              'echo', 'test2')

        '''
        Restart the succeeded run
        '''
        print('=====RESTART=====')
        test.utils.run_python(file, 'restart')

        '''
        Stop the succeeded run
        '''
        print('=====STOP THE SUCCEEDED RUN=====')
        self.assertRaises(test.utils.run_python, file, 'stop')

        '''
        Remove the first run
        '''
        print('=====REMOVE THE FIRST RUN=====')
        self.assertRaises(Exception, test.utils.run_python, file, 'rm')
        test.utils.run_python(file, 'rm', 'test_full_first')

        db = utils.DB.load()
        self.assertEqual(len(db.jobs), 1)
        self.assertEqual(db.jobs[0].tag, 'test_full_second')

        from os import remove
        remove(utils.path_file_ignore())
        remove(utils.path_file_db())
