def restart(tag, db, force):
    assert isinstance(force, bool)
    from src import utils
    assert isinstance(db, utils.DB)

    job = db.get_job_by_tag(tag)

    if not job.step:
        print('Job of tag: {} has not started yet, will now start!'.format(tag))

    if job.container:
        print('Stopping and removing the running container')
        from .lib.docker import docker_rm
        try:
            docker_rm(job.using_host, job.remote_path, job.container, job.docker)
        except Exception:
            if not force:
                raise
            else:
                print('there is a problem on removing the container, however since you force, it will be ignored.')

        job.container = None
        db.save()

    # set step to begin
    job.step = None
    db.save()

    print('Restarting the process of tag: {}'.format(tag))
    from .run import run, NormalFlow
    run(job, db, NormalFlow)
