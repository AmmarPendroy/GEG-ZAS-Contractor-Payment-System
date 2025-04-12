import os
import json
from datetime import datetime

DATA_FILE = "payments.json"

def load_payments():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_payments(payments):
    with open(DATA_FILE, "w") as f:
        json.dump(payments, f, indent=2)

def submit_payment_request(contractor, description, work_period, amount, email, files):
    payments = load_payments()
    upload_dir = f"uploads/{email.replace('@', '_')}/"
    os.makedirs(upload_dir, exist_ok=True)

    file_paths = []
    for file in files:
        filepath = os.path.join(upload_dir, file.name)
        with open(filepath, "wb") as out:
            out.write(file.read())
        file_paths.append(filepath)

    payments.append({
        "contractor": contractor,
        "description": description,
        "work_period": work_period,
        "amount": amount,
        "submitted_by": email,
        "attachments": file_paths,
        "status": "Pending",
        "submitted_at": datetime.now().isoformat()
    })

    save_payments(payments)
