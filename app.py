import streamlit as st
from github import Github
from utils.emailer import send_email
from db import load_payments, save_payments
from auth import get_current_user
import os

# Get the current user
user = get_current_user()
if not user:
    st.warning("Login required.")
    st.stop()

# GitHub Authentication
# Initialize the GitHub API using the token from Streamlit secrets
github_token = st.secrets["github"]["token"]
g = Github(github_token)

# Access the repository
repo = g.get_repo("AmmarPendroy/GEG-ZAS-Contractor-Payment-System")

# Streamlit title
st.title("📊 GEG ZAS Contractor Payment System")

# Example of fetching issues or data from the repo
issues = repo.get_issues(state='open')
st.write("### Open Issues in the Repository:")
for issue in issues:
    st.write(f"- {issue.title} (#{issue.number})")

# Further logic to interact with payments and other functionalities
# Loading existing payments
payments = load_payments()

# Displaying the payments in a data table
if payments:
    st.write("### Payments")
    st.dataframe(payments)
else:
    st.write("No payments found.")

# Allowing to add a new payment
if st.button("Add Payment"):
    new_payment = {
        "contractor": "New Contractor Inc.",
        "amount": 2000.00,
        "work_period": "2025-04-01 to 2025-04-15",
        "submitted_by": user,
        "submitted_at": "2025-04-15T00:00:00",
        "description": "Payment for April work",
        "status": "Pending",
        "reviewed_by": ""
    }
    payments.append(new_payment)
    save_payments(payments)
    st.success("New payment added successfully!")
