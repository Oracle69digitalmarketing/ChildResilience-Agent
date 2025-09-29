async def classify(description: str, language: str) -> dict:
    """
    Replace with Bedrock/SageMaker call.
    Handles child-impact classification + multilingual response generation.
    """
    # Simulated output
    return {
        "incident_type": "flood",
        "severity_score": 0.87,
        "child_impact_tags": ["school_disruption", "health_risk"],
        "response_text": f"Detected flood risk. Evacuate children to safe shelters. ({language})"
    }
