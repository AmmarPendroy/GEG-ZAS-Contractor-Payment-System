import streamlit as st
import bcrypt
import pandas as pd
from utils.emailer import send_login_alert

USERS_FILE = "user_db.csv"

def load_users():
    try:
        return pd.read_csv(USERS_FILE, dtype=str).fillna("")
    except FileNotFoundError:
        return pd.DataFrame(columns=["email", "password", "approved", "role"])

def save_users(df):
    df.to_csv(USERS_FILE, index=False)

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

def get_current_user():
    return st.session_state.get("user")

def logout_user():
    user = get_current_user()
    if user:
        send_login_alert(user, success=False)
        del st.session_state["user"]

def register_user(email, password, role):
    df = load_users()
    email = email.strip().lower()
    if email in df["email"].values:
        return False, "User already exists."

    hashed = hash_password(password)
    new_user = pd.DataFrame([{
        "email": email,
        "password": hashed,
        "approved": "false",
        "role": role
    }])
    df = pd.concat([df, new_user], ignore_index=True)
    save_users(df)
    return True, "Registration successful. Awaiting approval."

def login_user(email, password):
    df = load_users()
    email = email.strip().lower()

    user_row = df[df["email"] == email]
    if user_row.empty:
        return False, "Email not found."

    row = user_row.iloc[0]
    if row["approved"].lower() != "true":
        return False, "Account not approved yet."

    if not verify_password(password, row["password"]):
        return False, "Incorrect password."

    st.session_state["user"] = email
    send_login_alert(email, success=True)
    return True, "Login successful."

def change_password(email, old_password, new_password):
    df = load_users()
    email = email.strip().lower()
    user_row = df[df["email"] == email]
    if user_row.empty:
        return False, "Email not found."

    idx = user_row.index[0]
    if not verify_password(old_password, df.at[idx, "password"]):
        return False, "Old password incorrect."

    df.at[idx, "password"] = hash_password(new_password)
    save_users(df)
    return True, "Password updated successfully."

def get_all_users():
    return load_users().to_dict(orient="records")

def approve_user(email):
    df = load_users()
    current_user = get_current_user()
    if current_user is None:
        return False, "Not logged in."

    approver = df[df["email"] == current_user]
    if approver.empty:
        return False, "Invalid user session."

    role = approver.iloc[0]["role"]
    if role not in ["hq_admin", "hq_project_director", "super_admin"]:
        return False, "Not authorized."

    idx = df[df["email"] == email].index
    if idx.empty:
        return False, "User not found."

    df.at[idx[0], "approved"] = "true"
    save_users(df)
    return True, "User approved."

def reject_user(email):
    df = load_users()
    current_user = get_current_user()
    if current_user is None:
        return False, "Not logged in."

    role = df[df["email"] == current_user].iloc[0]["role"]
    if role not in ["hq_admin", "hq_project_director", "super_admin"]:
        return False, "Not authorized."

    df = df[df["email"] != email]
    save_users(df)
    return True, "User rejected or deleted."
