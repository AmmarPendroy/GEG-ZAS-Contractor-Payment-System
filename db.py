import json

def load_payments():
    """Load payments from a JSON file"""
    try:
        with open('payments.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_payments(payments):
    """Save payments to a JSON file"""
    with open('payments.json', 'w') as f:
        json.dump(payments, f, indent=4)
