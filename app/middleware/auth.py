import os
import jwt
from fastapi import Request, HTTPException

def authenticate(request: Request):
    token = request.cookies.get("accessToken")

    if not token:
        raise HTTPException(status_code=401, detail="Missing access token")

    try:
        decoded = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256", "HS512"])
        request.state.user = {
            "id": decoded["sub"],
            "role": decoded["role"]
        }
    except:
        raise HTTPException(status_code=401, detail="Invalid or expired token")