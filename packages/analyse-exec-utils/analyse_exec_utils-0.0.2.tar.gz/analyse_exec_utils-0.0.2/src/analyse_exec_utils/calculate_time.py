from time import time


def calculate_time(func):
    """Decorator used to calculate execution time of a method"""

    def inner_func(*args, **kwargs):
        start_time = time()
        result = func(*args, **kwargs)
        end_time = time()
        print("Time taken", end_time - start_time)
        return result

    return inner_func
