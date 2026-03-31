from functools import wraps


def login_decorator(endpoint):
    @wraps(endpoint)
    def wrapper(*args, **kwargs):
        return endpoint(*args, **kwargs)
    return wrapper