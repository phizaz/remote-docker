def rsync_up_command(host, remote_path):
    from src.utils import Files
    command = [
        'rsync', '-a', '--delete', '--verbose',
        '--exclude-from={}'.format(Files.IGNORE), './',
        '{host}:{path}'.format(host=host, path=remote_path)
    ]
    return command

def rsync_up(host, remote_path):
    from src import utils
    command = rsync_up_command(host, remote_path)
    return utils.run_local_check(command)

def rsync_down_command(host, remote_path):
    from src.utils import Files
    command = [
        'rsync', '-au', '--verbose',
        '--exclude-from={}'.format(Files.IGNORE),
        '{host}:{path}/'.format(host=host, path=remote_path),
        './'
    ]
    return command

def rsync_down(host, remote_path):
    from src import utils
    command = rsync_down_command(host, remote_path)
    return utils.run_local_check(command)

