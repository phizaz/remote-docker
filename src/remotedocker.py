def act_list(args):
    pass

def act_set_default_host(args):
    pass

def act_new_host(args):
    pass

def act_new_alias(args):
    pass

def act_run(args):
    pass

def main():
    import sys
    from src.parser import parseargs, Actions
    args = parseargs(sys.argv[1:])
    print(args)

    func_map = {
        Actions.LIST: act_list,
        Actions.DEFAULT: act_set_default_host,
        Actions.NEW_HOST: act_new_host,
        Actions.NEW_ALIAS: act_new_alias,
        Actions.RUN: act_run
    }

    # call function 
    func_map[args.action](args)

if __name__ == '__main__':
    main()