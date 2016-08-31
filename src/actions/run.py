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
        from src.utils import Job
        assert isinstance(job, Job)
        assert job in db
        self.job = job
        self._db = db

    def save(self):
        from src.utils import save_db
        save_db(self._db)

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

def run_job(job, db, flow_cls):
    flow = flow_cls(job=job, db=db)
    flow.start()

def run(tag, db, flow_cls):
    assert issubclass(flow_cls, Flow), 'flow_cls must be inherited from Flow'
    assert isinstance(db, list)
    job = None

    for each in db:
        if each.tag == tag:
            job = each
            break

    run_job(job, db, flow_cls)

