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

    def __init__(self, host, remote_path, command, job):
        from src.utils import Job
        assert isinstance(job, Job)
        self.host = host
        self.remote_path = remote_path
        self.command = command
        self.job = job

    @abstractmethod
    def start(self):
        pass


class NormalFlow(Flow):
    def start(self):
        if self.job.step == Steps.SYNC_UP or not self.job.step:
            self.job.step = Steps.SYNC_UP
            self.sync_up()
            self.job.step = Steps.BUILD
        if self.job.step == Steps.BUILD:
            self.build()
            self.job.step = Steps.RUN
        if self.job.step == Steps.RUN:
            self.run()
            self.job.step = Steps.LOG
        if self.job.step == Steps.LOG:
            self.log()
            self.job.step = Steps.REMOVE
        if self.job.step == Steps.REMOVE:
            self.remove()
            self.job.step = Steps.SYNC_DOWN
        if self.job.step == Steps.SYNC_DOWN:
            self.sync_down()
            self.job.step = None

    def sync_up(self):
        pass

    def build(self):
        pass

    def run(self):
        pass

    def log(self):
        pass

    def remove(self):
        pass

    def sync_down(self):
        pass


def run(tag, host, remote_path, command):
    pass
