import streamlit as st
from utils.sidebar import render_sidebar
from utils.taskbar import render_taskbar

AUTHORIZED_USERS = {
    "Raad_Kakoni": {"password": "ABC", "role": "hq_project_director"},
    "Raman_Sherwani": {"password": "ABC", "role": "hq_admin"},
    "accountant1": {"password": "ABC", "role": "hq_accountant"},
    "Bala_Kawa": {"password": "ABC", "role": "zas-pm"},
    "SiteAccountant": {"password": "ABC", "role": "zas-accountant"},
}

def main():
    st.set_page_config(page_title="GEG-ZAS Login", layout="centered")

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.role = None

    if not st.session_state.logged_in:
        st.image("static/geg_logo.png", use_container_width=True)
        st.title("🔐 Login to GEG-ZAS")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            user = AUTHORIZED_USERS.get(username)
            if user and user["password"] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.role = user["role"]
                st.success(f"✅ Welcome, {username}!")
                st.rerun()
            else:
                st.error("❌ Invalid credentials. Please try again.")

    else:
        render_sidebar()
        render_taskbar()
        st.title("🏗️ GEG-ZAS Contractor Payment System")

        st.markdown("""
        Use the sidebar to:
        - 📤 Submit or view payment requests
        - ✅ Approve or reject requests
        - 📊 Access dashboards and reports
        - 📖 View help and manuals
        """)

        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.role = None
            st.rerun()

if __name__ == "__main__":
    main()
