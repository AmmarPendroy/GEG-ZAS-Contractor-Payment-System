import streamlit as st
from db import submit_payment_request
from auth import get_current_user, get_all_users
from datetime import datetime
from utils.sidebar import render_sidebar
from utils.emailer import send_email, authenticate_gmail

user = get_current_user()
if not user:
    st.warning("Login required.")
    st.stop()

render_sidebar()
st.title("📝 Payment Request")

contractor = st.text_input("Contractor Name")
amount = st.number_input("Amount", min_value=0.0, format="%.2f")
work_period = st.text_input("Work Period")
description = st.text_area("Description")

if st.button("Submit Payment Request"):
    if contractor and amount and work_period:
        payment = {
            "contractor": contractor,
            "amount": amount,
            "work_period": work_period,
            "submitted_by": user,
            "submitted_at": datetime.now().isoformat(),
            "description": description,
            "status": "Pending",
            "reviewed_by": ""
        }
        submit_payment_request(payment)
        st.success("Payment request submitted successfully!")

        # 📧 Notify HQ roles
        all_users = get_all_users()
        hq_emails = [u["email"] for u in all_users if u["role"] in ["hq_admin", "hq_project_director"] and u["approved"].lower() == "true"]
        email_service = authenticate_gmail()
        for to_email in hq_emails:
            subject = "📥 New Payment Submission"
            body = f"""Hello,

A new payment request has been submitted.

Contractor: {contractor}
Amount: ${amount}
Submitted by: {user}

Please review it on the approval page.

Regards,
GEG-ZAS Payment System
"""
            send_email(email_service, to_email, subject, body)

    else:
        st.error("Please fill all required fields.")
