import streamlit as st

def show_sidebar():
    with st.sidebar:
        st.success(f"👤 Logged in as: {st.session_state['user']}")
        if st.button("Logout"):
            st.session_state.clear()
            st.rerun()
