import streamlit as st
from db import load_payments, save_payments
from auth import get_current_user
from utils.emailer import send_approval_email
from datetime import datetime

st.title("✅ HQ Approval Page")

user = get_current_user()
if not user:
    st.warning("Login required.")
    st.stop()

payments = load_payments()

if not payments:
    st.info("No payment requests available.")
else:
    for i, p in enumerate(payments):
        if p["status"] == "Pending":
            with st.expander(f"{p['contractor']} - ${p['amount']}"):
                st.write(f"**Work Period:** {p['work_period']}")
                st.write(f"**Submitted by:** {p['submitted_by']}")
                st.write(f"**Submitted at:** {p['submitted_at']}")
                st.write(f"**Description:** {p['description']}")

                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("Approve", key=f"approve_{i}"):
                        payments[i]["status"] = "Approve"
                        payments[i]["reviewed_by"] = user
                        payments[i]["reviewed_at"] = datetime.now().isoformat()
                        save_payments(payments)
                        send_approval_email(p['submitted_by'], p['contractor'], p['amount'], "Approved")
                        st.success("Approved and email sent.")
                        st.experimental_rerun()

                with col2:
                    if st.button("Reject", key=f"reject_{i}"):
                        payments[i]["status"] = "Reject"
                        payments[i]["reviewed_by"] = user
                        payments[i]["reviewed_at"] = datetime.now().isoformat()
                        save_payments(payments)
                        send_approval_email(p['submitted_by'], p['contractor'], p['amount'], "Rejected")
                        st.warning("Rejected and email sent.")
                        st.experimental_rerun()

                with col3:
                    if st.button("Return", key=f"return_{i}"):
                        payments[i]["status"] = "Return"
                        payments[i]["reviewed_by"] = user
                        payments[i]["reviewed_at"] = datetime.now().isoformat()
                        save_payments(payments)
                        send_approval_email(p['submitted_by'], p['contractor'], p['amount'], "Returned")
                        st.info("Returned and email sent.")
                        st.experimental_rerun()
