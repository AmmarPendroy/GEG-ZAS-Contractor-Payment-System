import streamlit as st
import pandas as pd
from db import load_payments
from auth import get_current_user, get_all_users
from utils.sidebar import render_sidebar
from datetime import datetime

st.set_page_config(page_title="Notifications", page_icon="🔔")

user = get_current_user()
if not user:
    st.warning("🔒 Login required.")
    st.stop()

render_sidebar()
st.title("🔔 Notifications")

# Load data
df = pd.DataFrame(load_payments())
users = {u["email"]: u for u in get_all_users()}
role = users.get(user, {}).get("role", "")

# Show user-relevant requests or all (for admin)
if role.startswith("hq_") or role == "super_admin":
    notifications = df[df["status"].isin(["Approved", "Rejected", "Returned"])]
else:
    notifications = df[(df["submitted_by"] == user) & df["status"].isin(["Approved", "Rejected", "Returned"])]

# Sort by time
notifications["submitted_at"] = pd.to_datetime(notifications["submitted_at"])
notifications = notifications.sort_values(by="submitted_at", ascending=False)

if notifications.empty:
    st.info("No updates yet.")
else:
    for _, row in notifications.iterrows():
        with st.expander(f"{row['contractor']} • ${row['amount']} • {row['status']}"):
            st.markdown(f"📅 **Submitted**: {row['submitted_at'].strftime('%Y-%m-%d %H:%M')}")
            st.markdown(f"👤 **Submitted by**: `{row['submitted_by']}`")
            st.markdown(f"👨‍⚖️ **Reviewed by**: `{row.get('reviewed_by', '—')}`")
            st.markdown(f"📝 **Description**: {row['description']}")
            if row["status"] == "Returned" and "return_comment" in row:
                st.warning(f"🔁 **Return Comment**: {row['return_comment']}")
