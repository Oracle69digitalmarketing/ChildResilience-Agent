# backend/app/services/auth.py
import time
from typing import Optional
import jwt
from backend.app.core.config import JWT_SECRET, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

# Minimal demo user store. Replace with secure user store in production.
USERS = {
    "reporter1": {"id": "u-rep-1", "username": "reporter1", "password": "password", "role": "reporter"},
    "authority1": {"id": "u-auth-1", "username": "authority1", "password": "password", "role": "authority"},
    "admin": {"id": "u-admin-1", "username": "admin", "password": "password", "role": "admin"}
}

def authenticate_user(username: str, password: str) -> Optional[dict]:
    user = USERS.get(username)
    if user and user["password"] == password:
        return {"id": user["id"], "username": user["username"], "role": user["role"]}
    return None

def create_access_token(subject: dict, expires_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
    now = int(time.time())
    payload = {
        "sub": subject.get("id"),
        "username": subject.get("username"),
        "role": subject.get("role"),
        "iat": now,
        "exp": now + expires_minutes * 60
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    # PyJWT returns bytes on some versions; normalize to string
    if isinstance(token, bytes):
        token = token.decode("utf-8")
    return token

def decode_token(token: str) -> dict:
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
