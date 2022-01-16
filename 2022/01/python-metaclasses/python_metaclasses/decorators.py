import logging
import time

from functools import wraps

logger = logging.getLogger(__name__)


def measure_it(func):
    @wraps(func)
    def timed(*args, **kw):
        start = time.perf_counter()
        try:
            return func(*args, **kw)
        finally:
            elapsed = time.perf_counter() - start
            logger.info(f"{func.__name__} from {func.__module__} with args {args} took {elapsed:0.2f} seconds")

    return timed


def take_screenshot(func):
    @wraps(func)
    def wrapped(*args, **kw):
        result = func(*args, **kw)
        try:
            logger.info(f"Screenshot has been taken for {func.__name__}")
        except Exception as e:
            raise FailedToTakeScreenshotException
        return result

    return wrapped


class FailedToTakeScreenshotException(Exception):
    pass
