import streamlit as st
from auth import login_user, register_user, change_password, get_current_user

def main():
    if "user" in st.session_state:
        st.switch_page("pages/1_Payment_Request.py")

    st.title("🔐 GEG-ZAS Login/Register")

    tab1, tab2, tab3 = st.tabs(["Login", "Register", "Change Password"])

    # Login Tab
    with tab1:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            success, msg = login_user(email, password)
            if success:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)

    # Register Tab
    with tab2:
        new_email = st.text_input("Email", key="register_email")
        new_pass = st.text_input("Password", type="password", key="register_pass")

        role = st.selectbox("Select your role", [
            "HQ - Project Director",
            "HQ - Admin",
            "HQ - Accountantt",
            "ZAS - Project Manager",
            "ZAS - Accountant"
        ], key="register_role")

        if st.button("Register"):
            success, msg = register_user(new_email, new_pass, role)
            if success:
                st.success(msg)
            else:
                st.error(msg)

    # Change Password Tab
    with tab3:
        email_cp = st.text_input("Your Email", key="cp_email")
        old_pass = st.text_input("Old Password", type="password", key="cp_old")
        new_pass = st.text_input("New Password", type="password", key="cp_new")
        if st.button("Change Password"):
            success, msg = change_password(email_cp, old_pass, new_pass)
            if success:
                st.success(msg)
            else:
                st.error(msg)

if __name__ == "__main__":
    main()
