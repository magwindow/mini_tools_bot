from functools import wraps
from logging import getLogger

logger = getLogger("console")


def mute_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.exception(str(e), exc_info=e)
            return []

    return wrapper
