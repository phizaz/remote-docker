class Actions(object):
    LIST = 'LIST'
    RUN = 'RUN'
    RESTART = 'RESTART'
    STOP = 'STOP'
    REMOVE = 'REMOVE'

def parseargs(argv):
    import argparse

    class ExceptionHandledArgumentParser(argparse.ArgumentParser):
        def error(self, message):
            raise argparse.ArgumentError(None, message)

    from .remotedocker import __version__
    parser = ExceptionHandledArgumentParser('RemoteDocker (version {}) : Run your script in a docker on another machine as if it were on yours'.format(__version__))
    subparse = parser.add_subparsers()

    parse_list = subparse.add_parser('list')
    parse_list.set_defaults(action=Actions.LIST)

    parse_run = subparse.add_parser('run')
    parse_run.add_argument('command', nargs=argparse.REMAINDER)
    parse_run.add_argument('--tag', help='tag')
    parse_run.add_argument('--host', help='host')
    parse_run.add_argument('--path', help='remote path')
    parse_run.add_argument('--docker', default='docker', help='docker executable, you can provide this value to be something like `nvidia-docker` (default: docker)')
    parse_run.set_defaults(action=Actions.RUN)

    parse_restart = subparse.add_parser('restart')
    parse_restart.add_argument('tag')
    parse_restart.set_defaults(action=Actions.RESTART)

    parse_stop = subparse.add_parser('stop')
    parse_stop.add_argument('tag')
    parse_stop.set_defaults(action=Actions.STOP)

    parse_remove = subparse.add_parser('rm')
    parse_remove.add_argument('tag')
    parse_remove.set_defaults(action=Actions.REMOVE)

    try:
        args = parser.parse_args(argv)
        return args
    except argparse.ArgumentError as e:
        from src import utils
        raise utils.errors.ArgumentError(str(e))
