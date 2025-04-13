import streamlit as st

def get_current_user():
    # Implement your user authentication logic here
    user = st.session_state.get("user")
    return user
