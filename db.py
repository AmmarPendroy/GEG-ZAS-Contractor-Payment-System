import json

# Path to your payments database
PAYMENTS_FILE = "payments.json"

def load_payments():
    try:
        with open(PAYMENTS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_payments(payments):
    with open(PAYMENTS_FILE, "w") as f:
        json.dump(payments, f, indent=4)
