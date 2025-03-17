import functools
import time


def log(func):
    @functools.wraps(func)
    def write(*args, **kwargs):
        local = time.ctime(time.time())

        with open('log/log.txt', 'r') as f:
            full = f.read()
        full += f'{local}: Start "{func.__name__}" with {args, kwargs}\n'

        with open('log/log.txt', 'w') as ff:
            ff.write(full)
        return func(*args, **kwargs)
    return write
