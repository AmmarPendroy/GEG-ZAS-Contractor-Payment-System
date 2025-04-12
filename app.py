import streamlit as st
from auth import login, get_current_user, logout

st.set_page_config(page_title="GEG-ZAS Contractor Payment System", layout="wide")

login()

user = get_current_user()

if user:
    st.sidebar.success(f"Logged in as: {user['email']} ({user['role']})")
    if st.sidebar.button("Logout"):
        logout()

    st.title("🏗️ GEG-ZAS Contractor Payment System")
    st.markdown("Welcome to the contractor payment tracking and approval platform.")
else:
    st.stop()
