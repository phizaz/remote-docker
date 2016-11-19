def sync_up(host, remote_path, delete):
    import os
    import sys
    sys.stdout.flush()

    from src.actions.lib import rsync

    command = rsync.rsync_up_command(host, remote_path, delete=delete)
    print('Syncing back from the remote: {host} path: {remote_path} delete: {delete}'.format(host=host,
                                                                                             remote_path=remote_path,
                                                                                             delete=delete))
    os.execvp(command[0], command)
