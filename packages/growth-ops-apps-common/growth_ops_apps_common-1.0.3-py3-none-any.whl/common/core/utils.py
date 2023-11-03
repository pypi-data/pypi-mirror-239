from datetime import timedelta, datetime
from functools import lru_cache, wraps


def timed_lru_cache(seconds: int, maxsize: int = 128):
    def wrapper_cache(func):
        func = lru_cache(maxsize=maxsize)(func)
        func.lifetime = timedelta(seconds=seconds)
        func.expiration = datetime.utcnow() + func.lifetime

        @wraps(func)
        def wrapped_func(*args, **kwargs):
            if datetime.utcnow() >= func.expiration:
                func.cache_clear()
                func.expiration = datetime.utcnow() + func.lifetime

            return func(*args, **kwargs)

        return wrapped_func

    return wrapper_cache


def to_title_case(snake_case_string):
    # Split the string by underscores and capitalize each word
    words = snake_case_string.split('_')
    title_words = [word.capitalize() for word in words]

    # Join the words to form the title case string
    title_case_string = ''.join(title_words)

    return title_case_string
