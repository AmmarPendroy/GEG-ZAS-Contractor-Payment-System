import streamlit as st
from db import load_payments, save_payments
from utils.emailer import send_email, create_github_issue
from datetime import datetime

# Simulate payment approval process
def approve_payment(payment_id):
    # Load payments
    payments = load_payments()
    
    # Find the payment by ID and update its status
    for payment in payments:
        if payment["id"] == payment_id:
            payment["status"] = "Approved"
            payment["reviewed_by"] = "ammar.muhammed@geg-construction.com"
            payment["reviewed_at"] = datetime.now().isoformat()
            break

    # Save the updated payments
    save_payments(payments)

    # Send email notification
    send_email(payment["submitted_by"], "Payment Approved", f"Your payment of ${payment['amount']} has been approved.")

    # Create GitHub issue for tracking
    create_github_issue()

    st.success(f"Payment {payment_id} has been approved successfully!")

# Streamlit UI for approval
st.title("Payment Approval Page")

payment_id = st.text_input("Enter Payment ID to approve:")

if st.button("Approve Payment"):
    if payment_id:
        approve_payment(payment_id)
    else:
        st.warning("Please provide a valid Payment ID.")
