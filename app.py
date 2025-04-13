import streamlit as st
from utils.emailer import send_email
from pages import approval_page, dashboard_page
from auth import get_current_user

# Ensure the user is logged in
user = get_current_user()
if not user:
    st.warning("Login required.")
    st.stop()

# App title and selection
st.title("GEG-ZAS Contractor Payment System")

# Sidebar with navigation options
page = st.sidebar.radio("Select a page", ["Dashboard", "Approval Page"])

if page == "Dashboard":
    dashboard_page.dashboard()
elif page == "Approval Page":
    approval_page.approval_page()
