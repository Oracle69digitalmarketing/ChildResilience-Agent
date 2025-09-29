# backend/app/services/incident_service.py
import boto3
import asyncio
from backend.app.models.incident import Incident
from backend.app.core.config import DYNAMODBTABLE, AWSREGION, SNS_TOPIC_ARN
from backend.app.services.notification_service import send_whatsapp, send_email

dynamodb = boto3.resource("dynamodb", region_name=AWSREGION)
table = dynamodb.Table(DYNAMODBTABLE)

async def save_incident(incident: Incident):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, lambda: table.put_item(Item=incident.dict()))

async def get_incident(incident_id: str):
    loop = asyncio.get_event_loop()
    resp = await loop.run_in_executor(None, lambda: table.get_item(Key={"id": incident_id}))
    return resp.get("Item")

async def list_incidents():
    loop = asyncio.get_event_loop()
    resp = await loop.run_in_executor(None, table.scan)
    return resp.get("Items", [])

async def update_incident(incident_id: str, incident: Incident):
    incident.id = incident_id
    await save_incident(incident)
    return {"message": "Incident updated", "incident": incident}

async def delete_incident(incident_id: str):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, lambda: table.delete_item(Key={"id": incident_id}))
    return {"message": "Incident deleted"}

async def notify_authorities(incident: Incident):
    # WhatsApp
    await send_whatsapp(f"🚨 New incident reported:\n{incident.description}")
    # Email
    await send_email(
        subject="🚨 Child Resilience Incident Alert",
        body=f"Incident details:\n{incident.json()}",
        to="authority@example.com"
    )
    return {"notified": True}
