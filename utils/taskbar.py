import streamlit as st

def render_taskbar():
    if st.session_state.get("logged_in"):
        username = st.session_state.get("username", "Unknown")
        role = st.session_state.get("role", "No role")

        with st.container():
            st.markdown(
                f"""
                <div style='background-color: #f0f2f6; padding: 0.8rem 1.2rem; border-radius: 0.5rem; display: flex; justify-content: space-between; align-items: center;'>
                    <div style='font-size: 1rem; font-weight: bold;'>👤 {username.replace('_', ' ')} | 🧭 {role.replace('_', ' ').title()}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
