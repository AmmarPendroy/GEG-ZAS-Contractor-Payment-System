import streamlit as st

USERS = {
    "pm@site.com": {"password": "123", "role": "site_pm"},
    "acc@site.com": {"password": "456", "role": "site_acc"},
    "hq@admin.com": {"password": "789", "role": "hq_admin"},
}

def login():
    st.sidebar.title("Login")
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        user = USERS.get(email)
        if user and user["password"] == password:
            st.session_state["user"] = {"email": email, "role": user["role"]}
            st.success("Logged in!")
            st.rerun()
        else:
            st.error("Invalid credentials")

def get_current_user():
    return st.session_state.get("user", None)

def logout():
    if "user" in st.session_state:
        del st.session_state["user"]
        st.rerun()
