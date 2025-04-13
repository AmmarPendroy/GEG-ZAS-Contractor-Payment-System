import streamlit as st
from auth import load_users
from sidebar import show_sidebar

def show_login():
    st.title("🔐 Login to GEG-ZAS Payment System")

    email = st.text_input("Enter your email to log in:")
    if st.button("Login"):
        users = load_users()
        if email in users:
            if users[email].get("approved"):
                st.session_state["user"] = email
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Your account is not approved yet.")
        else:
            st.error("Email not found. Please contact admin.")

def main():
    if "user" not in st.session_state:
        show_login()
        return

    show_sidebar()
    st.switch_page("pages/1_Payment_Request.py")

if __name__ == "__main__":
    main()
