import os
import base64
import time
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from github import Github

# If modifying the email service scope, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def authenticate_gmail():
    """Authenticate and return the Gmail API service"""
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)

def send_email(service, to, subject, body):
    """Send an email using Gmail API"""
    try:
        # Create the MIME message
        message = MIMEMultipart()
        message['to'] = to
        message['subject'] = subject
        msg = MIMEText(body)
        message.attach(msg)

        # Encode the message to base64url
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        # Send the email
        send_message = service.users().messages().send(userId='me', body={'raw': raw_message}).execute()
        print(f'Message sent successfully. Message ID: {send_message["id"]}')
    
    except HttpError as error:
        print(f'An error occurred: {error}')

# GitHub interaction (e.g., creating issues)
def create_github_issue():
    # Authenticate with your GitHub token
    g = Github(os.environ['GITHUB_TOKEN'])

    # Get the repository
    repo = g.get_repo("AmmarPendroy/GEG-ZAS-Contractor-Payment-System")  # Replace with your username/repository

    # Create an issue
    issue = repo.create_issue(
        title="New Payment Request",
        body="A new payment request has been submitted and needs approval."
    )

    print(f"Issue created: {issue.title}")
