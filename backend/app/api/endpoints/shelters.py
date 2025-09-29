# backend/app/api/endpoints/shelters.py
from fastapi import APIRouter, HTTPException
from backend.app.services.aws_dynamodb import fetch_shelters

router = APIRouter()

@router.get("/shelters")
async def get_shelters(limit: int = 500):
    try:
        items = await fetch_shelters(limit=limit)
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
