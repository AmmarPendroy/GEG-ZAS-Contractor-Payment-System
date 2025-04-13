import streamlit as st
import json
import os
import hashlib
from utils.emailer import send_email

USER_DB_FILE = "user_db.json"
SESSION_KEY = "current_user"

HQ_ADMIN_EMAIL = "ammar.muhammed@geg-construction.com"  # Automatically approved

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

# --- Session handling ---

def get_current_user():
    return st.session_state.get(SESSION_KEY)

def logout():
    if SESSION_KEY in st.session_state:
        del st.session_state[SESSION_KEY]

# --- Main login/register logic ---

def login():
    users = load_users()

    with st.sidebar:
        st.subheader("Login / Register")

        tab = st.radio("Choose option:", ["Login", "Register", "Reset Password"])

        if tab == "Login":
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            remember = st.checkbox("Remember me")

            if st.button("Login"):
                if email == HQ_ADMIN_EMAIL:
                    st.session_state[SESSION_KEY] = {"email": email, "role": "hq_admin"}
                    st.experimental_rerun()  # Skip further checks for HQ Admin
                elif email not in users:
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
                if remember:
                    st.session_state["remembered_user"] = st.session_state[SESSION_KEY]
                st.experimental_rerun()

        elif tab == "Register":
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
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

        elif tab == "Reset Password":
            email = st.text_input("Enter your email for reset")
            new_pass = st.text_input("New password", type="password")
            confirm_pass = st.text_input("Confirm new password", type="password")

            if st.button("Reset Password"):
                if email not in users:
                    st.error("Email not found.")
                    return
                if new_pass != confirm_pass:
                    st.error("Passwords do not match.")
                    return
                users[email]["password"] = hash_password(new_pass)
                save_users(users)
                send_email(
                    to=email,
                    subject="🔒 Password Reset - GEG-ZAS System",
                    body="Your password has been reset successfully. You can now log in with your new password."
                )
                st.success("Password reset successfully.")

    # Restore session from "Remember me"
    if "remembered_user" in st.session_state and SESSION_KEY not in st.session_state:
        st.session_state[SESSION_KEY] = st.session_state["remembered_user"]

def get_all_users():
    return load_users()

def approve_user(email):
    users = load_users()
    if email in users:
        users[email]["approved"] = True
        save_users(users)

def reject_user(email):
    users = load_users()
    if email in users:
        del users[email]
        save_users(users)

