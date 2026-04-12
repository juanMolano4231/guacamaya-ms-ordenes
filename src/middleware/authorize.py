from functools import wraps
from flask import jsonify, g

def authorize(roles=[]):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if "user" not in g:
                return jsonify({"message": "Unauthenticated"}), 401

            if g.user["role"] not in roles:
                return jsonify({"message": "Forbidden"}), 403

            return f(*args, **kwargs)
        return wrapper
    return decorator