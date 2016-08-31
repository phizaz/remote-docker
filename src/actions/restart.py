def restart(tag, db):
    from src import utils
    assert isinstance(db, utils.DB)

    job = db.get_job_by_tag(tag)

    if not job.step:
        raise Exception('the job of the given tag {} has not started yet'.format(tag))

    if job.container:
        print('Stopping and removing the running container')
        from .lib.docker import docker_rm
        docker_rm(job.using_host, job.remote_path, job.container, job.docker)
        job.container = None
        db.save()

    # set step to begin
    job.step = None
    db.save()

    print('Restarting the process')
    from .run import run, NormalFlow
    run(job, db, NormalFlow)