import streamlit as st
from auth import login_user, register_user, change_password, get_current_user

st.set_page_config(page_title="GEG-ZAS | Login", page_icon="🔐")

def main():
    if "user" in st.session_state:
        st.switch_page("pages/1_Payment_Request.py")

    st.title("🔐 GEG-ZAS Contractor Payment Portal")
    st.caption("Secure access for project teams and HQ.")

    tab1, tab2, tab3 = st.tabs(["🔓 Login", "📝 Register", "🔁 Change Password"])

    # === LOGIN TAB ===
    with tab1:
        st.subheader("🔓 Login to Your Account")
        email = st.text_input("📧 Email", key="login_email").strip().lower()
        password = st.text_input("🔑 Password", type="password", key="login_pass")
        if st.button("Login"):
            success, msg = login_user(email, password)
            if success:
                st.success("✅ " + msg)
                st.rerun()
            else:
                st.error("❌ " + msg)

    # === REGISTER TAB ===
    with tab2:
        st.subheader("📝 Create a New Account")
        new_email = st.text_input("📧 Email", key="register_email").strip().lower()
        new_pass = st.text_input("🔐 Password", type="password", key="register_pass")

        role = st.selectbox("👤 Select Role", [
            "zas_project_manager",
            "zas_accountant",
            "hq_admin",
            "hq_accountant",
            "hq_project_director"
        ], index=0)

        if st.button("Register"):
            success, msg = register_user(new_email, new_pass, role)
            if success:
                st.success("✅ " + msg)
            else:
                st.error("❌ " + msg)

    # === PASSWORD RESET TAB ===
    with tab3:
        st.subheader("🔁 Reset Your Password")
        email = st.text_input("📧 Email", key="reset_email").strip().lower()
        old_pass = st.text_input("🔑 Current Password", type="password", key="reset_old")
        new_pass = st.text_input("🆕 New Password", type="password", key="reset_new")

        if st.button("Change Password"):
            success, msg = change_password(email, old_pass, new_pass)
            if success:
                st.success("🔒 " + msg)
            else:
                st.error("❌ " + msg)

if __name__ == "__main__":
    main()
