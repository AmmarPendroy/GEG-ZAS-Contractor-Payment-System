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

# Load payments and users
df = pd.DataFrame(load_payments())
users = {u["email"]: u for u in get_all_users()}
role = users.get(user, {}).get("role", "")

# Guard: no data
if df.empty:
    st.info("No payment data available yet.")
    st.stop()

# Format timestamps
df["submitted_at"] = pd.to_datetime(df["submitted_at"])
df["week"] = df["submitted_at"].dt.strftime("%Y-W%U")
df["month"] = df["submitted_at"].dt.strftime("%B %Y")

# Role-based filtering
if not role.startswith("hq_") and not role == "super_admin":
    df = df[df["submitted_by"] == user]

# Sidebar filters
with st.sidebar:
    st.header("🔍 Filters")
    contractor = st.selectbox("🏗️ Contractor", ["All"] + sorted(df["contractor"].unique()))
    status_filter = st.multiselect("📌 Status", options=df["status"].unique(), default=df["status"].unique())
    date_range = st.date_input("📅 Submission Date Range", [])

# Apply filters
if contractor != "All":
    df = df[df["contractor"] == contractor]
if status_filter:
    df = df[df["status"].isin(status_filter)]
if len(date_range) == 2:
    start, end = pd.to_datetime(date_range)
    df = df[(df["submitted_at"] >= start) & (df["submitted_at"] <= end)]

# Metrics summary
st.subheader("📌 Summary")
col1, col2, col3 = st.columns(3)
col1.metric("🧾 Total Requests", len(df))
col2.metric("✅ Approved", len(df[df["status"] == "Approved"]))
col3.metric("🕒 Pending", len(df[df["status"] == "Pending"]))

# Chart
st.subheader("📈 Payment Status Breakdown")
chart_data = df["status"].value_counts().reset_index()
chart_data.columns = ["Status", "Count"]
fig = px.pie(chart_data, names="Status", values="Count", hole=0.4)
st.plotly_chart(fig, use_container_width=True)

# Export section
st.markdown("### 📁 Export Reports")

excel_buffer = BytesIO()
df.to_excel(excel_buffer, index=False)
b64_excel = base64.b64encode(excel_buffer.getvalue()).decode()
st.markdown(f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64_excel}" download="payments.xlsx">📥 Download Excel</a>', unsafe_allow_html=True)

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Payment Summary Report", ln=True, align="C")
    def chapter_body(self, text):
        self.set_font("Arial", "", 10)
        self.multi_cell(0, 10, text)

pdf = PDF()
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=15)

for _, row in df.iterrows():
    txt = (
        f"Contractor: {row['contractor']}\n"
        f"Amount: ${row['amount']}\n"
        f"Status: {row['status']}\n"
        f"Submitted by: {row['submitted_by']}\n"
        f"Period: {row['work_period']}\n"
        f"Date: {row['submitted_at'].strftime('%Y-%m-%d')}\n\n"
    )
    pdf.chapter_body(txt)

pdf_buffer = BytesIO()
pdf.output(pdf_buffer)
b64_pdf = base64.b64encode(pdf_buffer.getvalue()).decode()
st.markdown(f'<a href="data:application/pdf;base64,{b64_pdf}" download="payments.pdf">📥 Download PDF</a>', unsafe_allow_html=True)
