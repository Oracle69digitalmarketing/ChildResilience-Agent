# ChildResilience-Agent

**AI-Powered Child-Centered Climate Resilience Platform**

ChildResilience-Agent enables real-time reporting, classification, and routing of climate-related incidents affecting children. Built for low-resource environments, it supports multilingual input, offline-first reporting, and real-time dashboards. Ideal for UNICEF-aligned pilots and scalable deployments.

---

## Features

- **Incident Classification**: AI-powered tagging of child-impact, severity scoring, and risk type.
- **Multilingual Support**: English, Hausa, Yoruba, Igbo, Swahili, Hindi, and more.
- **Multi-Modal Reporting**: Text, image, voice inputs processed via AI.
- **Event-Driven Alerts**: Route incidents to authorities, NGOs, and volunteers.
- **Real-Time Dashboard**: WebSocket-powered updates for public and internal monitoring.
- **AWS-Integrated**: S3, DynamoDB, Lambda, EventBridge, SNS, Rekognition, Textract.
- **Equity & Safety Layer**: Prioritize underserved areas, flag child-related incidents.

---

## Tech Stack

- **Backend**: FastAPI (async)
- **Frontend**: React + Vite (offline-first)
- **AI Services**: Amazon Bedrock / SageMaker, Rekognition, Textract
- **Database**: DynamoDB
- **Notifications**: SNS / Twilio
- **Serverless Events**: Lambda, EventBridge
- **Storage**: S3
- **Monitoring**: CloudWatch

---

## Installation (Backend)

```bash
git clone https://github.com/Oracle69digitalmarketing/ChildResilience-Agent.git
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000


---

Environment Variables

Variable	Description	Default

AWSREGION	AWS region	us-east-1
DYNAMODBTABLE	DynamoDB table name	ChildResilienceIncidents
S3BUCKET	S3 bucket for incident files	childresilience-agent-files
SNS_TOPIC_ARN	SNS topic for notifications	-



---

Folder Structure

backend/
├─ app/
│  ├─ api/
│  ├─ core/
│  ├─ models/
│  ├─ services/
│  ├─ utils/
│  └─ tests/
├─ requirements.txt
└─ main.py


---

Usage

1. Submit Incident: /api/report endpoint (text, image, voice)


2. AI Classification: Automatically tags child impact and severity


3. Event Routing: Alerts authorities via SMS/WhatsApp/Email


4. Real-Time Dashboard: Live incident map via WebSocket


5. Data Storage: DynamoDB + S3 for structured and unstructured assets




---

Contributing

Open-source and UNICEF-aligned

PRs welcome for language packs, AI improvements, or dashboard enhancements

Follow PEP8 and FastAPI async best practices



---

License

MIT License
