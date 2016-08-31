def act_list(args):
    from src.actions.list import print_list
    from src import utils
    db = utils.DB.load()
    print_list(db)


def act_run_old(args):
    from src import utils
    db = utils.DB.load()
    job = db.get_job_by_tag(args.tag)

    if args.host:
        job.set_using_host(args.host)

    from .actions import run
    run.run(job, db, run.NormalFlow)


def act_run_new(args):
    from src import utils
    db = utils.DB.load()

    if not args.host:
        if not db.latest_host:
            raise Exception('no default (latest) host, must explicitly provide one')
        args.host = db.latest_host

    if not args.path:
        args.path = db.get_path_by_host(args.host)

    # search for existing job for duplicates

    try:
        job = db.get_job_by_tag(args.tag)
        raise Exception('job duplicate with tag: {} host: {}'.format(job.tag, job.hosts))
    except ValueError:
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

    from .actions import run
    run.run(job, db, run.NormalFlow)


def act_run(args):
    if not args.command:
        act_run_old(args)
    else:
        act_run_new(args)


def act_restart(args):
    from .actions import restart
    from src import utils
    db = utils.DB.load()
    restart.restart(args.tag, db)


def act_stop(args):
    from .actions import stop
    from src import utils
    db = utils.DB.load()
    stop.stop(args.tag, db)


def act_remove(args):
    from .actions import remove
    from src import utils
    db = utils.DB.load()
    remove.remove(args.tag, db)


def main():
    import sys
    from src.parser import parseargs, Actions
    args = parseargs(sys.argv[1:])
    print(args)

    func_map = {
        Actions.LIST: act_list,
        Actions.RUN: act_run,
        Actions.RESTART: act_restart,
        Actions.STOP: act_stop,
        Actions.REMOVE: act_remove,
    }

    # call function
    func_map[args.action](args)


if __name__ == '__main__':
    main()
