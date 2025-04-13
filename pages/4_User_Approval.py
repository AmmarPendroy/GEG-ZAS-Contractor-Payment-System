import streamlit as st
from auth import get_current_user, get_all_users, approve_user, reject_user
from utils.sidebar import render_sidebar

st.set_page_config(page_title="User Approval", page_icon="👥")

user = get_current_user()
if not user:
    st.warning("🔒 Login required.")
    st.stop()

render_sidebar()
st.title("👥 Pending User Approvals")
st.caption("HQ Admin & Director Only")

users = get_all_users()
pending_users = [u for u in users if u["approved"].lower() != "true"]

if not pending_users:
    st.success("✅ No pending users.")
else:
    for u in pending_users:
        email = u["email"]
        with st.expander(f"📧 {email} | Role: {u['role']}"):
            col1, col2 = st.columns(2)

            if col1.button("✅ Approve", key=f"approve_{email}"):
                success, msg = approve_user(email)
                if success:
                    st.success(f"{email} approved.")
                else:
                    st.error(msg)
                st.experimental_rerun()

            if col2.button("❌ Reject", key=f"reject_{email}"):
                success, msg = reject_user(email)
                if success:
                    st.warning(f"{email} rejected.")
                else:
                    st.error(msg)
                st.experimental_rerun()
