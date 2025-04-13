import streamlit as st

def get_current_user():
    """Simulate user authentication (dummy user for now)"""
    user_email = st.session_state.get('user_email', None)
    if user_email:
        return user_email
    else:
        st.warning("Please log in to proceed.")
        return None
