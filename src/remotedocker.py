def main():
    import sys
    from src.parser import parseargs
    args = parseargs(sys.argv[1:])
    print(args)

if __name__ == '__main__':
    main()