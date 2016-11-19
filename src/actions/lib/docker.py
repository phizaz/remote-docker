def docker_build_command(image_tag, path, docker='docker'):
    command = [
        docker, 'build', '-t', image_tag, path
    ]
    return command


def docker_build(host, remote_path, image_tag, path, docker='docker'):
    from src import utils
    command = docker_build_command(image_tag, path, docker)
    out = utils.run_remote_with_tty_check_return_last(host, remote_path, command)
    return out


def docker_run_command(image_tag, mount_path, command, docker='docker'):
    mounting = '-v {}:{}'.format(mount_path, '/run')
    _command = [
        docker, 'run']
    if mount_path:
        _command.append(mounting)
    _command += [
                    '-d', '-w', '/run', image_tag
                ] + command
    return _command


def docker_run(host, remote_path, image_tag, mount_path, command, docker='docker'):
    command = docker_run_command(image_tag, mount_path, command, docker)
    from src import utils
    out = utils.run_remote_with_tty_check_return_last(host, remote_path, command)
    container = out.strip()
    return container


def docker_logs_command(container, docker='docker', log_rows='all'):
    command = [
        docker, 'logs', '-f', '--tail={}'.format(log_rows), container
    ]
    return command


def docker_logs(host, remote_path, container, docker='docker', log_rows='all'):
    command = docker_logs_command(container, docker=docker, log_rows=log_rows)
    from src import utils
    out = utils.run_remote_with_tty_check_return_last(host, remote_path, command)
    return out


def docker_logs_check(host, remote_path, container, docker='docker', log_rows='all'):
    out = docker_logs(host, remote_path, container, docker=docker, log_rows=log_rows)
    exit_code = docker_exit_code(host, remote_path, container, docker=docker)

    if exit_code != 0:
        from src import utils
        raise utils.errors.WrongDockerExitcode(
            'Some error occurred in the docker container: {} with error code: {}'.format(
                container, exit_code))

    return out


def docker_exit_code_command(container, docker='docker'):
    command = [
        docker, 'inspect', '-f', '{{.State.ExitCode}}', container
    ]
    return command


def docker_exit_code(host, remote_path, container, docker='docker'):
    command = docker_exit_code_command(container, docker)
    from src import utils
    out = utils.run_remote_with_tty_check_return_last(host, remote_path, command)
    return int(out)


def docker_rm_command(container, docker='docker'):
    command = [
        docker, 'rm', '-f', container
    ]
    return command


def docker_rm(host, remote_path, container, docker='docker'):
    command = docker_rm_command(container, docker)
    from src import utils
    utils.run_remote_with_tty_check_return_last(host, remote_path, command)
    return container
