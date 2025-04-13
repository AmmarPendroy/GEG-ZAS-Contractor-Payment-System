import streamlit as st
from db import load_payments, save_payments
from auth import get_current_user, get_all_users
from utils.sidebar import render_sidebar

user = get_current_user()
if not user:
    st.warning("Login required.")
    st.stop()

users = get_all_users()
role = users.get(user, {}).get("role")

render_sidebar()
st.title("✅ Approval Page")

if role not in ["hq_admin", "hq_project_director"]:
    st.error("Access denied. Only HQ Admin or HQ Project Director can review payments.")
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
            if "attachments" in p:
                for f in p["attachments"]:
                    st.markdown(f"[📎 {os.path.basename(f)}](/{f})", unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)

            if col1.button("Approve", key=f"a_{i}"):
                p["status"] = "Approve"
                p["reviewed_by"] = user
                save_payments(payments)
                st.success("Approved.")
                st.experimental_rerun()

            if col2.button("Reject", key=f"r_{i}"):
                p["status"] = "Reject"
                p["reviewed_by"] = user
                save_payments(payments)
                st.error("Rejected.")
                st.experimental_rerun()

            with col3:
                with st.form(key=f"return_form_{i}"):
                    comment = st.text_area("Return with comment")
                    submit_return = st.form_submit_button("Return")
                    if submit_return:
                        p["status"] = "Return"
                        p["reviewed_by"] = user
                        p["comment"] = comment
                        save_payments(payments)
                        st.warning("Returned with comment.")
                        st.experimental_rerun()
