import streamlit as st
from db import load_payments, save_payments
from utils.sidebar import render_sidebar
from utils.taskbar import render_taskbar

render_sidebar()
render_taskbar()
st.title("✅ Approval Page")

if st.session_state.get("role") not in ["hq_project_director", "hq_admin"]:
    st.warning("Access denied. This page is for HQ staff only.")
    st.stop()

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
                p["reviewed_by"] = st.session_state.username
                save_payments(payments)
                st.success("Approved.")
                st.rerun()
            if col2.button("Reject", key=f"r_{i}"):
                p["status"] = "Reject"
                p["reviewed_by"] = st.session_state.username
                save_payments(payments)
                st.error("Rejected.")
                st.rerun()
