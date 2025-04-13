# auth.py
import json
import streamlit as st

USER_DB_PATH = "user_db.json"

def load_users():
    try:
        with open(USER_DB_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_users(users):
    with open(USER_DB_PATH, "w") as f:
        json.dump(users, f, indent=4)

def get_current_user():
    return st.session_state.get("user", "")

def get_all_users():
    users = load_users()
    return [{"email": email, **details} for email, details in users.items()]

def approve_user(email):
    users = load_users()
    if email in users:
        users[email]["approved"] = True
        save_users(users)

def reject_user(email):
    users = load_users()
    if email in users:
        users[email]["approved"] = False
        save_users(users)
