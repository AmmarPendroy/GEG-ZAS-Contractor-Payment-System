import json
import streamlit as st
import hashlib

USERS_FILE = "user_db.json"

def load_users():
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_current_user():
    return st.session_state.get("user")

def logout_user():
    if "user" in st.session_state:
        del st.session_state["user"]

def register_user(email, password):
    users = load_users()
    if email in users:
        return False, "User already exists."
    users[email] = {
        "password": hash_password(password),
        "approved": False,
        "role": "user"
    }
    save_users(users)
    return True, "Registration successful. Awaiting approval."

def login_user(email, password):
    users = load_users()
    if email not in users:
        return False, "Email not found."
    if not users[email].get("approved", False):
        return False, "Account not approved yet."
    if users[email]["password"] != hash_password(password):
        return False, "Incorrect password."
    st.session_state["user"] = email
    return True, "Login successful."

def change_password(email, old_password, new_password):
    users = load_users()
    if email not in users:
        return False, "Email not found."
    if users[email]["password"] != hash_password(old_password):
        return False, "Old password incorrect."
    users[email]["password"] = hash_password(new_password)
    save_users(users)
    return True, "Password updated successfully."

# Additional Functions

def get_all_users():
    """Returns all users in the system"""
    return load_users()

def approve_user(email):
    """Approves a user by setting their 'approved' field to True"""
    users = load_users()
    if email not in users:
        return False, "User not found."
    users[email]["approved"] = True
    save_users(users)
    return True, "User approved."

def reject_user(email):
    """Rejects a user by setting their 'approved' field to False"""
    users = load_users()
    if email not in users:
        return False, "User not found."
    users[email]["approved"] = False
    save_users(users)
    return True, "User rejected."
