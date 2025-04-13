import streamlit as st
from utils.sidebar import render_sidebar

render_sidebar()
st.title("🔔 Notifications")

st.info("In-app notifications will appear here if enabled. This page is for viewing message history and alerts (coming soon).")
