import smtplib
from email.message import EmailMessage

EMAIL_FROM = "your.email@geg-construction.com"
EMAIL_PASSWORD = "your_app_password"  # Use app password or secure method
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def send_email(to, subject, body):
    msg = EmailMessage()
    msg["From"] = EMAIL_FROM
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_FROM, EMAIL_PASSWORD)
            server.send_message(msg)
        print(f"Email sent to {to}")
    except Exception as e:
        print(f"Email error: {e}")
