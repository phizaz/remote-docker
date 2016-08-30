class Actions(object):
    LIST = 'LIST'
    DEFAULT = 'DEFAULT'
    NEW_HOST = 'NEW_HOST'
    NEW_ALIAS = 'NEW_ALIAS'
    RUN = 'RUN'

def parseargs(argv):
    import argparse

    class ExceptionHandledArgumentParser(argparse.ArgumentParser):
        def error(self, message):
            raise argparse.ArgumentError(None, message)

    parser = ExceptionHandledArgumentParser('RemoteDocker')
    subparse = parser.add_subparsers()

    parse_list = subparse.add_parser('list')
    parse_list.set_defaults(action=Actions.LIST)

    parse_default = subparse.add_parser('default')
    parse_default.add_argument('host')
    parse_default.set_defaults(action=Actions.DEFAULT)

    parse_new = subparse.add_parser('new')
    parse_new_sub = parse_new.add_subparsers()

    parse_new_host = parse_new_sub.add_parser('host')
    parse_new_host.add_argument('host')
    parse_new_host.add_argument('path', nargs='?', help='remote path')
    parse_new_host.set_defaults(action=Actions.NEW_HOST)

    parse_new_alias = parse_new_sub.add_parser('alias')
    parse_new_alias.add_argument('alias')
    parse_new_alias.add_argument('host')
    parse_new_alias.set_defaults(action=Actions.NEW_ALIAS)

    parse_run = subparse.add_parser('run')
    parse_run.add_argument('command', nargs=argparse.REMAINDER)
    parse_run.add_argument('--tag', required=True, help='tag')
    parse_run.add_argument('--host', help='host')
    parse_run.add_argument('--path', help='remote path')
    parse_run.set_defaults(action=Actions.RUN)

    args = parser.parse_args(argv)
    return args
