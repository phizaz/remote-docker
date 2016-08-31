class Files(object):
    HOSTS = '.remotedhosts'
    DB = '.remoteddb'
    IGNORE = '.remotedignore'


class Job(object):
    def __init__(self, tag, host, step, command, start_time=None, container=None):
        import arrow
        self.tag = tag
        self.host = host
        self.step = step
        self.command = command
        if not start_time:
            self.start_time = arrow.utcnow()
        else:
            self.start_time = arrow.get(start_time)
        self.container = container

    def dict(self):
        return {
            'tag': self.tag,
            'host': self.host,
            'step': self.step,
            'command': self.command,
            'start_time': str(self.start_time),
            'container': self.container,
        }

    def time_elapsed(self):
        return self.start_time.humanize()


class Host(object):
    def __init__(self, host, remote_path):
        self.host = host
        self.remote_path = remote_path

    def dict(self):
        return self.__dict__


class Alias(object):
    def __init__(self, alias, host):
        assert isinstance(host, Host)
        self.alias = alias
        self.host = host.host
        self.remote_path = host.remote_path

    def dict(self):
        return {
            'alias': self.alias,
            'host': self.host
        }


def path_root():
    from os.path import dirname
    return dirname(dirname(__file__))


def path_caller():
    from os import getcwd
    return getcwd()


def path_src():
    from os.path import join
    return join(path_root(), 'src')


def path_test():
    from os.path import join
    return join(path_root(), 'test')


def path_file_hosts():
    from os.path import join
    return join(path_caller(), Files.HOSTS)


def path_file_db():
    from os.path import join
    return join(path_caller(), Files.DB)


def path_file_ignore():
    from os.path import join
    return join(path_caller(), Files.IGNORE)


def init_hosts():
    from shutil import copy
    from os.path import join
    copy(join(path_src(), 'static', Files.HOSTS), path_file_hosts())


def init_db():
    from shutil import copy
    from os.path import join
    copy(join(path_src(), 'static', Files.DB), path_file_db())


def init_ignore():
    from shutil import copy
    from os.path import join
    copy(join(path_src(), 'static', Files.IGNORE), path_file_ignore())


def get_hosts():
    '''
    [
        {host: ..., remote_path: ...}
        {alias: ..., host: ...}
    ]
    '''
    from os.path import exists

    if not exists(path_file_hosts()):
        init_hosts()

    with open(path_file_hosts()) as handle:
        import yaml
        content = yaml.load(handle)

    assert isinstance(content, list), 'hosts must be a list'

    plain_hosts = filter(lambda x: 'alias' not in x, content)
    plain_alias = filter(lambda x: 'alias' in x, content)

    h_map = {}
    all = []

    for host in plain_hosts:
        h = Host(host['host'], host['remote_path'])
        h_map[h.host] = h
        all.append(h)

    for alias in plain_alias:
        h = Alias(alias['alias'], h_map[alias['host']])
        all.append(h)

    return all


def get_db():
    from os.path import exists

    if not exists(path_file_db()):
        init_db()

    with open(path_file_db()) as handle:
        import yaml
        rows = yaml.load(handle)

    db = []
    for row in rows:
        db.append(Job(row['tag'], row['host'], row['step'], row['command'], row['start_time'], row['container']))

    return db


def save_hosts(hosts):
    '''
    [
        {host: ..., remote_path: ...}
        {alias: ..., host: ...}
    ]
    '''
    with open(path_file_hosts(), 'w') as handle:
        import yaml
        raw = [
            host.dict()
            for host in hosts
            ]
        yaml.safe_dump(raw, handle)


def save_db(db):
    with open(path_file_db(), 'w') as handle:
        import yaml
        raw = [
            each.dict()
            for each in db
        ]
        yaml.safe_dump(raw, handle)


def run_local(command, shell=False):
    import subprocess
    import sys

    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=sys.stdout, shell=shell)

    output = ''
    for line in iter(p.stdout.readline, ''):
        if not line: break
        line = line.decode('utf-8')
        output += line
        print(line, end='')

    code = p.wait()

    return (code, output)


def run_local_check(command, shell=False):
    code, out = run_local(command, shell)
    assert code == 0, 'some err occurred during the execution of cmd {}'.format(command)
    return out


def run_remote(host, path, command):
    cmd = [
        'ssh', '-T', '{host}'.format(host=host),
        '"cd {path} && {command}"'.format(path=path, command=' '.join(command))
    ]
    return run_local(' '.join(cmd), True)


def run_remote_check(host, path, command):
    code, out = run_remote(host, path, command)
    assert code == 0, 'some err occured during the execution of cmd {}'.format(command)
