import streamlit as st
import sqlite3
from auth import get_current_user

def fetch_requests():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT id, contractor, description, amount, status, submitted_by FROM payment_requests WHERE status = 'Pending'")
    rows = cur.fetchall()
    conn.close()
    return rows

def update_request_status(request_id, status):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("UPDATE payment_requests SET status = ? WHERE id = ?", (status, request_id))
    conn.commit()
    conn.close()

user = get_current_user()
if not user or not user["role"].startswith("hq"):
    st.warning("Only HQ users can access this page.")
    st.stop()

st.title("📋 HQ Approval Page")
st.header("GEG-ZAS Contractor Payment System")

requests = fetch_requests()

if requests:
    for req in requests:
        with st.expander(f"{req[1]} | {req[2]} | ${req[3]}"):
            st.write(f"**Submitted by**: {req[5]}")
            col1, col2, _ = st.columns(3)
            if col1.button("✅ Approve", key=f"approve_{req[0]}"):
                update_request_status(req[0], "Approved")
                st.success("Approved.")
                st.rerun()
            if col2.button("❌ Reject", key=f"reject_{req[0]}"):
                update_request_status(req[0], "Rejected")
                st.error("Rejected.")
                st.rerun()
else:
    st.info("No pending requests.")
