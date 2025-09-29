import boto3
from backend.app.models.incident import Incident
from backend.app.core.config import DYNAMODBTABLE

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(DYNAMODBTABLE)

async def save_incident(incident: Incident):
    import asyncio
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(
        None,
        lambda: table.put_item(Item=incident.dict())
    )
