from auth import get_current_user, get_all_users, approve_user, reject_user
import streamlit as st

# Your existing code for handling user approval/rejection...


import streamlit as st
from auth import get_current_user, get_all_users, approve_user, reject_user
from utils.sidebar import render_sidebar

user = get_current_user()
if not user:
    st.warning("Login required.")
    st.stop()

render_sidebar()
st.title("👥 User Approval")

users = get_all_users()

for email, info in users.items():
    if not info.get("approved"):
        with st.expander(f"{email}"):
            col1, col2 = st.columns(2)
            if col1.button("Approve", key=f"approve_{email}"):
                approve_user(email)
                st.success(f"{email} approved.")
                st.experimental_rerun()
            if col2.button("Reject", key=f"reject_{email}"):
                reject_user(email)
                st.error(f"{email} rejected.")
                st.experimental_rerun()
