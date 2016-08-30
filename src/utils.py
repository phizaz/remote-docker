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
