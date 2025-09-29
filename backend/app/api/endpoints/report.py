from fastapi import APIRouter, UploadFile, Form, HTTPException
from backend.app.models.incident import Incident
from backend.app.services import (
    aws_s3,
    aws_dynamodb,
    aws_eventbridge,
    notifications,
    llm_pipeline,
    realtime_dashboard,
    ai_media
)
from backend.app.utils.language_support import translate_text

router = APIRouter()

@router.post("/report")
async def submit_incident(
    reporter_name: str = Form(...),
    location: str = Form(...),
    description: str = Form(...),
    language: str = Form("en"),
    file: UploadFile = None,
    phone_numbers: list[str] = Form([]),
    whatsapp_numbers: list[str] = Form([]),
    emails: list[str] = Form([])
):
    try:
        # --- Upload file to S3 ---
        file_url = await aws_s3.upload_file(file) if file else None

        # --- Analyze with LLM ---
        classification = await llm_pipeline.classify(description, language)

        # --- AI Media Analysis ---
        if file_url:
            media_analysis = await ai_media.analyze_image(file_url)
            classification["media_analysis"] = media_analysis

        # --- Translate response to user language ---
        response_text = classification.get("response_text", "")
        if language != "en":
            response_text = await translate_text(response_text, language)

        # --- Construct Incident Object ---
        incident = Incident(
            reporter_name=reporter_name,
            location=location,
            description=description,
            language=language,
            file_url=file_url,
            classification=classification,
            child_impact_tags=classification.get("childimpacttags", []),
            severity_score=classification.get("severity_score", 0.0),
            response_text=response_text
        )

        # --- Save to DynamoDB ---
        await aws_dynamodb.save_incident(incident)

        # --- Notify Authorities ---
        if phone_numbers or whatsapp_numbers or emails:
            await notifications.notify_authorities(
                message=response_text,
                phone_numbers=phone_numbers,
                whatsapp_numbers=whatsapp_numbers,
                emails=emails
            )

        # --- EventBridge Trigger ---
        await aws_eventbridge.trigger_event("IncidentReported", incident.dict())

        # --- Broadcast to Real-time Dashboard ---
        await realtime_dashboard.broadcast({
            "type": "new_incident",
            "data": incident.dict()
        })

        return {"status": "success", "incident_id": incident.id, "response_text": response_text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
