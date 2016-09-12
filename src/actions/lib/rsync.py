def rsync_up_command(host, remote_path, delete=True):
    from src import utils
    _host, _port = utils.resolve_host_port(host)
    command = [
        'rsync', '-az', '-e', 'ssh -p {port}'.format(port=_port),
        '--delete' if delete else '',
        '--verbose', '--progress',
        '--exclude-from={}'.format(utils.Files.IGNORE), './',
        '{host}:{path}'.format(host=_host, path=remote_path)
    ]
    return command


def rsync_up(host, remote_path, delete=True):
    from src import utils
    command = rsync_up_command(host, remote_path, delete=delete)
    return utils.run_local_check_return_last(command)


def rsync_down_command(host, remote_path):
    from src import utils
    _host, _port = utils.resolve_host_port(host)
    command = [
        'rsync', '-az',
        '--rsh=ssh -p {port}'.format(port=_port),
        '--update', '--verbose', '--progress',
        '--exclude-from={}'.format(utils.Files.IGNORE),
        '{host}:{path}/'.format(host=_host, path=remote_path),
        './'
    ]
    return command


def rsync_down(host, remote_path):
    from src import utils
    command = rsync_down_command(host, remote_path)
    return utils.run_local_check_return_last(command)
