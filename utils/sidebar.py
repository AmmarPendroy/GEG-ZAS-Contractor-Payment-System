import streamlit as st
from auth import get_current_user, logout_user

def render_sidebar():
    st.sidebar.markdown("""
        <style>
            .sidebar-logo {
                width: 100%;
                margin-bottom: 10px;
                border-radius: 8px;
            }
            .stButton>button {
                background-color: #004080;
                color: white;
                border-radius: 6px;
                border: none;
                padding: 6px 10px;
            }
            .stButton>button:hover {
                background-color: #0066cc;
            }
        </style>
    """, unsafe_allow_html=True)

    # ✅ Logo (fixed)
    st.sidebar.image("static/geg_logo.png", use_container_width=True, caption="GEG Construction")

    # 🔹 Navigation
    st.sidebar.markdown("### 📂 Navigation")
    st.sidebar.page_link("app.py", label="🏠 Home")
    st.sidebar.page_link("pages/1_Payment_Request.py", label="📝 Payment Request")
    st.sidebar.page_link("pages/2_Approval_Page.py", label="✅ Approval Page")
    st.sidebar.page_link("pages/3_Dashboard.py", label="📊 Dashboard")
    st.sidebar.page_link("pages/4_User_Approval.py", label="👥 User Approvals")
    st.sidebar.page_link("pages/5_User_Management.py", label="🔧 Manage Users")
    st.sidebar.page_link("pages/6_Site_Charts.py", label="🌍 Site Charts")
    st.sidebar.page_link("pages/7_Help_and_Manual.py", label="❓ Help / Manual")

    # 👤 User session + logout
    user = get_current_user()
    if user:
        st.sidebar.markdown(f"---\n👤 Logged in as: `{user}`")
        if st.sidebar.button("🚪 Logout"):
            logout_user()
            st.rerun()
