from functools import wraps
import logging
import time

import torch


def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        time_delta_ms = (end - start) * 1000
        logging.debug(f"@_timeit: {func.__name__} took {time_delta_ms:.2f} ms")
        return result

    return wrapper


def init_cuda(device_id, torch_seed=0):
    torch.random.manual_seed(torch_seed)

    if torch.cuda.is_available():
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
        if device_id == "cpu":
            logging.warning("Running on CPU, despite CUDA being available!")
    else:
        if device_id != "cpu":
            logging.warning("CUDA not available, falling back to CPU")
        device_id = "cpu"
    device = torch.device(device_id)

    return device


class Singleton:
    """
    A non-thread-safe helper class to ease implementing singletons.
    This should be used as a decorator -- not a metaclass -- to the
    class that should be a singleton.

    The decorated class can define one `__init__` function that
    takes only the `self` argument. Also, the decorated class cannot be
    inherited from. Other than that, there are no restrictions that apply
    to the decorated class.

    To get the singleton instance, use the `instance` method. Trying
    to use `__call__` will result in a `TypeError` being raised.

    """

    def __init__(self, decorated):
        self._decorated = decorated

    def instance(self):
        """
        Returns the singleton instance. Upon its first call, it creates a
        new instance of the decorated class and calls its `__init__` method.
        On all subsequent calls, the already created instance is returned.

        """
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated()
            return self._instance

    def __call__(self):
        raise TypeError("Singletons must be accessed through `instance()`.")

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)


def unify_string(string: str) -> str:
    """
    Unify a string by replacing whitespace with underscores and converting to lowercase.
    """

    return string.replace(" ", "_").lower()
