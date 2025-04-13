import streamlit as st

def render_taskbar():
    if st.session_state.get("logged_in"):
        username = st.session_state.get("username", "Unknown")
        role = st.session_state.get("role", "unknown")

        # Role-based colors
        color_map = {
            "hq_project_director": "#004d99",
            "hq_admin": "#006600",
            "hq_accountant": "#993300",
            "zas-pm": "#336699",
            "zas-accountant": "#9966cc",
        }
        bg_color = color_map.get(role, "#444")

        st.markdown(
            f"""
            <div style='position:sticky;top:0;z-index:999;background-color:{bg_color};color:white;
                        padding:0.6rem 1.2rem;border-radius:0.5rem 0.5rem 0 0;
                        display:flex;justify-content:space-between;align-items:center;box-shadow:0px 2px 6px rgba(0,0,0,0.2);'>
                <div>👤 <b>{username.replace('_', ' ')}</b> &nbsp;|&nbsp; 🧭 <i>{role.replace('_', ' ').title()}</i></div>
                <form action="" method="post">
                    <button style='background:none;border:none;color:white;cursor:pointer;font-weight:bold;' title='Logout' name='logout'>🚪 Logout</button>
                </form>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.session_state.get("logout"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.role = None
            st.rerun()
