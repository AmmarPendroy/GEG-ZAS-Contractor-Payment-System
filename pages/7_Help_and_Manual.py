import streamlit as st
from auth import get_current_user
from utils.sidebar import render_sidebar

st.set_page_config(page_title="Help & Manual", page_icon="❓")

user = get_current_user()
if not user:
    st.warning("🔒 Login required.")
    st.stop()

render_sidebar()
st.title("📘 GEG-ZAS Help & Manual")

st.markdown("""
Welcome to the official user guide for the **GEG-ZAS Contractor Payment System**.

---

### 📝 How to Submit a Payment Request
- Go to **"Payment Request"** in the sidebar.
- Fill in contractor name, amount, work period, description.
- Upload required files (invoices, photos).
- Click **"Submit"** — HQ will be notified.

---

### ✅ Approving Requests (HQ only)
- Open **"Approval Page"**.
- View details and attachments.
- Choose **Approve**, **Reject**, or **Return with comment**.

---

### 📊 Dashboard
- Track payment trends by contractor or site.
- Filter by status, date, user, or project.
- Export Excel/PDF files.

---

### 👥 Manage Users (HQ Admin only)
- Approve new registrations.
- Change passwords.
- Remove inactive accounts.

---

If you face any issues, contact HQ IT team.
""")
