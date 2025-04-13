import streamlit as st
from auth import logout_user, get_current_user

def main():
    st.set_page_config(page_title="GEG-ZAS Payment System", layout="wide")
    st.title("🔓 GEG-ZAS Contractor Payment System")

    st.markdown("""
        Welcome to the GEG-ZAS Payment Management System.
        
        Use the sidebar to navigate:
        - 📤 Submit payment requests
        - ✅ Approve pending requests (HQ only)
        - 📊 View payment dashboards
        - 👥 Manage users (HQ only)
    """)

    st.info("Login is no longer required. All pages are accessible from the sidebar.")

if __name__ == "__main__":
    main()
