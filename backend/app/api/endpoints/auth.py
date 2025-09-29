from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.app.services.auth import authenticate_user, create_access_token

router = APIRouter()

class LoginIn(BaseModel):
    username: str
    password: str

@router.post("/login")
async def login(payload: LoginIn):
    user = authenticate_user(payload.username, payload.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(user)
    return {"access_token": token, "token_type": "bearer", "user": user}
