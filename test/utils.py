def dict_to_cli_args(d):
    assert isinstance(d, dict)
    return tuple(
        '--{key}={val}'.format(key=key, val=val)
        for key, val in d.items()
    )


def run_python(file, *args, **kwargs):
    import sys
    return run_local_check((sys.executable, file) + dict_to_cli_args(kwargs) + args)


def run_local(command):
    import subprocess
    import sys

    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=sys.stdout)

    output = ''
    for line in iter(p.stdout.readline, ''):
        if not line: break
        line = line.decode('utf-8')
        output += line
        print(line, end='')

    code = p.wait()

    return (code, output)


def run_local_check(command):
    print('running:', command)
    code, out = run_local(command)
    assert code == 0, 'some err occurred during the execution of cmd {}'.format(command)
    return out
