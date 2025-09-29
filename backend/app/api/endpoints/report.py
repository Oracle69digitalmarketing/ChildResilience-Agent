from fastapi import APIRouter, UploadFile, Form, HTTPException
from backend.app.models.incident import Incident
from backend.app.services import (
    aws_s3, aws_dynamodb, llm_pipeline,
    aws_eventbridge, notifications, realtime_dashboard
)

router = APIRouter()

@router.post("/report")
async def submit_incident(
    reporter_name: str = Form(...),
    location: str = Form(...),
    description: str = Form(...),
    language: str = Form("en"),
    file: UploadFile = None
):
    try:
        file_url = await aws_s3.upload_file(file) if file else None
        classification = await llm_pipeline.classify(description, language)

        incident = Incident(
            reporter_name=reporter_name,
            location=location,
            description=description,
            language=language,
            file_url=file_url,
            classification=classification,
            child_impact_tags=classification.get("child_impact_tags", []),
            severity_score=classification.get("severity_score", 0.0),
            response_text=classification.get("response_text", ""),
            equity_priority_score=0.0  # optional dynamic scoring
        )

        await aws_dynamodb.save_incident(incident)
        await aws_eventbridge.send_incident_event(incident.dict())
        await notifications.notify_authorities(
            f"New child-impact incident: {incident.description}",
            phone_numbers=["+2348012345678", "+2348098765432"]
        )
        await realtime_dashboard.broadcast_incident(incident.dict())

        return {"status": "success", "incident_id": incident.id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
