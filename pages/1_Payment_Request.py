import streamlit as st
from sidebar import show_sidebar

if "user" not in st.session_state:
    st.error("Please log in to access this page.")
    st.stop()

show_sidebar()



# 1_Payment_Request.py
import streamlit as st
from db import submit_payment_request
from datetime import datetime

# Form for submitting a payment request
st.title("Submit Payment Request")

contractor = st.text_input("Contractor Name")
amount = st.number_input("Amount", min_value=0.0)
work_period = st.text_input("Work Period")
description = st.text_area("Description")
submitted_by = st.text_input("Your Email")

if st.button("Submit Payment Request"):
    if contractor and amount and work_period and description and submitted_by:
        payment_data = {
            "contractor": contractor,
            "amount": amount,
            "work_period": work_period,
            "submitted_by": submitted_by,
            "submitted_at": datetime.now().isoformat(),
            "description": description,
            "status": "Pending",
            "reviewed_by": ""
        }

        # Submit the payment request
        if submit_payment_request(payment_data):
            st.success("Payment request submitted successfully!")
        else:
            st.error("Error submitting payment request.")
    else:
        st.error("Please fill out all the fields.")
