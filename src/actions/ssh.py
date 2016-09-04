def ssh(host, path):
    import os
    import sys
    sys.stdout.flush()
    os.execvp('ssh', ['ssh', '-t', host, 'cd', path, ';', 'bash'])

