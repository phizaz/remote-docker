def dict_to_cli_args(d):
    assert isinstance(d, dict)
    return tuple(
        '--{key}={val}'.format(key=key, val=val)
        for key, val in d.items()
    )

def run_python(file, *args, **kwargs):
    import subprocess
    import sys
    output = subprocess.check_output((sys.executable, file) + args + dict_to_cli_args(kwargs))
    return output



