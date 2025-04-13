from auth import get_current_user, get_all_users, approve_user, reject_user
import streamlit as st
from utils.sidebar import render_sidebar

# Check if the user is logged in
user = get_current_user()
if not user:
    st.warning("Login required.")
    st.stop()

# Render the sidebar
render_sidebar()

# Set the title for the page
st.title("👥 User Approval")

# Get all users from the database
users = get_all_users()

# Iterate over users to display approval options
for email, info in users.items():
    if not info.get("approved"):  # Only show unapproved users
        with st.expander(f"{email}"):
            col1, col2 = st.columns(2)

            # Approve button
            if col1.button("Approve", key=f"approve_{email}"):
                success, message = approve_user(email)
                if success:
                    st.success(f"{email} approved.")
                else:
                    st.error(message)
                st.experimental_rerun()

            # Reject button
            if col2.button("Reject", key=f"reject_{email}"):
                success, message = reject_user(email)
                if success:
                    st.error(f"{email} rejected.")
                else:
                    st.error(message)
                st.experimental_rerun()
