import streamlit as st
from db import submit_payment_request
from datetime import datetime
from utils.sidebar import render_sidebar
from utils.taskbar import render_taskbar

render_sidebar()
render_taskbar()
st.title("📝 Submit Payment Request")

user = st.session_state.get("username", "anonymous")

contractor = st.text_input("Contractor Name")
amount = st.number_input("Amount", min_value=0.0, format="%.2f")
work_period = st.text_input("Work Period")
description = st.text_area("Description")

if st.button("Submit Payment Request"):
    if contractor and amount and work_period and user:
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
        st.success("✅ Payment request submitted.")
    else:
        st.error("Please fill all required fields.")
