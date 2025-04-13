import streamlit as st
from auth import get_current_user, logout_user
from db import load_payments

def get_unread_notification_count(user):
    try:
        data = load_payments()
        return sum(1 for p in data if p["submitted_by"] == user and p["status"] in ["Approved", "Rejected", "Returned"])
    except:
        return 0

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

    st.sidebar.image("static/geg_logo.png", use_container_width=True, caption="GEG Construction")

    st.sidebar.markdown("### 📂 Navigation")
    st.sidebar.page_link("app.py", label="🏠 Home")
    st.sidebar.page_link("pages/1_Payment_Request.py", label="📝 Payment Request")
    st.sidebar.page_link("pages/2_Approval_Page.py", label="✅ Approval Page")
    st.sidebar.page_link("pages/3_Dashboard.py", label="📊 Dashboard")
    st.sidebar.page_link("pages/4_User_Approval.py", label="👥 User Approvals")
    st.sidebar.page_link("pages/5_User_Management.py", label="🔧 Manage Users")
    st.sidebar.page_link("pages/6_Site_Charts.py", label="🌍 Site Charts")
    st.sidebar.page_link("pages/7_Help_and_Manual.py", label="❓ Help / Manual")

    user = get_current_user()
    if user:
        # 🔔 Notification badge
        unread_count = get_unread_notification_count(user)
        notif_label = f"🔔 Notifications {'🔴 '+str(unread_count) if unread_count > 0 else ''}"
        st.sidebar.page_link("pages/8_Notifications.py", label=notif_label)

        st.sidebar.markdown(f"---\n👤 Logged in as: `{user}`")
        if st.sidebar.button("🚪 Logout"):
            logout_user()
            st.rerun()
