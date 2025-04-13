import streamlit as st
from auth import get_current_user, logout_user

def show_sidebar():
    user = get_current_user()
    if user:
        st.sidebar.info(f"👤 Logged in as: **{user}**")
        if st.sidebar.button("🔓 Logout"):
            logout_user()
            st.rerun()
    else:
        st.sidebar.warning("Not logged in.")
