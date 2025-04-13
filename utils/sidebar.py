import streamlit as st

def render_sidebar():
    st.sidebar.image("static/geg_logo.png", use_container_width=True)
    st.sidebar.markdown("**GEG Construction**", unsafe_allow_html=True)

    st.sidebar.markdown("---")
    st.sidebar.subheader("📁 Navigation")

    st.sidebar.page_link("app.py", label="🏠 Home")
    st.sidebar.page_link("pages/1_Payment_Request.py", label="📤 Payment Request")
    st.sidebar.page_link("pages/2_Approval_Page.py", label="✅ Approval Page")
    st.sidebar.page_link("pages/3_Dashboard.py", label="📊 Dashboard")
    st.sidebar.page_link("pages/4_User_Approval.py", label="👥 User Approval")
    st.sidebar.page_link("pages/5_User_Management.py", label="🛠 User Management")
    st.sidebar.page_link("pages/6_Site_Charts.py", label="📍 Site Charts")
    st.sidebar.page_link("pages/7_Help_and_Manual.py", label="📖 Help and Manual")
    st.sidebar.page_link("pages/8_Notifications.py", label="🔔 Notifications")

    st.sidebar.markdown("---")
    st.sidebar.caption("Made with ❤️ for GEG-ZAS")
