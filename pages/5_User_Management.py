import streamlit as st
from auth import get_all_users, approve_user, reject_user, change_password
from utils.sidebar import render_sidebar

user = st.session_state.get("user")
if not user:
    st.warning("Login required.")
    st.stop()

render_sidebar()
st.title("🛡️ User Management")

users = get_all_users()

if not users:
    st.info("No users found.")
    st.stop()

for email, info in users.items():
    with st.expander(f"{email} ({'✅' if info.get('approved') else '❌'})"):
        st.text(f"Role: {info.get('role', 'N/A')}")

        col1, col2, col3 = st.columns(3)

        if not info.get("approved") and col1.button("Approve", key=f"approve_{email}"):
            success, msg = approve_user(email)
            st.success(msg) if success else st.error(msg)
            st.experimental_rerun()

        if col2.button("Reject/Delete", key=f"reject_{email}"):
            success, msg = reject_user(email)
            st.success(msg) if success else st.error(msg)
            st.experimental_rerun()

        with col3:
            with st.form(key=f"reset_{email}"):
                new_pass = st.text_input("New Password", type="password")
                submit = st.form_submit_button("Reset Password")
                if submit and new_pass:
                    success, msg = change_password(email, info["password"], new_pass)
                    st.success("Password reset.") if success else st.error(msg)
