from db import load_payments, save_payments
from datetime import datetime

dummy_payment = {
    "contractor": "Test Contractor Inc.",
    "amount": 1250.75,
    "work_period": "2025-03-01 to 2025-03-15",
    "submitted_by": "ammar.muhammed@geg-construction.com",
    "submitted_at": datetime.now().isoformat(),
    "description": "Test payment for development",
    "status": "Pending",
    "reviewed_by": ""
}

# Load existing payments, append the dummy one, and save
payments = load_payments()
payments.append(dummy_payment)
save_payments(payments)

print("✅ Dummy payment added.")
