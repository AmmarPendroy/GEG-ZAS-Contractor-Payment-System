import streamlit as st
from db import submit_payment_request
from datetime import datetime
from utils.sidebar import render_sidebar

render_sidebar()
st.title("📝 Submit Payment Request")

contractor = st.text_input("Contractor Name")
amount = st.number_input("Amount", min_value=0.0, format="%.2f")
work_period = st.text_input("Work Period")
description = st.text_area("Description")
submitted_by = st.text_input("Your Name or Email")

if st.button("Submit Payment Request"):
    if contractor and amount and work_period and submitted_by:
        payment = {
            "contractor": contractor,
            "amount": amount,
            "work_period": work_period,
            "submitted_by": submitted_by,
            "submitted_at": datetime.now().isoformat(),
            "description": description,
            "status": "Pending",
            "reviewed_by": ""
        }
        submit_payment_request(payment)
        st.success("✅ Payment request submitted.")
    else:
        st.error("Please fill all required fields.")
