from flask import request


def get_safe_max_id(v):
    if not v:
        return None

    try:
        rv = int(v)
        if rv <= 0:
            return None

    except ValueError:
        rv = None

    return rv


def get_safe_count(v, default=10, max=100):
    if not v:
        return default

    try:
        rv = int(v)
        if not (1 <= rv <= max):
            rv = default
    except ValueError:
        rv = default

    return rv