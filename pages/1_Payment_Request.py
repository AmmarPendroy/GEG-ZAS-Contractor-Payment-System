import streamlit as st
from db import submit_payment_request
from auth import get_current_user
from datetime import datetime
from utils.sidebar import render_sidebar

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
    else:
        st.error("Please fill all required fields.")
