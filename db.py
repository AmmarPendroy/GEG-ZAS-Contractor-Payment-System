# db.py
import json
from datetime import datetime

# Function to load payments data from the payments.json file
def load_payments():
    try:
        with open("payments.json", "r") as f:
            payments = json.load(f)
        return payments
    except FileNotFoundError:
        return []

# Function to save payments data to the payments.json file
def save_payments(payments):
    with open("payments.json", "w") as f:
        json.dump(payments, f, indent=4)

# Function to submit a payment request
def submit_payment_request(payment_data):
    # Load existing payments
    payments = load_payments()

    # Append the new payment request to the list
    payments.append(payment_data)

    # Save updated payments to the JSON file
    save_payments(payments)

    return True
