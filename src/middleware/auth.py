import os
import jwt
from functools import wraps
from flask import request, jsonify, g

def authenticate(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.cookies.get("accessToken")

        if not token:
            return jsonify({"message": "Missing access token"}), 401

        try:
            decoded = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256", "HS512"])
            g.user = {
                "id": decoded["sub"],
                "role": decoded["role"]
            }
        except:
            return jsonify({"message": "Invalid or expired token"}), 401

        return f(*args, **kwargs)
    return wrapper