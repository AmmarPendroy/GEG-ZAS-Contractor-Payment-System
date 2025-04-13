import json
import hashlib
import os

USER_DB_FILE = "user_db.json"

def load_users():
    if os.path.exists(USER_DB_FILE):
        with open(USER_DB_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USER_DB_FILE, "w") as f:
        json.dump(users, f, indent=2)
        print("✅ Changes saved.")

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def list_users():
    users = load_users()
    if not users:
        print("No users found.")
        return
    for email, data in users.items():
        print(f"- {email} | Role: {data['role']} | Approved: {data.get('approved', False)}")

def add_or_update_user():
    email = input("Enter user email: ").strip()
    password = input("Enter password: ").strip()
    role = input("Enter role (hq_project_director, hq_admin, hq_accountant, zas_pm, zas_accountant): ").strip()
    approved = input("Approve now? (y/n): ").lower().startswith("y")

    users = load_users()
    users[email] = {
        "password": hash_password(password),
        "role": role,
        "approved": approved
    }
    save_users(users)
    print(f"✅ User '{email}' added/updated.")

def approve_user():
    email = input("Enter user email to approve: ").strip()
    users = load_users()
    if email in users:
        users[email]["approved"] = True
        save_users(users)
        print(f"✅ User '{email}' approved.")
    else:
        print("❌ User not found.")

def reject_user():
    email = input("Enter user email to reject/delete: ").strip()
    users = load_users()
    if email in users:
        del users[email]
        save_users(users)
        print(f"🗑️ User '{email}' removed.")
    else:
        print("❌ User not found.")

def reset_password():
    email = input("Enter user email: ").strip()
    new_pass = input("Enter new password: ").strip()
    users = load_users()
    if email in users:
        users[email]["password"] = hash_password(new_pass)
        save_users(users)
        print(f"🔐 Password for '{email}' reset.")
    else:
        print("❌ User not found.")

def menu():
    while True:
        print("\n=== GEG-ZAS User Manager ===")
        print("1. List users")
        print("2. Add or update user")
        print("3. Approve user")
        print("4. Reject/delete user")
        print("5. Reset password")
        print("0. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            list_users()
        elif choice == "2":
            add_or_update_user()
        elif choice == "3":
            approve_user()
        elif choice == "4":
            reject_user()
        elif choice == "5":
            reset_password()
        elif choice == "0":
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    menu()
