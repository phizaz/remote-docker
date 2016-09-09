def ssh(host, path):
    import os
    import sys
    sys.stdout.flush()

    from src import utils
    _host, _port = utils.resolve_host_port(host)
    os.execvp('ssh', ['ssh', '-t', '-p', _port, _host, 'cd', path, ';', 'bash'])

