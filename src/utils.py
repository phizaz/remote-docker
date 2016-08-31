class Files(object):
    HOSTS = '.remotedhosts'
    DB = '.remoteddb'
    IGNORE = '.remotedignore'


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
    copy(join(path_src(), Files.HOSTS), path_file_hosts())


def init_db():
    from shutil import copy
    from os.path import join
    copy(join(path_src(), Files.DB), path_file_db())


def get_hosts():
    from os.path import exists

    if not exists(path_file_hosts()):
        init_hosts()

    with open(path_file_hosts()) as handle:
        import yaml
        hosts = yaml.load(handle)
    return hosts


def get_db():
    from os.path import exists

    if not exists(path_file_db()):
        init_db()

    with open(path_file_db()) as handle:
        import yaml
        db = yaml.load(handle)
    return db


def save_hosts(hosts):
    with open(path_file_hosts(), 'w') as handle:
        import yaml
        yaml.safe_dump(hosts, handle)


def save_db(db):
    with open(path_file_db(), 'w') as handle:
        import yaml
        yaml.safe_dump(db, handle)


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
