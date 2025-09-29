import boto3
from uuid import uuid4
from backend.app.core.config import S3BUCKET

s3 = boto3.client("s3")

async def upload_file(file):
    import asyncio
    loop = asyncio.get_event_loop()
    file_key = f"{uuid4()}_{file.filename}"
    await loop.run_in_executor(
        None,
        lambda: s3.upload_fileobj(file.file, S3BUCKET, file_key)
    )
    return f"https://{S3BUCKET}.s3.amazonaws.com/{file_key}"
