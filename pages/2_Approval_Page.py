import streamlit as st
from db import load_payments, save_payments
from auth import get_current_user
from utils.sidebar import render_sidebar
from datetime import datetime

st.set_page_config(page_title="Approval Panel", page_icon="✅")

user = get_current_user()
if not user:
    st.warning("🔒 Login required to view this page.")
    st.stop()

render_sidebar()
st.title("✅ HQ Payment Approvals")
st.caption("Review and process payment requests")

payments = load_payments()
pending = [p for p in payments if p["status"] == "Pending"]

if not pending:
    st.info("✅ No pending requests at the moment.")
else:
    for i, p in enumerate(pending):
        with st.expander(f"🧾 {p['contractor']} - ${p['amount']} | Submitted by {p['submitted_by']}"):
            st.markdown(f"**📅 Work Period:** {p['work_period']}")
            st.markdown(f"**📝 Description:** {p['description']}")
            st.markdown(f"**📤 Submitted at:** {p['submitted_at']}")
            st.markdown("---")

            col1, col2, col3 = st.columns([1, 1, 2])

            # Approve button
            if col1.button("✅ Approve", key=f"approve_{i}"):
                p["status"] = "Approved"
                p["reviewed_by"] = user
                p["reviewed_at"] = datetime.now().isoformat()
                save_payments(payments)
                st.success("Payment approved.")
                st.experimental_rerun()

            # Reject button
            if col2.button("❌ Reject", key=f"reject_{i}"):
                p["status"] = "Rejected"
                p["reviewed_by"] = user
                p["reviewed_at"] = datetime.now().isoformat()
                save_payments(payments)
                st.error("Payment rejected.")
                st.experimental_rerun()

            # Return with comment
            with col3:
                return_msg = st.text_input("🔁 Return with comment", key=f"return_{i}")
                if st.button("Send Back", key=f"return_btn_{i}"):
                    if return_msg:
                        p["status"] = "Returned"
                        p["reviewed_by"] = user
                        p["reviewed_at"] = datetime.now().isoformat()
                        p["return_comment"] = return_msg
                        save_payments(payments)
                        st.warning(f"Returned with comment: {return_msg}")
                        st.experimental_rerun()
                    else:
                        st.error("Comment is required to return the request.")
