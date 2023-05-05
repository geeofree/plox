if __name__ == "__main__":
    from src.plox import Plox
    import sys

    argc = len(sys.argv)

    if argc > 2:
        exit("{} takes in a single argument only.".format(sys.argv[0]))
    elif argc == 2:
        Plox.run(sys.argv[1])
    else:
        Plox.run_prompt()
