import streamlit as st
from github import Github

# GitHub token authentication
g = Github(st.secrets["github"]["token"])

# Get the repository
repo = g.get_repo("AmmarPendroy/GEG-ZAS-Contractor-Payment-System")  # Use your actual repo details

def create_github_issue():
    issue = repo.create_issue(
        title="Payment Approval Update",
        body="A payment has been approved and logged."
    )
    print(f"Issue created: {issue.title}")

# Streamlit page
st.title("GEG-ZAS Contractor Payment System")

st.write("This is the main page of the GEG-ZAS Contractor Payment System.")
if st.button("Create GitHub Issue"):
    create_github_issue()
    st.success("GitHub issue created successfully!")
