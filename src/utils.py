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


def run_global(host, path, command):
    cmd = [
        'ssh', '-T', '{host}'.format(host=host),
        '"cd {path} && {command}"'.format(path=path, command=' '.join(command))
    ]
    return run_local(' '.join(cmd), True)


def run_global_check(host, path, command):
    code, out = run_global(host, path, command)
    assert code == 0, 'some err occured during the execution of cmd {}'.format(command)
