import csv
import bcrypt
import streamlit as st
from utils.emailer import send_approval_request_email

USER_CSV = "user_db.csv"

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def load_users():
    users = []
    try:
        with open(USER_CSV, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                users.append(row)
    except FileNotFoundError:
        pass
    return users

def save_users(users):
    with open(USER_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["email", "username", "password", "approved", "role"])
        writer.writeheader()
        for user in users:
            writer.writerow(user)

def get_current_user():
    return st.session_state.get("user")

def logout_user():
    if "user" in st.session_state:
        del st.session_state["user"]

def register_user(username, email, password, role):
    email = email.strip().lower()
    users = load_users()
    for u in users:
        if u["email"].strip().lower() == email:
            return False, "User already exists."

    send_approval_request_email(username, email, role, password)
    return True, "Registration request sent for approval."

def verify_password(plain_password, hashed_password):
    if not hashed_password or not isinstance(hashed_password, str):
        return False
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

def login_user(email, password):
    email = email.strip().lower()
    users = load_users()
    for row in users:
        if row["email"].strip().lower() == email:
            if row.get("approved", "").lower() != "true":
                return False, "Account not approved yet."
            if verify_password(password, row["password"]):
                st.session_state["user"] = row["email"]
                return True, "Login successful."
            else:
                return False, "Incorrect password."
    return False, "Email not found."
