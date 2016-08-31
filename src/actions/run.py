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
        if self.job.step == Steps.SYNC_UP or not self.job.step:
            print('(1/6)')
            self.sync_up()
            self.job.step = Steps.BUILD
            self.save()
        if self.job.step == Steps.BUILD:
            print('(2/6)')
            self.build()
            self.job.step = Steps.RUN
            self.save()
        if self.job.step == Steps.RUN:
            print('3/6')
            self.run()
            self.job.step = Steps.LOG
            self.save()
        if self.job.step == Steps.LOG:
            print('4/6')
            self.log()
            self.job.step = Steps.REMOVE
            self.save()
        if self.job.step == Steps.REMOVE:
            print('5/6')
            self.remove()
            self.job.step = Steps.SYNC_DOWN
            self.save()
        if self.job.step == Steps.SYNC_DOWN:
            print('6/6')
            self.sync_down()
            self.job.step = None
            self.save()

    def sync_up(self):
        from .lib.rsync import rsync_up
        rsync_up(self.job.using_host, self.job.remote_path)

    def build(self):
        from .lib.docker import docker_build
        docker_build(self.job.using_host,
                     self.job.remote_path,
                     self.job.tag,
                     '.')

    def run(self):
        from .lib.docker import docker_run
        container = docker_run(self.job.using_host, '$(pwd)', self.job.tag, self.job.remote_path,
                               self.job.command)
        self.job.container = container

    def log(self):
        from .lib.docker import docker_logs_check
        docker_logs_check(self.job.using_host, self.job.remote_path, self.job.container)

    def remove(self):
        from .lib.docker import docker_rm
        docker_rm(self.job.using_host, self.job.remote_path, self.job.container)
        self.job.container = None

    def sync_down(self):
        from .lib.rsync import rsync_down
        rsync_down(self.job.using_host, self.job.remote_path)


def run(job, db, flow_cls=NormalFlow):
    assert issubclass(flow_cls, Flow), 'flow_cls must be inherited from Flow'
    flow = flow_cls(job=job, db=db)
    flow.start()
