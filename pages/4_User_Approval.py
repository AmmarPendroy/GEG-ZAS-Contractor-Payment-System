from auth import get_current_user, get_all_users, approve_user, reject_user
import streamlit as st
from utils.sidebar import render_sidebar

user = get_current_user()
if not user:
    st.warning("Login required.")
    st.stop()

render_sidebar()
st.title("👥 User Approval")

users = get_all_users()
current_role = users.get(user, {}).get("role")

if current_role not in ["hq_admin", "hq_project_director"]:
    st.error("Access denied. Only HQ Admin or HQ Project Director can manage user approvals.")
    st.stop()

for email, info in users.items():
    if not info.get("approved"):  # Only unapproved users
        with st.expander(f"{email} - Role: {info.get('role', 'N/A')}"):
            col1, col2 = st.columns(2)

            if col1.button("Approve", key=f"approve_{email}"):
                success, message = approve_user(email)
                if success:
                    st.success(f"{email} approved.")
                else:
                    st.error(message)
                st.experimental_rerun()

            if col2.button("Reject", key=f"reject_{email}"):
                success, message = reject_user(email)
                if success:
                    st.error(f"{email} rejected.")
                else:
                    st.error(message)
                st.experimental_rerun()
