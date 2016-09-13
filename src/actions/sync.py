def sync(host, remote_path):
    import os
    import sys
    sys.stdout.flush()

    from src.actions.lib import rsync
    command = rsync.rsync_down_command(host, remote_path)
    print('Syncing back from the remote: {host} path: {remote_path}'.format(host=host, remote_path=remote_path))
    os.execvp(command[0], command)