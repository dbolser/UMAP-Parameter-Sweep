from time import time
from functools import wraps

import logging

logging.basicConfig(level=logging.INFO)


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)
        end = time()
        logging.info(f"Elapsed time: {end - start:.2f} sec")

        return result

    return wrapper
