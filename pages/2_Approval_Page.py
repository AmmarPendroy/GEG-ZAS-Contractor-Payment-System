import streamlit as st
from db import load_payments, save_payments
from utils.emailer import send_email
from datetime import datetime
import os
from github import Github

# Load the GitHub token from Streamlit secrets
GITHUB_TOKEN = st.secrets["github"]["token"]

# Function to add dummy payment
def add_dummy_payment():
    dummy_payment = {
        "contractor": "Test Contractor Inc.",
        "amount": 1250.75,
        "work_period": "2025-03-01 to 2025-03-15",
        "submitted_by": "ammar.muhammed@geg-construction.com",
        "submitted_at": datetime.now().isoformat(),
        "description": "Test payment for development",
        "status": "Pending",
        "reviewed_by": ""
    }
    
    payments = load_payments()
    payments.append(dummy_payment)
    save_payments(payments)

    st.success("✅ Dummy payment added.")

# Function to show GitHub token for demo purposes
def use_github_token():
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo("your-username/your-repository")  # Replace with your repo details
    st.write(f"Using GitHub token for: {repo.name}")
    # You can perform additional operations with GitHub here, like pushing updates to a repo

def approval_page():
    st.title("Approval Page")

    # Show dummy payment options
    if st.button("Add Dummy Payment"):
        add_dummy_payment()

    # Use GitHub token for demonstration
    use_github_token()

if __name__ == "__main__":
    approval_page()
