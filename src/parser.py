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

    parser = ExceptionHandledArgumentParser('RemoteDocker')
    subparse = parser.add_subparsers()

    parse_list = subparse.add_parser('list')
    parse_list.set_defaults(action=Actions.LIST)

    parse_run = subparse.add_parser('run')
    parse_run.add_argument('command', nargs=argparse.REMAINDER)
    parse_run.add_argument('--tag', required=True, help='tag')
    parse_run.add_argument('--host', help='host')
    parse_run.add_argument('--path', help='remote path')
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

    args = parser.parse_args(argv)
    return args
