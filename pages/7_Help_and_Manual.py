import streamlit as st
from utils.sidebar import render_sidebar
from utils.taskbar import render_taskbar

render_sidebar()
render_taskbar()
st.title("📖 Help & Manual")

st.markdown("""
### 📤 Submitting a Payment
1. Go to **Payment Request** from the sidebar.
2. Fill in the contractor name, amount, period, and description.
3. Add attachments if required.
4. Submit your request.

---

### ✅ Approving Requests
1. Go to **Approval Page**.
2. Click to expand a request.
3. Approve or Reject.

---

### 📊 Dashboard
- See total payments, breakdowns by status and contractor.
- Export data as Excel or PDF.

---

### 🔔 Notifications
- Toast alerts for submission and approval appear at the bottom.

---

For help contact: ammar.muhammed@geg-construction.com
""")
