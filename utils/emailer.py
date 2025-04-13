import os
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Gmail API scope
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def authenticate_gmail():
    """Authenticate and return Gmail service."""
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
    """Send a basic email using Gmail API."""
    try:
        message = MIMEMultipart()
        message['to'] = to
        message['subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        send_message = service.users().messages().send(userId='me', body={'raw': raw_message}).execute()
        print(f"📧 Email sent to {to}. Message ID: {send_message['id']}")
    except Exception as e:
        print(f"❌ Email sending failed: {e}")

def send_approval_request_email(username, email, role, password):
    """Send a registration request to the super admin."""
    service = authenticate_gmail()
    subject = "🆕 New User Registration Request"
    body = f"""
Hello Super Admin,

A new user has requested access to the GEG-ZAS Payment System:

👤 Name: {username}
📧 Email: {email}
🛠️ Role: {role}

Temporary Password: {password}

Please log in to the system to approve or reject this user.

Regards,  
GEG-ZAS System
"""
    send_email(service, "ammar.muhammed@geg-construction.com", subject, body)
