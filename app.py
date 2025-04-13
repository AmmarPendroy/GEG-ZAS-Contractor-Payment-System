import streamlit as st
from auth import login_user, register_user, get_current_user, logout_user

def main():
    if "user" in st.session_state:
        st.switch_page("pages/1_Payment_Request.py")

    st.title("🔐 GEG-ZAS Login & Registration")

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        email = st.text_input("Email", key="login_email").strip().lower()
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            success, msg = login_user(email, password)
            if success:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)

    with tab2:
        username = st.text_input("Username", key="reg_user")
        email = st.text_input("Email", key="reg_email").strip().lower()
        password = st.text_input("Password", type="password", key="reg_pass")
        role = st.selectbox("Role", [
            "hq_project_director",
            "hq_admin",
            "hq_accountant",
            "zas_project_manager",
            "zas_accountant"
        ])
        if st.button("Request Registration"):
            if username and email and password and role:
                success, msg = register_user(username, email, password, role)
                if success:
                    st.success(msg)
                else:
                    st.error(msg)
            else:
                st.warning("Please fill in all fields.")

if __name__ == "__main__":
    main()
