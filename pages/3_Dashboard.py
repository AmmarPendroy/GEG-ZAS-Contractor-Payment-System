import streamlit as st
import pandas as pd
from db import load_payments
from auth import get_current_user, get_all_users
from datetime import datetime
from io import BytesIO
import base64
from fpdf import FPDF
from utils.sidebar import render_sidebar

user = get_current_user()
users = get_all_users()
role = users.get(user, {}).get("role")

if not user:
    st.warning("Login required.")
    st.stop()

render_sidebar()
st.title("📊 Dashboard")

payments = load_payments()
df = pd.DataFrame(payments)

if df.empty:
    st.info("No data yet.")
    st.stop()

# Show in-app notification (last update for the current user)
user_updates = df[(df["submitted_by"] == user) & (df["status"] != "Pending")]
if not user_updates.empty:
    latest = user_updates.sort_values(by="submitted_at", ascending=False).iloc[0]
    status = latest["status"]
    reviewed_by = latest.get("reviewed_by", "")
    comment = latest.get("comment", "")
    st.info(f"🔔 Your recent request was **{status.upper()}** by {reviewed_by}.")
    if status == "Return" and comment:
        st.warning(f"💬 Comment from reviewer: *{comment}*")

# Restrict view to own submissions for ZAS roles
if role in ["zas_pm", "zas_accountant"]:
    df = df[df["submitted_by"] == user]

# Convert and enrich dates
df["submitted_at"] = pd.to_datetime(df["submitted_at"])
df["week"] = df["submitted_at"].dt.strftime("%Y-W%U")
df["month"] = df["submitted_at"].dt.strftime("%B")

# Summary table
summary = df.groupby("contractor").agg({
    "amount": ["sum"],
    "week": lambda x: df.loc[x.index].groupby("week")["amount"].sum().max(),
    "month": lambda x: df.loc[x.index].groupby("month")["amount"].sum().max()
})

st.subheader("💼 Contractor Summary")
st.dataframe(summary)

# Status counts
st.subheader("📌 Status Summary")
st.write(f"🕒 Pending: {len(df[df['status'] == 'Pending'])}")
st.write(f"✅ Approved: {len(df[df['status'] == 'Approve'])}")
st.write(f"❌ Rejected/Returned: {len(df[df['status'].isin(['Reject', 'Return'])])}")

# Export section
st.markdown("---")
st.subheader("🧾 Export Reports")

excel_buffer = BytesIO()
df.to_excel(excel_buffer, index=False, sheet_name="Payments")
excel_data = excel_buffer.getvalue()
b64_excel = base64.b64encode(excel_data).decode()
st.markdown(f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64_excel}" download="payments.xlsx">📥 Download Excel Report</a>', unsafe_allow_html=True)

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Payment Summary Report", ln=True, align="C")

    def chapter_title(self, title):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, title, ln=True)

    def chapter_body(self, text):
        self.set_font("Arial", "", 10)
        self.multi_cell(0, 10, text)

pdf = PDF()
pdf.add_page()
pdf.chapter_title("Submitted Payments")

for _, row in df.iterrows():
    text = f"Contractor: {row['contractor']}\nAmount: ${row['amount']}\nStatus: {row['status']}\nDescription: {row['description']}\nWork Period: {row['work_period']}\nSubmitted By: {row['submitted_by']}\nDate: {row['submitted_at'].strftime('%Y-%m-%d')}\n"
    pdf.chapter_body(text + "\n---------------------\n")

pdf_buffer = BytesIO()
pdf.output(pdf_buffer)
pdf_data = pdf_buffer.getvalue()
b64_pdf = base64.b64encode(pdf_data).decode()
st.markdown(f'<a href="data:application/pdf;base64,{b64_pdf}" download="payments_report.pdf">📥 Download PDF Report</a>', unsafe_allow_html=True)
