__version__ = '0.19'


def act_list(args):
    from src.actions.list import print_list
    from src import utils
    db = utils.DB.load()
    print_list(db)


def act_run_old(args):
    from src import utils
    db = utils.DB.load()

    if not args.tag:
        # provide some default tag
        args.tag = db.get_latest('tag')

    if args.tag is None:
        raise utils.errors.LatestTagNotFound(
            'There is no latest tag, we cannot make a good guess for you, please provide it explicitly')

    job = db.get_job_by_tag(args.tag)

    if args.host:
        print('Using host: {}'.format(args.host))
        job.set_using_host(args.host)
        db.save()

    if not args.docker:
        latest_docker = db.get_latest('docker')
        if not latest_docker:
            latest_docker = 'docker'
        args.docker = latest_docker

    print('Run using docker: {}'.format(args.docker))
    job.set_docker(args.docker)
    db.save()

    from src.actions import run
    run.run(job, db, run.NormalFlow)


def act_run_new(args):
    from src import utils
    db = utils.DB.load()

    if not args.tag:
        raise utils.errors.ArgumentError('Tag not provided')

    if not args.host:
        latest_host = db.get_latest('using_host')
        if not latest_host:
            raise utils.errors.LatestHostNotFound('No default (latest) host, must explicitly provide one')
        args.host = latest_host

    if not args.path:
        args.path = db.get_path_by_host(args.host)

    if not args.docker:
        latest_docker = db.get_latest('docker')
        if not latest_docker:
            latest_docker = 'docker'
        args.docker = latest_docker

    # search for existing job for duplicates

    try:
        job = db.get_job_by_tag(args.tag)
        raise utils.errors.JobDuplicate('Job duplicate with tag: {} host: {}'.format(job.tag, job.hosts))
    except utils.errors.TagNotFound:
        # no job duplicate great!
        pass

    print('Run using docker: {}'.format(args.docker))
    job = utils.Job(tag=args.tag,
                    hosts=[args.host],
                    using_host=args.host,
                    remote_path=args.path,
                    command=args.command,
                    step=None,
                    docker=args.docker)
    db.add_job(job)

    from src.actions import run
    run.run(job, db, run.NormalFlow)


def act_run(args):
    if not args.command:
        act_run_old(args)
    else:
        act_run_new(args)


def act_restart(args):
    from src.actions import restart
    from src import utils
    db = utils.DB.load()

    if not args.tag:
        # provide some default tag
        args.tag = db.get_latest('tag')

    restart.restart(args.tag, db)


def act_stop(args):
    from src.actions import stop
    from src import utils
    db = utils.DB.load()

    if not args.tag:
        # provide some default tag
        args.tag = db.get_latest('tag')

    stop.stop(args.tag, db)


def act_remove(args):
    from src.actions import remove
    from src import utils
    db = utils.DB.load()
    remove.remove(args.tag, db)


def act_ssh(args):
    from src.actions import ssh
    from src import utils
    db = utils.DB.load()

    if not args.tag:
        args.tag = db.get_latest('tag')

    job = db.get_job_by_tag(args.tag)
    host = job.using_host

    ssh.ssh(host, job.remote_path)


def act_sync(args):
    from src.actions import sync
    from src import utils

    db = utils.DB.load()

    if not args.tag:
        args.tag = db.get_latest('tag')

    job = db.get_job_by_tag(args.tag)
    host = job.using_host

    sync.sync(host, job.remote_path)


def act_sync_up(args):
    from src.actions import sync_up
    from src import utils

    db = utils.DB.load()

    if not args.tag:
        args.tag = db.get_latest('tag')

    job = db.get_job_by_tag(args.tag)
    host = job.using_host

    delete = not db.any_running()
    if not delete:
        print('Syncing up with update mode to preserve results from the other running jobs')

    sync_up.sync_up(host, job.remote_path, delete=delete)


def act_quit(signal, frame, args):
    print('Exiting ...')
    print('You can continue your work by:')
    print('$ rdocker run --tag={}'.format(args.tag))
    import sys
    sys.exit(0)


def main():
    import sys
    from src import utils

    try:
        # init ignore if not exist
        from os.path import exists

        if not exists(utils.path_file_ignore()):
            print('initiating a new .remotedignore, change it to suit your need')
            utils.init_ignore()

        from src.parser import parseargs, Actions
        args = parseargs(sys.argv[1:])

        # register signal
        import signal
        import functools
        signal.signal(signal.SIGINT, functools.partial(act_quit, args=args))

        func_map = {
            Actions.LIST: act_list,
            Actions.RUN: act_run,
            Actions.RESTART: act_restart,
            Actions.STOP: act_stop,
            Actions.REMOVE: act_remove,
            Actions.SSH: act_ssh,
            Actions.SYNC: act_sync,
            Actions.SYNC_UP: act_sync_up,
        }

        # call function
        func_map[args.action](args)
    except utils.errors.RemoteDockerError as e:
        print(e)
        sys.exit(1)


if __name__ == '__main__':
    main()
