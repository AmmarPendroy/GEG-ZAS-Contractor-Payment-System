import streamlit as st
from db import load_payments, save_payments
from auth import get_current_user
from utils.emailer import send_email

user = get_current_user()
if not user or user["role"] not in ["hq_admin", "hq_director"]:
    st.warning("Access restricted to HQ staff.")
    st.stop()

st.title("✅ Approve Contractor Payments")

payments = load_payments()
pending = [p for p in payments if p["status"] == "Pending"]

if not pending:
    st.info("No pending requests.")
else:
    for i, payment in enumerate(pending):
        with st.expander(f"{payment['contractor']} — ${payment['amount']} — {payment['description']}"):
            st.markdown(f"- **Submitted by:** {payment['submitted_by']}")
            st.markdown(f"- **Work Period:** {payment['work_period']}")
            st.markdown(f"- **Submitted At:** {payment['submitted_at']}")
            st.markdown("### Attachments:")
            for path in payment["attachments"]:
                st.markdown(f"- 📎 {path}")

            decision = st.radio(
                "Decision", ["Approve", "Reject", "Return"], key=f"decision_{i}"
            )
            comment = st.text_area("Comment (optional)", key=f"comment_{i}")

            if st.button("Submit Decision", key=f"submit_{i}"):
                payments[i]["status"] = decision
                payments[i]["comment"] = comment
                save_payments(payments)
                send_email(
                    to=payment["submitted_by"],
                    subject=f"Payment {decision}",
                    body=f"Your request for '{payment['description']}' has been {decision}.\n\nComment: {comment}"
                )
                st.success(f"Request marked as {decision}.")
                st.rerun()
