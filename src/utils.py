from . import errors


class Files(object):
    DB = '.remoteddb'
    IGNORE = '.remotedignore'


class DB(object):
    def __init__(self, latest_job, jobs):
        self.latest_job = latest_job
        self.jobs = jobs

    def add_job(self, job):
        self.jobs.append(job)
        self.save()

    def remove_job(self, job):
        assert isinstance(self.jobs, list)
        self.jobs = list(filter(lambda x: x.tag != job.tag, self.jobs))
        self.save()

    def update_latest_job(self, job):
        self.latest_job = job
        self.save()

    def get_latest(self, attr):
        if self.latest_job:
            return getattr(self.latest_job, attr, None)
        return None

    def any_running(self):
        return any(job.step is not None for job in self.jobs)

    def get_job_by_tag(self, tag):
        for job in self.jobs:
            if job.tag == tag:
                return job
        raise errors.TagNotFound('Job with tag: {} not found in the DB'.format(tag))

    def get_path_by_host(self, host):
        for job in self.jobs:
            if host in job.hosts:
                return job.remote_path
        raise errors.HostNotFound('Job with host: {} not found in the DB'.format(host))

    def dict(self):
        return {
            'latest_job': self.latest_job.dict() if self.latest_job else None,
            'jobs': [
                job.dict()
                for job in self.jobs
                ]
        }

    @classmethod
    def parse(cls, d):
        assert isinstance(d, dict)
        latest_job = d.get('latest_job', None)

        if latest_job is not None:
            latest_job = Job.parse(latest_job)

        return DB(latest_job=latest_job,
                  jobs=[
                      Job.parse(each)
                      for each in d['jobs']
                      ])

    @classmethod
    def load(cls):
        from os.path import exists
        if not exists(path_file_db()):
            db = DB(None, [])
            db.save()
            return db
        else:
            with open(path_file_db()) as handle:
                import yaml
                content = yaml.load(handle)
            return cls.parse(content)

    def save(self):
        with open(path_file_db(), 'w') as handle:
            import yaml
            yaml.safe_dump(self.dict(), handle)


class Job(object):
    def __init__(self, tag, hosts, using_host,
                 remote_path, command, step, docker='docker',
                 start_time=None, container=None, oth=None):
        assert isinstance(hosts, list)
        import arrow
        self.tag = tag
        self.hosts = hosts
        self.using_host = using_host
        self.remote_path = remote_path
        self.command = command
        self.step = step
        self.docker = docker
        if not start_time:
            self.start_time = arrow.utcnow()
        else:
            self.start_time = arrow.get(start_time)
        self.container = container
        self.oth = oth

    def set_using_host(self, host):
        if host not in self.hosts:
            self.hosts.append(host)
        self.using_host = host

    def set_docker(self, docker):
        self.docker = docker

    def dict(self):
        return {
            'tag': self.tag,
            'hosts': self.hosts,
            'using_host': self.using_host,
            'remote_path': self.remote_path,
            'command': self.command,
            'step': self.step,
            'docker': self.docker,
            'start_time': str(self.start_time),
            'container': self.container,
            'oth': self.oth
        }

    @classmethod
    def parse(cls, d):
        assert isinstance(d, dict)
        return Job(tag=d['tag'],
                   hosts=d['hosts'],
                   using_host=d['using_host'],
                   remote_path=d['remote_path'],
                   command=d['command'],
                   step=d['step'],
                   docker=d['docker'],
                   start_time=d['start_time'],
                   container=d['container'],
                   oth=d['oth'])

    def time_elapsed(self):
        return self.start_time.humanize()


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


def path_file_db():
    from os.path import join
    return join(path_caller(), Files.DB)


def path_file_ignore():
    from os.path import join
    return join(path_caller(), Files.IGNORE)


def init_db():
    db = DB(None, [])
    db.save()


def init_ignore():
    from shutil import copy
    from os.path import join
    copy(join(path_src(), 'static', Files.IGNORE), path_file_ignore())


def run_local(command):
    import subprocess
    import sys

    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=sys.stdout, bufsize=0)

    output = []
    for line in iter(p.stdout.readline, b''):
        line = line.decode('utf-8')
        output.append(line.strip())
        sys.stdout.write(line)  # also output to the screen

    code = p.wait()

    return (code, output)


def run_local_check(command):
    code, out = run_local(command)

    if code != 0:
        raise errors.WrongExitCode('Error occurred while running cmd: {} with err code: {}'.format(command, code))

    return out


def run_local_check_return_last(command):
    out = run_local_check(command)
    return out[-1]


def run_local_with_tty(command):
    from .lib.ptty import PTY
    code, out = PTY().spawn(command)
    import capturer
    out = capturer.interpret_carriage_returns(out)
    return (code, out)


def run_local_with_tty_check(command):
    try:
        code, out = run_local_with_tty(command)
    except FileNotFoundError:
        raise errors.WrongExitCode('Command Not Found occurred while running cmd: {}'.format(command))

    if code != 0:
        raise errors.WrongExitCode('Error occurred while running cmd: {} with err code: {}'.format(command, code))

    return out


def run_local_with_tty_check_return_last(command):
    out = run_local_with_tty_check(command)
    return out[-1]


def run_remote(host, path, command):
    _host, _port = resolve_host_port(host)
    cmd = [
        'ssh', '-T', '-p', _port, _host,
        'cd {path} && {command}'.format(path=path, command=' '.join(command))
    ]
    return run_local(cmd)


def run_remote_check(host, path, command):
    code, out = run_remote(host, path, command)

    if code != 0:
        raise errors.WrongExitCode(
            'Error occurred while remote running cmd: {} with error code: {}'.format(command, code))

    return out


def run_remote_check_return_last(host, path, command):
    out = run_remote_check(host, path, command)
    return out[-1]


def run_remote_with_tty_check(host, path, command):
    _host, _port = resolve_host_port(host)
    cmd = [
        'ssh', '-t', '-p', _port, _host,
        'cd {path} && {command}'.format(path=path, command=' '.join(command))
    ]
    out = run_local_with_tty_check(cmd)
    if 'Connection to' in out[-1]:
        # remove the text from ssh
        out.pop()
    return out


def run_remote_with_tty_check_return_last(host, path, command):
    out = run_remote_with_tty_check(host, path, command)
    return out[-1]


def resolve_host_port(host):
    tokens = host.split(':')
    if len(tokens) == 1:
        return tokens[0], str(22)
    else:
        return tokens[0], tokens[1]
