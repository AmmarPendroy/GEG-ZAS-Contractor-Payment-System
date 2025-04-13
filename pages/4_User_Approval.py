import streamlit as st
from utils.sidebar import render_sidebar
from utils.taskbar import render_taskbar
from auth import get_all_users, approve_user, reject_user

render_sidebar()
render_taskbar()
st.title("👥 User Approval")

if st.session_state.get("role") not in ["hq_admin", "hq_project_director"]:
    st.warning("Access restricted to HQ Admin or Project Director.")
    st.stop()

users = get_all_users()
for email, info in users.items():
    if not info.get("approved"):
        with st.expander(f"{email}"):
            col1, col2 = st.columns(2)
            if col1.button("Approve", key=f"approve_{email}"):
                success, message = approve_user(email)
                st.success(f"{email} approved." if success else message)
                st.rerun()
            if col2.button("Reject", key=f"reject_{email}"):
                success, message = reject_user(email)
                st.error(f"{email} rejected." if success else message)
                st.rerun()
