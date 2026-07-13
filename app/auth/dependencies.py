import os
from fastapi import Header, HTTPException
from jose import jwt, JWTError

JWT_SECRET = os.environ.get("JWT_SECRET")

async def get_current_professor(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    token = authorization.replace("Bearer", "")

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")