import csv
import bcrypt
import streamlit as st
from utils.emailer import send_approval_request_email

USER_CSV = "user_db.csv"
FIELDS = ["email", "username", "password", "approved", "role"]

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(plain_password, hashed_password):
    if not hashed_password or not isinstance(hashed_password, str):
        return False
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

def load_users():
    try:
        with open(USER_CSV, "r") as f:
            return list(csv.DictReader(f))
    except FileNotFoundError:
        return []

def save_users(users):
    with open(USER_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(users)

def get_current_user():
    return st.session_state.get("user")

def logout_user():
    st.session_state.pop("user", None)

def register_user(username, email, password, role):
    email = email.strip().lower()
    if any(u["email"].strip().lower() == email for u in load_users()):
        return False, "User already exists."
    send_approval_request_email(username, email, role, password)
    return True, "✅ Registration request sent. Please await admin approval."

def login_user(email, password):
    email = email.strip().lower()
    for row in load_users():
        if row["email"].strip().lower() == email:
            if row.get("approved", "").lower() != "true":
                return False, "🕒 Account not yet approved."
            if verify_password(password, row["password"]):
                st.session_state["user"] = row["email"]
                return True, "✅ Login successful."
            return False, "❌ Incorrect password."
    return False, "❌ Email not found."

def change_password(email, old_password, new_password):
    email = email.strip().lower()
    users = load_users()
    for user in users:
        if user["email"].strip().lower() == email:
            if verify_password(old_password, user["password"]):
                user["password"] = hash_password(new_password)
                save_users(users)
                return True, "🔐 Password updated."
            return False, "❌ Old password incorrect."
    return False, "❌ Email not found."
