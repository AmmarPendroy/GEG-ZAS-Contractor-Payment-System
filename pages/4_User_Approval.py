import streamlit as st
from auth import get_current_user, get_all_users, approve_user, reject_user
import pandas as pd
import base64

user = get_current_user()
if not user or user["role"] != "hq_admin":
    st.warning("Only HQ Admins can access this page.")
    st.stop()

st.title("👥 User Approval Management")

users = get_all_users()
pending_users = {k: v for k, v in users.items() if not v.get("approved", False)}

if pending_users:
    for email, data in pending_users.items():
        with st.expander(f"{email} – Role: {data['role']}"):
            col1, col2 = st.columns(2)
            if col1.button("✅ Approve", key=f"approve_{email}"):
                approve_user(email)
                st.success(f"Approved {email}")
                st.rerun()
            if col2.button("❌ Reject", key=f"reject_{email}"):
                reject_user(email)
                st.warning(f"Rejected {email}")
                st.rerun()
else:
    st.info("No users pending approval.")

# Export database
st.markdown("---")
df = pd.DataFrame.from_dict(users, orient='index').reset_index()
df.columns = ['Email', 'Password', 'Role', 'Approved']
csv = df.to_csv(index=False)
b64 = base64.b64encode(csv.encode()).decode()
st.markdown(f'<a href="data:file/csv;base64,{b64}" download="user_database.csv">Download CSV</a>', unsafe_allow_html=True)
