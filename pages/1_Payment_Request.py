import streamlit as st
from auth import get_current_user
from db import submit_payment_request

user = get_current_user()
if not user:
    st.warning("Please login first.")
    st.stop()

st.title("💵 Submit Payment Request")

with st.form("payment_form"):
    contractor = st.text_input("Contractor Name")
    description = st.text_area("Work Description")
    work_period = st.text_input("Work Period")
    amount = st.number_input("Amount Requested", min_value=0.0)
    attachments = st.file_uploader("Upload Supporting Documents", accept_multiple_files=True)

    submitted = st.form_submit_button("Submit Request")

    if submitted:
        submit_payment_request(contractor, description, work_period, amount, user["email"], attachments)
        st.success("Request submitted successfully!")
