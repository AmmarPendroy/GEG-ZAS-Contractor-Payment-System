import streamlit as st
from auth import get_all_users, approve_user, reject_user, change_password
from auth import get_current_user
from utils.sidebar import render_sidebar

st.set_page_config(page_title="Manage Users", page_icon="🔧")

user = get_current_user()
if not user:
    st.warning("🔒 Please log in first.")
    st.stop()

render_sidebar()
st.title("🔧 User Management Panel")
st.caption("Admin-only: View and manage all registered users")

users = get_all_users()

if not users:
    st.info("No users in system.")
    st.stop()

for u in users:
    with st.expander(f"👤 {u['email']} | Role: {u['role']} | Approved: {u['approved']}"):
        col1, col2, col3 = st.columns([1, 1, 2])

        if col1.button("✅ Approve", key=f"approve_{u['email']}"):
            approve_user(u["email"])
            st.success(f"{u['email']} approved.")
            st.experimental_rerun()

        if col2.button("❌ Reject/Delete", key=f"reject_{u['email']}"):
            reject_user(u["email"])
            st.warning(f"{u['email']} removed.")
            st.experimental_rerun()

        with col3:
            st.write("🔁 Reset Password:")
            new_pass = st.text_input(f"New Password for {u['email']}", type="password", key=f"pw_{u['email']}")
            if st.button("Change Password", key=f"cpw_{u['email']}"):
                success, msg = change_password(u["email"], "admin_reset", new_pass)
                st.success("✅ Password reset (using system override)")
