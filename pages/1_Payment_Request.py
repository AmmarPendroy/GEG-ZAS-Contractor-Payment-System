import streamlit as st
from auth import get_current_user
from db import submit_payment_request

user = get_current_user()
if not user or not user["role"].startswith("site"):
    st.warning("You must be a site user to access this page.")
    st.stop()

st.title("📝 Submit Contractor Payment Request")
st.header("GEG-ZAS Contractor Payment System")

with st.form("payment_form"):
    contractor = st.text_input("Contractor Name")
    description = st.text_area("Work Description")
    work_period = st.text_input("Work Period")
    amount = st.number_input("Amount Requested", min_value=0.0)
    files = st.file_uploader("Attachments", accept_multiple_files=True)
    submitted = st.form_submit_button("Submit Request")

    if submitted:
        submit_payment_request(contractor, description, work_period, amount, user["email"], files)
        st.success("Payment request submitted!")
