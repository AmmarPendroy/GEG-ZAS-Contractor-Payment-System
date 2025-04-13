import streamlit as st

def render_sidebar():
    st.sidebar.markdown("# 📂 Navigation")
    st.sidebar.page_link("app.py", label="🏠 Home")
    st.sidebar.page_link("pages/1_Payment_Request.py", label="📝 Payment Request")
    st.sidebar.page_link("pages/2_Approval_Page.py", label="✅ Approval Page")
    st.sidebar.page_link("pages/3_Dashboard.py", label="📊 Dashboard")
    st.sidebar.page_link("pages/4_User_Approval.py", label="👥 User Approvals")

    if st.sidebar.button("🚪 Logout"):
        st.session_state.clear()
        st.experimental_rerun()
