def send_approval_request_email(username, email, role, password):
    service = authenticate_gmail()
    subject = "🆕 New User Registration Request"
    body = f"""
Hello Admin,

A new user has requested to register on the GEG-ZAS System:

👤 Name: {username}
📧 Email: {email}
🛠️ Role: {role}

Please approve or reject this request in the system admin panel.

Temporary Password: {password} (Please hash securely if approved)

You can optionally leave a comment and confirm your decision.

Regards,
GEG-ZAS System
"""
    send_email(service, "ammar.muhammed@geg-construction.com", subject, body)
