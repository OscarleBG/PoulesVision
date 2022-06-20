from os import mkdir


def try_mkdir(path):
    try:
        mkdir(path)
    except OSError as error:
        pass
