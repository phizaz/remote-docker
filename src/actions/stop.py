def stop(tag, db):
    from src import utils
    assert isinstance(db, utils.DB)

    job = db.get_job_by_tag(tag)

    if not job.step:
        raise utils.errors.JobNotStarted('Job of tag: {} has not started yet'.format(tag))

    if job.container:
        print('Stopping and removing the running container')
        from .lib.docker import docker_rm
        docker_rm(job.using_host, job.remote_path, job.container, job.docker)
        job.container = None
        db.save()

    # reset the job
    print('Resetting the job tag: {}'.format(tag))
    job.step = None
    db.save()
