import streamlit as st
from db import submit_payment_request
from auth import get_current_user
from datetime import datetime
from utils.sidebar import render_sidebar

st.set_page_config(page_title="Submit Payment", page_icon="📝")

user = get_current_user()
if not user:
    st.warning("🔒 You must log in to submit a payment.")
    st.stop()

render_sidebar()

st.title("📝 Submit a Payment Request")
st.caption("For ZAS Site Project Teams")

with st.form("payment_form"):
    contractor = st.text_input("🏗️ Contractor Name", placeholder="e.g. Sunrise Subcontractors")
    amount = st.number_input("💵 Amount (USD)", min_value=0.0, step=100.0, format="%.2f")
    work_period = st.text_input("🗓️ Work Period", placeholder="e.g. 2025-04-01 to 2025-04-15")
    description = st.text_area("📝 Description of Work")
    attachments = st.file_uploader("📎 Upload Documents", accept_multiple_files=True)

    submitted = st.form_submit_button("📤 Submit Request")

if submitted:
    if contractor and amount > 0 and work_period:
        files_info = [f.name for f in attachments] if attachments else []
        payment = {
            "contractor": contractor,
            "amount": amount,
            "work_period": work_period,
            "submitted_by": user,
            "submitted_at": datetime.now().isoformat(),
            "description": description,
            "status": "Pending",
            "reviewed_by": "",
            "attachments": files_info
        }
        submit_payment_request(payment)

        st.toast("📤 Payment submitted successfully!", icon="✅")
    else:
        st.error("⚠️ Please complete all required fields.")
