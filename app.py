import streamlit as st
from auth import login, logout, get_current_user
import db

st.set_page_config(page_title="GEG-ZAS Contractor Payment System", layout="wide")

user = get_current_user()

if not user:
    login()
else:
    st.sidebar.title("GEG-ZAS Contractor Payment System")
    st.sidebar.write(f"Logged in as: {user['email']} ({user['role']})")
    if st.sidebar.button("Logout"):
        logout()

    st.title("🏗️ GEG-ZAS Contractor Payment System")
    st.info("Use the pages in the sidebar to navigate: Submit Requests, Approve, or View Dashboard.")
