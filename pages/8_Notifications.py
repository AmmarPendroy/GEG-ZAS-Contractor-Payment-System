import streamlit as st
from utils.sidebar import render_sidebar
from utils.taskbar import render_taskbar

render_sidebar()
render_taskbar()
st.title("🔔 Notifications")

st.info("In-app notifications appear here when enabled (coming soon).")
