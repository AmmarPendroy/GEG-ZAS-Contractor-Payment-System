import os
import base64
from datetime import datetime
import pandas as pd
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SCOPES = ['https://www.googleapis.com/auth/gmail.send']
ADMIN_EMAIL = "ammar.muhammed@geg-construction.com"
EMAIL_LOG_FILE = "sent_emails.csv"

def authenticate_gmail():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def log_sent_email(to_email, subject, body, status):
    timestamp = datetime.utcnow().isoformat()
    entry = {
        "timestamp": timestamp,
        "to_email": to_email,
        "subject": subject,
        "body": body,
        "status": status
    }

    try:
        df = pd.read_csv(EMAIL_LOG_FILE)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["timestamp", "to_email", "subject", "body", "status"])

    df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
    df.to_csv(EMAIL_LOG_FILE, index=False)

def send_email(service, to, subject, body):
    try:
        message = MIMEMultipart()
        message['to'] = to
        message['subject'] = subject
        msg = MIMEText(body)
        message.attach(msg)

        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        service.users().messages().send(userId='me', body={'raw': raw_message}).execute()

        log_sent_email(to, subject, body, "Sent")
        print(f"Email sent to {to}")

    except HttpError as error:
        log_sent_email(to, subject, body, "Failed")
        print(f"Error sending email to {to}: {error}")

def send_login_alert(to_email, success=True):
    service = authenticate_gmail()
    status = "logged in successfully" if success else "logged out"
    subject = "🔐 Login Notification"
    body = f"User {to_email} has {status}."
    send_email(service, ADMIN_EMAIL, subject, body)
