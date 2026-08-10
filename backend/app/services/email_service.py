from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from fastapi import HTTPException, status

from backend.app.core.config import settings


def send_email(to_email: str, subject: str, body: str, timeout: int = 20) -> bool:
    # Prefer explicit SMTP_* settings; fall back to legacy EMAIL_* values
    host = settings.smtp_host or settings.email_host
    port = settings.smtp_port or settings.email_port
    username = settings.smtp_username or settings.email_sender
    password = settings.smtp_password or settings.email_password

    if not host or not port or not username or not password:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="SMTP configuration is incomplete. Set SMTP_HOST/SMTP_PORT/SMTP_USERNAME/SMTP_PASSWORD.",
        )

    message = MIMEMultipart()
    message["From"] = username
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        import smtplib

        smtp = smtplib.SMTP(host, port, timeout=timeout)
        smtp.starttls()
        smtp.login(username, password)
        smtp.send_message(message)
        smtp.quit()
        return True
    except Exception:
        # Do not expose credentials or internal SMTP errors to callers; return False to allow caller to record failure
        return False
