import time


def kronos(func):
    """
        Decorator to measure your function's execution time
    """

    def wrapper(*args, **kwargs):
        t = time.time()
        result = func(*args, **kwargs)
        # FIXME que vaya a logs con formato json
        print(f'Execution time of {func.__module__}.{func.__name__}: {1000 * (time.time() - t)} ms ')
        return result

    return wrapper


def frange(init, stop, step):
    while init < stop:
        yield init
        init += step
