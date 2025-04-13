import streamlit as st
import json
import hashlib
from auth import load_users, save_users

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def show_login():
    st.subheader("🔐 Login to GEG-ZAS Payment System")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        users = load_users()
        if email in users:
            if not users[email].get("approved"):
                st.error("Your account is not approved yet.")
                return
            if users[email]["password"] == hash_password(password):
                st.session_state["user"] = email
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Incorrect password.")
        else:
            st.error("Email not found.")

def show_register():
    st.subheader("📝 Register New Account")
    email = st.text_input("New Email")
    password = st.text_input("Create Password", type="password")

    if st.button("Register"):
        users = load_users()
        if email in users:
            st.warning("This email is already registered.")
            return

        users[email] = {
            "password": hash_password(password),
            "approved": False,
            "role": "user"
        }
        save_users(users)
        st.success("Registration successful. Awaiting admin approval.")

def main():
    if "user" not in st.session_state:
        tab = st.sidebar.radio("Select", ["Login", "Register"])
        if tab == "Login":
            show_login()
        else:
            show_register()
        return

    st.sidebar.success(f"Logged in as {st.session_state['user']}")
    if st.sidebar.button("Logout"):
        del st.session_state["user"]
        st.rerun()

    st.switch_page("pages/1_Payment_Request.py")

if __name__ == "__main__":
    main()
