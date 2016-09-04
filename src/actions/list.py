def row_of(field, l):
    return list(map(lambda x: getattr(x, field), l))

def print_list(db):
    from src import utils
    assert isinstance(db, utils.DB)

    print('----------------------------------------')
    print('latest host:', db.get_latest('using_host'), 'latest tag:', db.get_latest('tag'), 'latest docker:', db.get_latest('docker'))
    print('----------------------------------------')

    table = []
    header = ['tag', 'using_host', 'command', 'step', 'remote_path', 'time_elapsed', 'all hosts', 'docker']

    rows = zip(
        row_of('tag', db.jobs),
        row_of('using_host', db.jobs),
        row_of('command', db.jobs),
        row_of('step', db.jobs),
        row_of('remote_path', db.jobs),
        list(map(lambda x: x.time_elapsed(), db.jobs)),
        row_of('hosts', db.jobs),
        row_of('docker', db.jobs)
    )

    table.append(header)
    table += rows

    from tabulate import tabulate
    print(tabulate(table))
