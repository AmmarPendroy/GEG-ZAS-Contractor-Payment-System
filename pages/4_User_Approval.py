import streamlit as st
from auth import get_current_user, get_all_users, approve_user, reject_user

user = get_current_user()
if not user or user["role"] != "hq_admin":
    st.warning("Only HQ Admins can access this page.")
    st.stop()

st.title("👥 User Approval Management")
st.write("Approve or reject new user registrations.")

users = get_all_users()

pending_users = {k: v for k, v in users.items() if not v.get("approved", False)}

if pending_users:
    for email, data in pending_users.items():
        with st.expander(f"{email} – Role: {data['role']}"):
            col1, col2 = st.columns(2)
            if col1.button("✅ Approve", key=f"approve_{email}"):
                approve_user(email)
                st.success(f"Approved {email}")
                st.rerun()
            if col2.button("❌ Reject", key=f"reject_{email}"):
                reject_user(email)
                st.warning(f"Rejected {email}")
                st.rerun()
else:
    st.info("No users pending approval.")
