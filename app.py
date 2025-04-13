import streamlit as st
from auth import login_user, register_user, change_password, get_current_user

def main():
    if get_current_user():
        st.switch_page("pages/1_Payment_Request.py")

    st.set_page_config(page_title="GEG-ZAS Login", page_icon="🔐")
    st.markdown("<h1 style='text-align:center;'>🔐 GEG-ZAS Login & Registration</h1>", unsafe_allow_html=True)
    st.divider()

    tab_login, tab_register, tab_reset = st.tabs(["🔓 Login", "📝 Register", "🔄 Change Password"])

    with tab_login:
        st.subheader("🔐 Login to Your Account")
        email = st.text_input("Email", key="login_email").strip().lower()
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            success, msg = login_user(email, password)
            st.success(msg) if success else st.error(msg)
            if success: st.rerun()

    with tab_register:
        st.subheader("📝 Request Access")
        username = st.text_input("Full Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Select Role", [
            "hq_project_director",
            "hq_admin",
            "hq_accountant",
            "zas_project_manager",
            "zas_accountant"
        ])
        if st.button("Request Registration"):
            if username and email and password:
                success, msg = register_user(username, email, password, role)
                st.success(msg) if success else st.error(msg)
            else:
                st.warning("Please fill in all fields.")

    with tab_reset:
        st.subheader("🔄 Reset Password")
        email = st.text_input("Your Email")
        old = st.text_input("Current Password", type="password")
        new = st.text_input("New Password", type="password")
        if st.button("Change Password"):
            success, msg = change_password(email, old, new)
            st.success(msg) if success else st.error(msg)

if __name__ == "__main__":
    main()
