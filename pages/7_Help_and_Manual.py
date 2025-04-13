import streamlit as st
from utils.sidebar import render_sidebar

render_sidebar()
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
- You will see toast notifications for new activity.

---

For any questions, contact the GEG-ZAS System Admin.
""")
