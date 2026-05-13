from functools import wraps
import timeit
from collections.abc import Callable


def measure_time(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        result_box = {}

        def run_once():
            result_box["value"] = func(*args, **kwargs)

        elapsed = timeit.Timer(run_once).timeit(number=1)
        print(f"{func.__name__} executed in {elapsed:.4f}s")
        return result_box["value"]

    return wrapper
