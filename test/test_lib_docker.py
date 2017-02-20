import unittest
from src.actions.lib import docker

from os import environ

environ['PATH'] += ':/usr/local/bin'


class DockerTest(unittest.TestCase):
    def test_docker_build_command(self):
        command = docker.docker_build_command('test:test', '.', 'docker')
        self.assertListEqual(command, ['docker', 'build', '-t', 'test:test', '.'])

    def test_docker_run_command(self):
        command = docker.docker_run_command('debian:jessie', '$(pwd)', ['cat', 'supplementary/hello.py'], 'nvidia-docker')
        print(command)
        self.assertListEqual(command,
                             ['nvidia-docker', 'run', '--user', '${UID}', '-v $(pwd):/run', '-d', '-w', '/run', 'debian:jessie', 'cat',
                              'supplementary/hello.py'])

        command = docker.docker_run_command('debian:jessie', None, ['echo', 'test'], 'docker')
        self.assertListEqual(command, ['docker', 'run', '--user', '${UID}', '-d', '-w', '/run', 'debian:jessie', 'echo', 'test'])

    def test_docker_logs_command(self):
        command = docker.docker_logs_command('aoeu', 'docker')
        self.assertListEqual(command, ['docker', 'logs', '-f', '--tail=all', 'aoeu'])
        command = docker.docker_logs_command('container', 'docker', 1000)
        self.assertListEqual(command, ['docker', 'logs', '-f', '--tail=1000', 'container'])

    def test_docker_exit_code_command(self):
        command = docker.docker_exit_code_command('aoeu', 'docker')
        print(command)
        self.assertListEqual(command, ['docker', 'inspect', '-f', '{{.State.ExitCode}}', 'aoeu'])

    def test_docker_rm_command(self):
        command = docker.docker_rm_command('aoeu', 'docker')
        print(command)
        self.assertListEqual(command, ['docker', 'rm', '-f', 'aoeu'])

    def test_docker_build_run_logs_exit_code_rm(self):
        from src import utils
        img = 'test_remotedocker_build'
        command = docker.docker_build_command(img, '.', 'docker')
        utils.run_local_with_tty_check_return_last(command)

        command = docker.docker_run_command(img, None, ['echo', 'test'], 'docker')
        container = utils.run_local_with_tty_check_return_last(command)
        container = container.strip()

        command = docker.docker_logs_command(container, 'docker')
        logs = utils.run_local_with_tty_check_return_last(command)
        self.assertEqual(logs, 'test')

        command = docker.docker_exit_code_command(container, 'docker')
        exit_code = utils.run_local_with_tty_check_return_last(command)
        self.assertEqual(exit_code, '0')

        command = docker.docker_rm_command(container, 'docker')
        utils.run_local_with_tty_check_return_last(command)



