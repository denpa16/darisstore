import logging
import time
from functools import wraps


def task_logging(func):
    """
    Логер задач
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        logging.info(f"Started: {func.__name__}")
        result = func(*args, **kwargs)
        logging.info(f"Success: {func.__name__}")
        logging.info(
            f"time:{time.perf_counter() - start_time} s.",
        )
        return result

    return wrapper


def retry(exception: Exception, tries: int, delay: float, backoff: int, logger):
    """
    Декоратор для повторения запросов

    """

    def decorator_retry(func):
        @wraps(func)
        def func_retry(*args, **kwargs):
            func_tries, func_delay = tries, delay
            while func_tries > 1:
                try:
                    return func(*args, **kwargs)
                except exception:
                    msg = f"{exception}, Retrying in {func_delay} seconds"
                    logger.warning(msg)
                    time.sleep(func_delay)
                    func_tries -= 1
                    func_delay *= backoff
            return func(*args, **kwargs)

        return func_retry  # true decorator

    return decorator_retry
