import streamlit as st
import pandas as pd
from db import load_payments
from auth import get_current_user, get_all_users
from datetime import datetime
from io import BytesIO
import base64
from fpdf import FPDF
import plotly.express as px
from utils.sidebar import render_sidebar

# Auth check
user = get_current_user()
if not user:
    st.warning("Login required.")
    st.stop()

render_sidebar()
st.title("📊 Dashboard")

# Get current user's role
users = get_all_users()
user_data = next((u for u in users if u["email"] == user), None)
role = user_data["role"] if user_data else "unknown"

# Load payments
payments = load_payments()
df = pd.DataFrame(payments)

if df.empty:
    st.info("No data available.")
    st.stop()

# Handle timestamps
df["submitted_at"] = pd.to_datetime(df["submitted_at"])
df["month"] = df["submitted_at"].dt.strftime("%Y-%m")
df["week"] = df["submitted_at"].dt.strftime("%Y-W%U")

# Role filter: site users only see their data
if role.startswith("zas_"):
    df = df[df["submitted_by"] == user]

# 📍 New Entry Notification
if "last_check" not in st.session_state:
    st.session_state["last_check"] = datetime.now()
else:
    new_entries = df[df["submitted_at"] > st.session_state["last_check"]]
    if not new_entries.empty:
        st.success(f"🔔 {len(new_entries)} new payment(s) since your last visit.")
    st.session_state["last_check"] = datetime.now()

# 📊 Charts
st.subheader("📌 Monthly Total per Contractor")
monthly_summary = df.groupby(["month", "contractor"])["amount"].sum().reset_index()
fig1 = px.bar(monthly_summary, x="month", y="amount", color="contractor", barmode="group")
st.plotly_chart(fig1, use_container_width=True)

st.subheader("📌 Status Distribution")
fig2 = px.pie(df, names="status", title="Payment Status Distribution", hole=0.4)
st.plotly_chart(fig2, use_container_width=True)

# 📊 Total summary
st.subheader("📋 Summary Table")
summary = df.groupby("contractor").agg({
    "amount": "sum",
    "status": "count"
}).rename(columns={"status": "requests"})
st.dataframe(summary)

# 📥 Export buttons
st.markdown("### 🧾 Export Filtered Reports")

filtered_df = df.copy()  # filtered already by role

# Excel
excel_buffer = BytesIO()
filtered_df.to_excel(excel_buffer, index=False)
excel_data = excel_buffer.getvalue()
b64_excel = base64.b64encode(excel_data).decode()
st.markdown(f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64_excel}" download="payments.xlsx">📥 Download Excel</a>', unsafe_allow_html=True)

# PDF
class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Payment Summary Report", ln=True, align="C")

    def chapter_body(self, text):
        self.set_font("Arial", "", 10)
        self.multi_cell(0, 10, text)

pdf = PDF()
pdf.add_page()
for _, row in filtered_df.iterrows():
    body = (
        f"Contractor: {row['contractor']}\n"
        f"Amount: ${row['amount']}\n"
        f"Status: {row['status']}\n"
        f"Description: {row['description']}\n"
        f"Work Period: {row['work_period']}\n"
        f"Submitted By: {row['submitted_by']}\n"
        f"Date: {row['submitted_at'].strftime('%Y-%m-%d')}\n"
        "-------------------------\n"
    )
    pdf.chapter_body(body)

pdf_buffer = BytesIO()
pdf.output(pdf_buffer)
pdf_data = pdf_buffer.getvalue()
b64_pdf = base64.b64encode(pdf_data).decode()
st.markdown(f'<a href="data:application/pdf;base64,{b64_pdf}" download="payments.pdf">📥 Download PDF</a>', unsafe_allow_html=True)
