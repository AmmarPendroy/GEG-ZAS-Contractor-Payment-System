import streamlit as st
import pandas as pd
from db import load_payments, save_payments
from auth import get_current_user
from utils.emailer import send_approval_email

st.title("📤 Payment Approval Page")

user = get_current_user()
if not user:
    st.warning("Please log in to access this page.")
    st.stop()

payments = load_payments()
df = pd.DataFrame(payments)

if df.empty:
    st.info("No payment requests to review.")
    st.stop()

# Filter pending payments only
pending_df = df[df['status'] == 'Pending']
if pending_df.empty:
    st.success("🎉 No pending payments.")
    st.stop()

selected_index = st.selectbox("Select a request to review:", pending_df.index)
selected = df.loc[selected_index]

st.subheader("Request Details")
st.write(f"**Contractor:** {selected['contractor']}")
st.write(f"**Amount:** ${selected['amount']}")
st.write(f"**Work Period:** {selected['work_period']}")
st.write(f"**Submitted By:** {selected['submitted_by']}")
st.write(f"**Description:** {selected['description']}")
st.write(f"**Submitted At:** {selected['submitted_at']}")

action = st.radio("Action", ["Approve", "Reject", "Return"], horizontal=True)

if st.button("Submit Action"):
    df.at[selected_index, 'status'] = action
    df.at[selected_index, 'reviewed_by'] = user["email"]

    save_payments(df.to_dict(orient="records"))

    # Send notification email to the original submitter
    subject = f"Payment Request {action} - {selected['contractor']}"
    body = f"""
    Hello {selected['submitted_by']},

    Your contractor payment request has been **{action}** by {user['email']}.

    🧾 Details:
    - Contractor: {selected['contractor']}
    - Amount: ${selected['amount']}
    - Work Period: {selected['work_period']}
    - Description: {selected['description']}

    Please log in to the GEG-ZAS Contractor Payment System for more details.
    """

    try:
        send_approval_email(to=selected['submitted_by'], subject=subject, body=body)
        st.success(f"Payment {action} and email sent to {selected['submitted_by']}.")
    except Exception as e:
        st.warning(f"Payment {action}, but failed to send email: {e}")
