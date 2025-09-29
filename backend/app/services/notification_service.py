# backend/app/services/notification_service.py
from backend.app.core.config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_FROM
from backend.app.core.config import EMAIL_HOST, EMAIL_PORT, EMAIL_USERNAME, EMAIL_PASSWORD, EMAIL_FROM
from twilio.rest import Client
import smtplib
from email.mime.text import MIMEText

async def send_whatsapp(message: str, to="whatsapp:+2348000000000"):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    client.messages.create(
        body=message,
        from_=TWILIO_WHATSAPP_FROM,
        to=to
    )

async def send_email(subject: str, body: str, to: str):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_FROM
    msg["To"] = to

    with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
        server.starttls()
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        server.sendmail(EMAIL_FROM, [to], msg.as_string())
