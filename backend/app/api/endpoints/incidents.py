# backend/app/api/endpoints/incidents.py
from fastapi import APIRouter, Depends, HTTPException
from backend.app.models.incident import Incident
from backend.app.services.incident_service import (
    save_incident, get_incident, list_incidents,
    update_incident, delete_incident, notify_authorities
)
from backend.app.services.auth_service import decode_token

router = APIRouter(tags=["Incidents"])

def get_current_user(token: str) -> dict:
    try:
        return decode_token(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/incidents")
async def create_incident(incident: Incident, user=Depends(get_current_user)):
    if user["role"] not in ["reporter", "admin"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    await save_incident(incident)
    await notify_authorities(incident)
    return {"message": "Incident reported", "incident": incident}

@router.get("/incidents/{incident_id}")
async def read_incident(incident_id: str, user=Depends(get_current_user)):
    return await get_incident(incident_id)

@router.get("/incidents")
async def list_all_incidents(user=Depends(get_current_user)):
    if user["role"] not in ["authority", "admin"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    return await list_incidents()

@router.put("/incidents/{incident_id}")
async def update_incident_route(incident_id: str, incident: Incident, user=Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admins only")
    return await update_incident(incident_id, incident)

@router.delete("/incidents/{incident_id}")
async def delete_incident_route(incident_id: str, user=Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admins only")
    return await delete_incident(incident_id)
