VERSION = (1, 2, 1)


def get_version(tail=''):
    return ".".join(map(str, VERSION)) + tail
