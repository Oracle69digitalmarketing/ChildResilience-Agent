# backend/app/services/aws_dynamodb.py
import boto3
from botocore.exceptions import ClientError
import asyncio
from backend.app.core.config import AWSREGION, DYNAMODBTABLE, SHELTER_TABLE
from backend.app.models.incident import Incident  # if used for validation
from backend.app.models.shelter import Shelter      # if used for validation

# Create boto3 resource once
_dynamodb = boto3.resource("dynamodb", region_name=AWSREGION)
_incident_table = _dynamodb.Table(DYNAMODBTABLE)
_shelter_table = _dynamodb.Table(SHELTER_TABLE)

# ----- Incident persistence -----
async def save_incident(incident: Incident):
    """
    Save incident to configured DynamoDB table.
    """
    loop = asyncio.get_event_loop()
    def _put():
        return _incident_table.put_item(Item=incident.dict())
    return await loop.run_in_executor(None, _put)

# Optional: fetch incidents for dashboard (paginated)
async def fetch_incidents(limit: int = 100):
    loop = asyncio.get_event_loop()
    def _scan():
        resp = _incident_table.scan(Limit=limit)
        return resp.get("Items", [])
    return await loop.run_in_executor(None, _scan)

# ----- Shelters: CRUD helpers -----
async def fetch_shelters(limit: int = 500):
    """
    Scan shelters table with simple pagination up to limit.
    """
    loop = asyncio.get_event_loop()
    def _scan_all():
        items = []
        resp = _shelter_table.scan(Limit=limit)
        items.extend(resp.get("Items", []))
        while "LastEvaluatedKey" in resp and len(items) < limit:
            resp = _shelter_table.scan(ExclusiveStartKey=resp["LastEvaluatedKey"], Limit=limit - len(items))
            items.extend(resp.get("Items", []))
        return items
    return await loop.run_in_executor(None, _scan_all)

async def put_shelter(item: dict):
    loop = asyncio.get_event_loop()
    def _put():
        return _shelter_table.put_item(Item=item)
    return await loop.run_in_executor(None, _put)

async def fetch_shelter_by_id(shelter_id: str):
    loop = asyncio.get_event_loop()
    def _get():
        resp = _shelter_table.get_item(Key={"id": shelter_id})
        return resp.get("Item")
    return await loop.run_in_executor(None, _get)

async def update_shelter(shelter_id: str, item: dict):
    # Overwrite pattern (simple). For partial updates, use UpdateExpression.
    item["id"] = shelter_id
    return await put_shelter(item)

async def delete_shelter(shelter_id: str):
    loop = asyncio.get_event_loop()
    def _delete():
        return _shelter_table.delete_item(Key={"id": shelter_id})
    return await loop.run_in_executor(None, _delete)
