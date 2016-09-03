__version__ = '0.7'


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
        args.tag = db.latest_tag

    if args.tag is None:
        raise utils.errors.LatestTagNotFound(
            'There is no latest tag, we cannot make a good guess for you, please provide it explicitly')

    job = db.get_job_by_tag(args.tag)

    if args.host:
        print('Using host: {}'.format(args.host))
        job.set_using_host(args.host)
        db.save()

    if args.docker:
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
        if not db.latest_host:
            raise utils.errors.LatestHostNotFound('No default (latest) host, must explicitly provide one')
        args.host = db.latest_host

    if not args.path:
        args.path = db.get_path_by_host(args.host)

    # search for existing job for duplicates

    try:
        job = db.get_job_by_tag(args.tag)
        raise utils.errors.JobDuplicate('Job duplicate with tag: {} host: {}'.format(job.tag, job.hosts))
    except utils.errors.TagNotFound:
        # no job duplicate great!
        pass

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
    restart.restart(args.tag, db)


def act_stop(args):
    from src.actions import stop
    from src import utils
    db = utils.DB.load()
    stop.stop(args.tag, db)


def act_remove(args):
    from src.actions import remove
    from src import utils
    db = utils.DB.load()
    remove.remove(args.tag, db)


def act_quit(signal, frame, args):
    print('Exiting ...')
    print('You can continue your work by:')
    print('$ rdocker run --tag={}'.format(args.tag))
    import sys
    sys.exit(0)


def main():
    # init ignore if not exist
    from os.path import exists
    from src import utils

    if not exists(utils.path_file_ignore()):
        print('initiating a new .remotedignore, change it to suit your need')
        utils.init_ignore()

    import sys
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
    }

    # call function
    try:
        func_map[args.action](args)
    except utils.errors.RemoteDockerError as e:
        print(e)
        sys.exit(1)


if __name__ == '__main__':
    main()
