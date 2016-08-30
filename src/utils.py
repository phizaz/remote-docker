class Files(object):
    HOSTS = '.remotedhosts'
    DB = '.remoteddb'
    IGNORE = '.remotedignore'

def path_root():
    from os.path import dirname
    return dirname(dirname(__file__))

def path_caller():
    from os import getcwd
    return getcwd()

def path_src():
    from os.path import join
    return join(path_root(), 'src')

def path_test():
    from os.path import join
    return join(path_root(), 'test')

def path_file_hosts():
    from os.path import join
    return join(path_caller(), Files.HOSTS)

def path_file_db():
    from os.path import join
    return join(path_caller(), Files.DB)

def path_file_ignore():
    from os.path import join
    return join(path_caller(), Files.IGNORE)
