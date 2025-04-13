import os
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SCOPES = ['https://www.googleapis.com/auth/gmail.send']
ADMIN_EMAIL = "ammar.muhammed@geg-construction.com"

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

def send_email(service, to, subject, body):
    try:
        message = MIMEMultipart()
        message['to'] = to
        message['subject'] = subject
        msg = MIMEText(body)
        message.attach(msg)
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        send_message = service.users().messages().send(userId='me', body={'raw': raw_message}).execute()
        print(f'Email sent. ID: {send_message["id"]}')
    except HttpError as error:
        print(f'An error occurred: {error}')

def send_login_alert(to_email, success=True):
    service = authenticate_gmail()
    status = "logged in successfully" if success else "logged out"
    subject = "🔐 Login Notification"
    body = f"User {to_email} has {status}."
    send_email(service, ADMIN_EMAIL, subject, body)
