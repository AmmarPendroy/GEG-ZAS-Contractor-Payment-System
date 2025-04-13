import streamlit as st
from auth import get_current_user
from utils.sidebar import render_sidebar

user = get_current_user()
render_sidebar()

st.title("📘 Help & User Manual")

st.markdown("""
Welcome to the **GEG-ZAS Contractor Payment System**. This guide will help you understand how to use the platform based on your role.

---

## 🧑‍💼 User Roles & Access

| Role                | Permissions |
|---------------------|-------------|
| **ZAS Project Manager** | Submit requests, view dashboard |
| **ZAS Accountant**      | Submit requests, view dashboard |
| **HQ Admin**            | Approve users, view/export all |
| **HQ Project Director** | Approve/reject/return payments |
| **HQ Accountant**       | View/export dashboard |

---

## 🔐 Login / Register

- Visit the homepage
- Register using a **@geg-construction.com** email
- Select your correct **role**
- Wait for **HQ Admin or Director approval**
- Login after approval

---

## 📝 Submit a Payment Request

1. Go to **"Payment Request"**
2. Fill in:
   - Contractor name
   - Amount
   - Work period
   - Description
3. Click **Submit**
4. HQ will receive an email and process it

---

## ✅ Approval Process (HQ Roles)

- Go to **"Approval Page"**
- View all pending requests
- You can:
  - ✅ Approve
  - ❌ Reject
  - 🔁 Return (comment feature coming soon)

---

## 📊 Dashboard

- View all payment history (filtered by your role)
- Use sidebar to filter by:
  - Contractor
  - Date range
- Export reports in:
  - 📄 Excel
  - 📄 PDF

---

## 🏗️ Site / Region Charts

- HQ users only
- Compare totals by site
- View monthly submission trends

---

## 👥 User Approval (HQ Admin)

- Go to **"User Approval"**
- View all pending users
- Approve or reject them

---

## 📩 Email Alerts

- You get emails when:
  - You submit a payment
  - Your request is approved/rejected
  - You log in or out

---

## 🧾 Logs

- All exports are logged in **`export_logs.csv`**
- All emails logged in **`sent_emails.csv`**

---

## ❓ Need Help?

Contact: **ammar.muhammed@geg-construction.com**

---
""")
