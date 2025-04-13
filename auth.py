import csv
import hashlib
import os
import bcrypt
import streamlit as st

USERS_FILE = "user_db.csv"

# ======================
# Password Hashing
# ======================
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

# ======================
# User Session Management
# ======================
def get_current_user():
    return st.session_state.get("user")

def logout_user():
    if "user" in st.session_state:
        del st.session_state["user"]

# ======================
# CSV Load/Save Helpers
# ======================
def get_all_users():
    try:
        with open(USERS_FILE, newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    except FileNotFoundError:
        return []

def save_all_users(users):
    with open(USERS_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["email", "password", "role", "approved"])
        writer.writeheader()
        writer.writerows(users)

# ======================
# Core Auth Functions
# ======================
def register_user(email, password, role="user"):
    email = email.strip().lower()
    users = get_all_users()

    for u in users:
        if u["email"] == email:
            return False, "User already exists."

    hashed = hash_password(password)
    users.append({
        "email": email,
        "password": hashed,
        "role": role,
        "approved": "False"
    })

    save_all_users(users)
    return True, "Registration successful. Awaiting approval."

def login_user(email, password):
    email = email.strip().lower()
    users = get_all_users()

    for row in users:
        if row["email"] == email:
            if row["approved"].lower() != "true":
                return False, "Account not approved yet."

            if verify_password(password, row["password"]):
                st.session_state["user"] = email
                return True, "Login successful."
            else:
                return False, "Incorrect password."

    return False, "Email not found."

def change_password(email, old_password, new_password):
    email = email.strip().lower()
    users = get_all_users()
    updated = False

    for row in users:
        if row["email"] == email:
            if not verify_password(old_password, row["password"]):
                return False, "Old password is incorrect."
            row["password"] = hash_password(new_password)
            updated = True
            break

    if updated:
        save_all_users(users)
        return True, "Password changed successfully."
    return False, "User not found."

# ======================
# Admin Actions
# ======================
def approve_user(email):
    email = email.strip().lower()
    users = get_all_users()
    found = False
    for row in users:
        if row["email"] == email:
            row["approved"] = "True"
            found = True
            break
    if found:
        save_all_users(users)
        return True, "User approved."
    return False, "User not found."

def reject_user(email):
    email = email.strip().lower()
    users = get_all_users()
    filtered = [u for u in users if u["email"] != email]
    if len(filtered) == len(users):
        return False, "User not found."
    save_all_users(filtered)
    return True, "User rejected/deleted."
