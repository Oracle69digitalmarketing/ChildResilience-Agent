# backend/app/services/auth_service.py
import time
import jwt
import boto3
from typing import Optional
from backend.app.core.config import JWT_SECRET, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, AWSREGION

dynamodb = boto3.resource("dynamodb", region_name=AWSREGION)
user_table = dynamodb.Table("ChildResilienceUsers")  # create this table

def authenticate_user(username: str, password: str) -> Optional[dict]:
    resp = user_table.get_item(Key={"username": username})
    user = resp.get("Item")
    if user and user["password"] == password:  # ⚠️ replace with hashed check
        return {"id": user["id"], "username": user["username"], "role": user["role"]}
    return None

def create_access_token(subject: dict, expires_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
    now = int(time.time())
    payload = {
        "sub": subject["id"],
        "username": subject["username"],
        "role": subject["role"],
        "iat": now,
        "exp": now + expires_minutes * 60,
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def decode_token(token: str) -> dict:
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
