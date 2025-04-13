import os
import base64
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def authenticate_gmail():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def log_email_history(to_email, subject, body, status):
    email_history = []
    if os.path.exists('sent_emails.json'):
        with open('sent_emails.json', 'r') as f:
            email_history = json.load(f)
    
    email_entry = {
        "to": to_email,
        "subject": subject,
        "body": body,
        "status": status,
        "timestamp": datetime.now().isoformat()
    }
    
    email_history.append(email_entry)
    
    with open('sent_emails.json', 'w') as f:
        json.dump(email_history, f, indent=4)

def send_approval_email(to_email, contractor, amount, status):
    try:
        service = authenticate_gmail()
        subject = f"Payment Request {status}"
        body = f"""Hello,

This is to inform you that the payment request for:

Contractor: {contractor}
Amount: ${amount}
Status: {status}

has been processed.

Regards,
GEG-ZAS System
"""
        message = MIMEMultipart()
        message['to'] = to_email
        message['subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        send_message = service.users().messages().send(userId='me', body={'raw': raw}).execute()
        
        # Log the email in the history
        log_email_history(to_email, subject, body, "Sent")

        print(f'✅ Email sent: {send_message["id"]}')
    except HttpError as error:
        print(f"❌ Gmail API error: {error}")
        log_email_history(to_email, subject, body, "Failed")
