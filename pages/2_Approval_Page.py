import streamlit as st
from db import load_payments, save_payments
from utils.sidebar import render_sidebar

render_sidebar()
st.title("✅ Approval Page")

payments = load_payments()
pending = [p for p in payments if p["status"] == "Pending"]

if not pending:
    st.info("No pending payments.")
else:
    for i, p in enumerate(pending):
        with st.expander(f"{p['contractor']} - ${p['amount']}"):
            st.write(f"Submitted by: {p['submitted_by']}")
            st.write(f"Work Period: {p['work_period']}")
            st.write(f"Description: {p['description']}")
            col1, col2 = st.columns(2)
            if col1.button("Approve", key=f"a_{i}"):
                p["status"] = "Approve"
                p["reviewed_by"] = "admin"
                save_payments(payments)
                st.success("Approved.")
                st.experimental_rerun()
            if col2.button("Reject", key=f"r_{i}"):
                p["status"] = "Reject"
                p["reviewed_by"] = "admin"
                save_payments(payments)
                st.error("Rejected.")
                st.experimental_rerun()
