# backend/app/services/deps.py
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from backend.app.services.auth import decode_token

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = decode_token(token)
        return {"id": payload.get("sub"), "username": payload.get("username"), "role": payload.get("role")}
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

def require_role(role: str):
    async def role_checker(user=Depends(get_current_user)):
        if user.get("role") != role and user.get("role") != "admin":
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return role_checker
