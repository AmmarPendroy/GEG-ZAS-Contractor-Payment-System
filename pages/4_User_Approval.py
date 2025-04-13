import streamlit as st
from utils.sidebar import render_sidebar
from auth import get_all_users, approve_user, reject_user

render_sidebar()
st.title("👥 User Approval")

users = get_all_users()

for email, info in users.items():
    if not info.get("approved"):  # Only show unapproved users
        with st.expander(f"{email}"):
            col1, col2 = st.columns(2)
            if col1.button("Approve", key=f"approve_{email}"):
                success, message = approve_user(email)
                st.success(f"{email} approved." if success else message)
                st.experimental_rerun()
            if col2.button("Reject", key=f"reject_{email}"):
                success, message = reject_user(email)
                st.error(f"{email} rejected." if success else message)
                st.experimental_rerun()
