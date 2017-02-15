class Actions(object):
    LIST = 'LIST'
    RUN = 'RUN'
    RESTART = 'RESTART'
    STOP = 'STOP'
    REMOVE = 'REMOVE'
    SSH = 'SSH'
    SYNC = 'SYNC'
    SYNC_UP = 'SYNC_UP'


def parseargs(argv):
    import argparse

    class ExceptionHandledArgumentParser(argparse.ArgumentParser):
        def error(self, message):
            raise argparse.ArgumentError(None, message)

    from .remotedocker import __version__
    parser = ExceptionHandledArgumentParser(
        'RemoteDocker (version {}) : Run your script in a docker on another machine as if it were on yours'.format(
            __version__))
    subparse = parser.add_subparsers()

    parse_list = subparse.add_parser('list')
    parse_list.set_defaults(action=Actions.LIST)

    parse_run = subparse.add_parser('run')
    parse_run.add_argument('command', nargs=argparse.REMAINDER)
    parse_run.add_argument('--tag', help='a tag, latest used if not provided (only for running the old tag)')
    parse_run.add_argument('--host', help='a host, user@host[:port]')
    parse_run.add_argument('--path', help='a remote path, can be a relative path on the remote host')
    parse_run.add_argument('--docker',
                           help='docker executable, you can provide this value to be something like `nvidia-docker` (default: docker)')
    parse_run.set_defaults(action=Actions.RUN)

    parse_restart = subparse.add_parser('restart')
    parse_restart.add_argument('tag', nargs='?', help='a tag, latest used if not provided')
    parse_restart.add_argument('--force', action='store_true',
                               help='if anything should go wrong, will you consent to still restart it?')
    parse_restart.set_defaults(action=Actions.RESTART)

    parse_stop = subparse.add_parser('stop')
    parse_stop.add_argument('tag', nargs='?', help='a tag, latest used if not provided')
    parse_stop.add_argument('--force', action='store_true',
                            help='if anything should go wrong, will you consent to still stop it?')
    parse_stop.set_defaults(action=Actions.STOP)

    parse_remove = subparse.add_parser('rm')
    parse_remove.add_argument('tag', help='a tag, you must specify this explicitly')
    parse_remove.add_argument('--force', action='store_true',
                              help='if anything should go wrong, will you consent to still remove it?')
    parse_remove.set_defaults(action=Actions.REMOVE)

    parse_ssh = subparse.add_parser('ssh')
    parse_ssh.add_argument('tag', nargs='?', help='a tag of which host we will ssh into')
    parse_ssh.set_defaults(action=Actions.SSH)

    parse_sync = subparse.add_parser('sync')
    parse_sync.add_argument('tag', nargs='?', help='a tag of which host we will sync back from')
    parse_sync.set_defaults(action=Actions.SYNC)

    parse_sync_up = subparse.add_parser('syncup')
    parse_sync_up.add_argument('tag', nargs='?', help='a tag of which host we will sync to')
    parse_sync_up.set_defaults(action=Actions.SYNC_UP)

    try:
        args = parser.parse_args(argv)

        if not getattr(args, 'action', None):
            raise argparse.ArgumentError(None, 'No action provided')

        return args
    except argparse.ArgumentError as e:
        from src import utils
        raise utils.errors.ArgumentError(str(e))
