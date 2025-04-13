import csv
import bcrypt

USER_CSV = "user_db.csv"

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

def get_all_users():
    return load_users()

def get_current_user():
    import streamlit as st
    return st.session_state.get("user")

def logout_user():
    import streamlit as st
    if "user" in st.session_state:
        del st.session_state["user"]

def verify_password(plain_password, hashed_password):
    if not hashed_password or not isinstance(hashed_password, str):
        return False
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

def login_user(email, password):
    import streamlit as st
    email = email.strip().lower()
    users = load_users()
    for row in users:
        if row["email"].strip().lower() == email:
            print(">> Trying login:", email)
            print(">> Input password:", password)
            print(">> Stored hash:", row["password"])
            match = verify_password(password, row["password"])
            print(">> Match?", match)
            if not row.get("approved", "").lower() == "true":
                return False, "Account not approved yet."
            if match:
                st.session_state["user"] = row["email"]
                return True, "Login successful."
            else:
                return False, "Incorrect password."
    return False, "Email not found."
