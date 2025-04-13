import streamlit as st
from auth import login_user, register_user, change_password, get_current_user
from utils.sidebar import render_sidebar

st.set_page_config(page_title="GEG-ZAS | Login", page_icon="🔐")

def main():
    render_sidebar()

    # Theme toggle (stored in session)
    if "theme" not in st.session_state:
        st.session_state.theme = "light"

    theme_toggle = st.sidebar.radio("🌓 Theme", ["light", "dark"], index=0 if st.session_state.theme == "light" else 1)
    st.session_state.theme = theme_toggle

    # Welcome screen if not logged in
    if "user" not in st.session_state:
        st.image("static/geg_logo.png", width=180)
        st.title("🏗️ Welcome to GEG-ZAS Contractor Portal")
        st.markdown("""
        This portal is for **ZAS project teams** and **GEG HQ staff** to manage contractor payments.

        - 📝 Submit & track payment requests  
        - ✅ HQ approval system  
        - 📊 Dashboard insights  
        - 📁 Secure document uploads  
        """)

        st.markdown("---")
        if st.button("🔐 Continue to Login/Register"):
            st.session_state.show_login = True
        elif "show_login" not in st.session_state:
            return

    st.title("🔐 Login / Register")

    tab1, tab2, tab3 = st.tabs(["🔓 Login", "📝 Register", "🔁 Change Password"])

    # === LOGIN TAB ===
    with tab1:
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
        new_email = st.text_input("📧 Email", key="register_email").strip().lower()
        new_pass = st.text_input("🔐 Password", type="password", key="register_pass")

        role = st.selectbox("👤 Select Role", [
            "zas_project_manager",
            "zas_accountant",
            "hq_admin",
            "hq_accountant",
            "hq_project_director"
        ])

        if st.button("Register"):
            success, msg = register_user(new_email, new_pass, role)
            if success:
                st.success("✅ " + msg)
            else:
                st.error("❌ " + msg)

    # === PASSWORD RESET TAB ===
    with tab3:
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
