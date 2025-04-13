import streamlit as st
from db import submit_payment_request
from auth import get_current_user
from datetime import datetime
from utils.sidebar import render_sidebar
import os
import shutil

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

uploaded_files = st.file_uploader("Upload Supporting Documents (PDFs, images, etc.)", type=["pdf", "png", "jpg", "jpeg", "docx", "xlsx"], accept_multiple_files=True)

if st.button("Submit Payment Request"):
    if contractor and amount and work_period:
        # Save uploaded files
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        folder_path = f"uploads/{user}/{timestamp}/"
        os.makedirs(folder_path, exist_ok=True)
        saved_files = []

        for file in uploaded_files:
            file_path = os.path.join(folder_path, file.name)
            with open(file_path, "wb") as f:
                shutil.copyfileobj(file, f)
            saved_files.append(file_path)

        payment = {
            "contractor": contractor,
            "amount": amount,
            "work_period": work_period,
            "submitted_by": user,
            "submitted_at": datetime.now().isoformat(),
            "description": description,
            "attachments": saved_files,
            "status": "Pending",
            "reviewed_by": "",
            "comment": ""
        }
        submit_payment_request(payment)
        st.success("Payment request submitted successfully!")
    else:
        st.error("Please fill all required fields.")
