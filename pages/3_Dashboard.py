import streamlit as st
import pandas as pd
import plotly.express as px
from db import load_payments
from auth import get_current_user, get_all_users
from datetime import datetime
from io import BytesIO
import base64
from fpdf import FPDF
from utils.sidebar import render_sidebar

st.set_page_config(page_title="Dashboard", page_icon="📊")

user = get_current_user()
if not user:
    st.warning("🔒 Login required.")
    st.stop()

render_sidebar()
st.title("📊 Payment Dashboard")

# Load data
df = pd.DataFrame(load_payments())
users = {u["email"]: u for u in get_all_users()}
role = users.get(user, {}).get("role", "")

if df.empty:
    st.info("No payment data available.")
    st.stop()

df["submitted_at"] = pd.to_datetime(df["submitted_at"])
df["month"] = df["submitted_at"].dt.strftime("%B %Y")

# Filter for non-admins
if not role.startswith("hq_") and not role == "super_admin":
    df = df[df["submitted_by"] == user]

# Sidebar filters
with st.sidebar:
    st.header("🔍 Filters")
    contractor = st.selectbox("🏗️ Contractor", ["All"] + sorted(df["contractor"].unique()))
    status_filter = st.multiselect("📌 Status", options=df["status"].unique(), default=df["status"].unique())
    date_range = st.date_input("📅 Submission Range", [])

if contractor != "All":
    df = df[df["contractor"] == contractor]
if status_filter:
    df = df[df["status"].isin(status_filter)]
if len(date_range) == 2:
    start, end = pd.to_datetime(date_range)
    df = df[(df["submitted_at"] >= start) & (df["submitted_at"] <= end)]

# Metrics
st.subheader("📌 Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Total Requests", len(df))
col2.metric("Approved", len(df[df["status"] == "Approved"]))
col3.metric("Pending", len(df[df["status"] == "Pending"]))

# Chart
st.subheader("📈 Payment Status Breakdown")
chart_data = df["status"].value_counts().reset_index()
chart_data.columns = ["Status", "Count"]
fig = px.pie(chart_data, names="Status", values="Count", hole=0.4)
st.plotly_chart(fig, use_container_width=True)

# Export buttons
st.markdown("### 📁 Export Filtered Reports")

excel_buffer = BytesIO()
df.to_excel(excel_buffer, index=False)
b64_excel = base64.b64encode(excel_buffer.getvalue()).decode()
st.markdown(f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64_excel}" download="filtered_payments.xlsx">📥 Download Excel</a>', unsafe_allow_html=True)

# Full report (for admins only)
if role in ["hq_admin", "hq_project_director", "super_admin"]:
    st.markdown("---")
    st.subheader("📤 Download All Reports (Admin Only)")

    full_df = pd.DataFrame(load_payments())
    all_buffer = BytesIO()
    full_df.to_excel(all_buffer, index=False)
    b64_all = base64.b64encode(all_buffer.getvalue()).decode()
    st.markdown(f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64_all}" download="all_payments.xlsx">📥 Download All Payments</a>', unsafe_allow_html=True)
