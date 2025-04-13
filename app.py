import streamlit as st
from utils.sidebar import render_sidebar

st.set_page_config(page_title="Welcome | GEG-ZAS Payment System", layout="centered")

def main():
    render_sidebar()
    st.image("static/geg_logo.png", use_container_width=True)
    st.title("🏗️ Welcome to the GEG-ZAS Payment System")
    st.markdown("""
    ---
    This system helps streamline and monitor contractor payments across all GEG Construction sites, including ZAS.

    **Use the sidebar to:**
    - 📤 Submit or view payment requests
    - ✅ Approve or reject requests (HQ only)
    - 📊 Analyze dashboards and charts
    - 📖 Get help and system guidance

    ---
    All users can now explore the system without logging in.
    """)

if __name__ == "__main__":
    main()
