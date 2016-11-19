class Steps(object):
    SYNC_UP = 'SYNC_UP'
    BUILD = 'BUILD'
    RUN = 'RUN'
    BUILD_AND_RUN = 'BUILD_AND_RUN'
    LOG = 'LOG'
    REMOVE = 'REMOVE'
    LOG_AND_REMOVE = 'LOG_AND_REMOVE'
    SYNC_DOWN = 'SYNC_DOWN'


class Flow(object):
    from abc import abstractmethod

    def __init__(self, job, db):
        from src.utils import Job, DB
        assert isinstance(job, Job)
        assert isinstance(db, DB)
        self.job = job
        self.db = db

    def save(self):
        self.db.save()

    @abstractmethod
    def start(self):
        pass


class NormalFlow(Flow):
    def start(self):
        log = None

        if self.job.step == Steps.SYNC_UP or not self.job.step:
            print('(1/6) Syncing files to the remote {}'.format(self.job.using_host))
            self.sync_up()
            self.job.step = Steps.BUILD
            self.save()
        if self.job.step == Steps.BUILD:
            print('(2/6) Building the environment')
            self.build()
            self.job.step = Steps.RUN
            self.save()
        if self.job.step == Steps.RUN:
            print('(3/6) Start running the process')
            self.run()
            self.job.step = Steps.LOG
            self.save()
        if self.job.step == Steps.LOG:
            rows = 10000
            print('(4/6) Fetching logs (latest = {} lines)'.format(rows))
            log = self.log(rows=rows)
            self.job.step = Steps.REMOVE
            self.save()
        if self.job.step == Steps.REMOVE:
            print('(5/6) Removing the container')
            self.remove()
            self.job.step = Steps.SYNC_DOWN
            self.save()
        if self.job.step == Steps.SYNC_DOWN:
            print('(6/6) Syncing files back to the host (preserving newer files)')
            self.sync_down()
            self.job.step = None
            self.save()

        return log

    def sync_up(self):
        from .lib.rsync import rsync_up
        delete = not self.db.any_running()
        if not delete:
            print('Syncing up with update mode to preserve results from the other running jobs')
        rsync_up(self.job.using_host, self.job.remote_path, delete=delete)

    def build(self):
        from .lib.docker import docker_build
        docker_build(self.job.using_host,
                     self.job.remote_path,
                     self.job.tag,
                     '.',
                     docker=self.job.docker)

    def run(self):
        from .lib.docker import docker_run
        container = docker_run(self.job.using_host, self.job.remote_path, self.job.tag, '$(pwd)',
                               self.job.command,
                               docker=self.job.docker)
        self.job.container = container

    def log(self, rows):
        from .lib.docker import docker_logs_check
        return docker_logs_check(self.job.using_host, self.job.remote_path, self.job.container,
                                 docker=self.job.docker, log_rows=rows)

    def remove(self):
        from .lib.docker import docker_rm
        docker_rm(self.job.using_host, self.job.remote_path, self.job.container,
                  docker=self.job.docker)
        self.job.container = None

    def sync_down(self):
        from .lib.rsync import rsync_down
        rsync_down(self.job.using_host, self.job.remote_path)


def run(job, db, flow_cls=NormalFlow):
    assert issubclass(flow_cls, Flow), 'flow_cls must be inherited from Flow'
    # set latest job
    db.update_latest_job(job)
    # run
    flow = flow_cls(job=job, db=db)
    return flow.start()
