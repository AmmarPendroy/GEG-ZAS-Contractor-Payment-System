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
import streamlit as st

# Load the GitHub token from Streamlit secrets
GITHUB_TOKEN = st.secrets["github"]["token"]

# Gmail API authentication
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

def use_github_token():
    """Demonstration of using GitHub token"""
    print(f"GitHub Token: {GITHUB_TOKEN}")
    # You can use this token in your GitHub API calls for authorization (like pushing updates, etc.)
    # Example: Making a request to GitHub API using the token

if __name__ == '__main__':
    try:
        # Authenticate and get Gmail service
        service = authenticate_gmail()

        # Email details
        to = 'recipient@example.com'
        subject = 'Test Email'
        body = 'This is a test email sent using Gmail API with OAuth 2.0 authentication.'

        # Send the email
        send_email(service, to, subject, body)

        # Use GitHub token for GitHub-related operations
        use_github_token()

    except Exception as e:
        print(f"An error occurred: {e}")
