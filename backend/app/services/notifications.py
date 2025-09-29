import boto3
import asyncio
import smtplib
from email.message import EmailMessage
from backend.app.core.config import AWSREGION, SNS_TOPIC_ARN

# AWS SNS
sns = boto3.client("sns", region_name=AWSREGION)

# Twilio
from twilio.rest import Client
TWILIO_ACCOUNT_SID = "your_twilio_sid"
TWILIO_AUTH_TOKEN = "your_twilio_auth_token"
TWILIO_WHATSAPP_FROM = "whatsapp:+14155238886"  # Twilio Sandbox
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Email
EMAIL_HOST = "smtp.example.com"
EMAIL_PORT = 587
EMAIL_USERNAME = "your_email@example.com"
EMAIL_PASSWORD = "your_email_password"
EMAIL_FROM = "ChildResilience-Agent <your_email@example.com>"

async def notify_authorities(message: str, phone_numbers: list = [], whatsapp_numbers: list = [], emails: list = []):
    """
    Send notifications via SMS (AWS SNS), WhatsApp (Twilio), and Email (SMTP)
    """
    loop = asyncio.get_event_loop()

    # --- SMS via AWS SNS ---
    async def send_sms(number):
        await loop.run_in_executor(None, lambda: sns.publish(
            PhoneNumber=number,
            Message=message
        ))

    # --- WhatsApp via Twilio ---
    async def send_whatsapp(number):
        await loop.run_in_executor(None, lambda: twilio_client.messages.create(
            from_=TWILIO_WHATSAPP_FROM,
            to=f"whatsapp:{number}",
            body=message
        ))

    # --- Email via SMTP ---
    async def send_email(to_email):
        def _send():
            msg = EmailMessage()
            msg.set_content(message)
            msg["Subject"] = "ChildResilience Incident Alert"
            msg["From"] = EMAIL_FROM
            msg["To"] = to_email
            with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
                server.starttls()
                server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
                server.send_message(msg)
        await loop.run_in_executor(None, _send)

    tasks = []
    tasks += [send_sms(num) for num in phone_numbers]
    tasks += [send_whatsapp(num) for num in whatsapp_numbers]
    tasks += [send_email(email) for email in emails]

    await asyncio.gather(*tasks)
