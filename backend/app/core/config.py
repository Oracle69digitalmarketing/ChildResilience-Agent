import os
from dotenv import load_dotenv
load_dotenv()

AWSREGION = os.getenv("AWSREGION", "us-east-1")
DYNAMODBTABLE = os.getenv("DYNAMODBTABLE", "ChildResilienceIncidents")
S3BUCKET = os.getenv("S3BUCKET", "childresilience-agent-files")
SNS_TOPIC_ARN = os.getenv("SNS_TOPIC_ARN")

# Twilio credentials
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM", "whatsapp:+14155238886")

# Email SMTP
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.example.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_FROM = os.getenv("EMAIL_FROM", "ChildResilience-Agent <no-reply@example.com>")
