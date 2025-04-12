import streamlit as st
import json
import os
import hashlib
from utils.emailer import send_email

USER_DB_FILE = "user_db.json"
SESSION_KEY = "current_user"

# --- Helper functions ---

def load_users():
    if os.path.exists(USER_DB_FILE):
        with open(USER_DB_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USER_DB_FILE, "w") as f:
        json.dump(users, f, indent=2)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# --- Auth functions ---

def get_current_user():
    return st.session_state.get(SESSION_KEY)

def logout():
    if SESSION_KEY in st.session_state:
        del st.session_state[SESSION_KEY]

def login():
    users = load_users()

    with st.sidebar:
        st.subheader("Login / Register")

        choice = st.radio("Choose action:", ["Login", "Register"])

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if choice == "Register":
            role = st.selectbox("Role", ["site_pm", "site_accountant", "hq_admin", "hq_director"])
            if st.button("Register"):
                if not email.endswith("@geg-construction.com"):
                    st.error("Email must be from @geg-construction.com domain.")
                    return
                if email in users:
                    st.error("Email already registered.")
                    return
                users[email] = {
                    "password": hash_password(password),
                    "role": role,
                    "approved": False
                }
                save_users(users)
                st.success("Registered. Awaiting approval by HQ.")
        else:
            if st.button("Login"):
                if email not in users:
                    st.error("Email not found.")
                    return
                user = users[email]
                if hash_password(password) != user["password"]:
                    st.error("Incorrect password.")
                    return
                if not user.get("approved", False):
                    st.warning("Account pending approval by HQ.")
                    return
                st.session_state[SESSION_KEY] = {"email": email, "role": user["role"]}
                st.experimental_rerun()

# --- Admin functions ---

def get_all_users():
    return load_users()

def approve_user(email):
    users = load_users()
    if email in users:
        users[email]["approved"] = True
        save_users(users)
        send_email(
            to=email,
            subject="✅ Access Approved – GEG-ZAS System",
            body="Your account has been approved. You may now log in."
        )

def reject_user(email):
    users = load_users()
    if email in users:
        del users[email]
        save_users(users)
        send_email(
            to=email,
            subject="❌ Access Denied – GEG-ZAS System",
            body="Your registration was not approved. Contact HQ for help."
        )
