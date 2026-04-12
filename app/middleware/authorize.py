from fastapi import Request, HTTPException

def authorize(request: Request, roles: list):
    if not hasattr(request.state, "user"):
        raise HTTPException(status_code=401, detail="Unauthenticated")

    if request.state.user["role"] not in roles:
        raise HTTPException(status_code=403, detail="Forbidden")