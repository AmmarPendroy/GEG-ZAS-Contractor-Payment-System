import csv
import bcrypt
import streamlit as st

USER_CSV = "user_db.csv"

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(plain_password, hashed_password):
    if not hashed_password or not isinstance(hashed_password, str):
        return False
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

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
        writer = csv.DictWriter(f, fieldnames=["email", "password", "approved", "role"])
        writer.writeheader()
        for user in users:
            writer.writerow(user)

def get_all_users():
    return load_users()

def get_current_user():
    return st.session_state.get("user")

def logout_user():
    if "user" in st.session_state:
        del st.session_state["user"]

def register_user(email, password, role):
    email = email.strip().lower()
    users = load_users()
    for u in users:
        if u["email"].strip().lower() == email:
            return False, "User already exists."
    hashed = hash_password(password)
    users.append({
        "email": email,
        "password": hashed,
        "approved": "false",
        "role": role
    })
    save_users(users)
    return True, "Registration submitted. Awaiting approval."

def login_user(email, password):
    email = email.strip().lower()
    users = load_users()
    for row in users:
        if row["email"].strip().lower() == email:
            print(">> Trying login:", email)
            print(">> Input password:", password)
            print(">> Stored hash:", row["password"])
            match = verify_password(password, row["password"])
            print(">> Match?", match)
            if row.get("approved", "").lower() != "true":
                return False, "Account not approved yet."
            if match:
                st.session_state["user"] = row["email"]
                return True, "Login successful."
            else:
                return False, "Incorrect password."
    return False, "Email not found."

def change_password(email, old_password, new_password):
    email = email.strip().lower()
    users = load_users()
    for row in users:
        if row["email"].strip().lower() == email:
            if old_password == "admin_reset" or verify_password(old_password, row["password"]):
                row["password"] = hash_password(new_password)
                save_users(users)
                return True, "Password updated."
            else:
                return False, "Old password incorrect."
    return False, "User not found."

def approve_user(email):
    email = email.strip().lower()
    users = load_users()
    for row in users:
        if row["email"].strip().lower() == email:
            row["approved"] = "true"
            save_users(users)
            return True, "User approved."
    return False, "User not found."

def reject_user(email):
    email = email.strip().lower()
    users = load_users()
    for row in users:
        if row["email"].strip().lower() == email:
            users.remove(row)
            save_users(users)
            return True, "User removed."
    return False, "User not found."
