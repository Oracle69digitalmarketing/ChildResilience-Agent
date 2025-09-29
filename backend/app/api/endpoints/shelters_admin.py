from fastapi import APIRouter, Depends, HTTPException
from backend.app.models.shelter import Shelter
from backend.app.services.aws_dynamodb import put_shelter, update_shelter, delete_shelter, fetch_shelter_by_id
from backend.app.services.deps import require_role

router = APIRouter()

@router.post("/shelters", dependencies=[Depends(require_role("authority"))])
async def create_shelter(payload: Shelter):
    try:
        await put_shelter(payload.dict())
        return {"status": "created", "id": payload.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/shelters/{shelter_id}", dependencies=[Depends(require_role("authority"))])
async def modify_shelter(shelter_id: str, payload: Shelter):
    try:
        existing = await fetch_shelter_by_id(shelter_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Shelter not found")
        await update_shelter(shelter_id, payload.dict())
        return {"status": "updated", "id": shelter_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/shelters/{shelter_id}", dependencies=[Depends(require_role("authority"))])
async def remove_shelter(shelter_id: str):
    try:
        await delete_shelter(shelter_id)
        return {"status": "deleted", "id": shelter_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
