import boto3, json
from backend.app.core.config import AWSREGION

eventbridge = boto3.client("events", region_name=AWSREGION)

async def send_incident_event(incident: dict):
    import asyncio
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(
        None,
        lambda: eventbridge.put_events(
            Entries=[{
                "Source": "childresilience.agent",
                "DetailType": "IncidentReported",
                "Detail": json.dumps(incident),
                "EventBusName": "default"
            }]
        )
    )
