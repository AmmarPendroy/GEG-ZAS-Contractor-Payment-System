import streamlit as st
import pandas as pd
from db import load_payments
from auth import get_current_user
from datetime import datetime

user = get_current_user()
if not user:
    st.warning("Login required.")
    st.stop()

st.title("📊 Dashboard")

payments = load_payments()
df = pd.DataFrame(payments)

if df.empty:
    st.info("No data yet.")
else:
    df["submitted_at"] = pd.to_datetime(df["submitted_at"])
    df["week"] = df["submitted_at"].dt.strftime("%Y-W%U")
    df["month"] = df["submitted_at"].dt.strftime("%B")

    summary = df.groupby("contractor").agg({
        "amount": ["sum"],
        "week": lambda x: df.loc[x.index].groupby("week")["amount"].sum().max(),
        "month": lambda x: df.loc[x.index].groupby("month")["amount"].sum().max()
    })

    st.dataframe(summary)

    st.markdown("### Status Summary")
    st.write(f"🕒 Pending: {len(df[df['status'] == 'Pending'])}")
    st.write(f"✅ Approved: {len(df[df['status'] == 'Approve'])}")
    st.write(f"❌ Rejected/Returned: {len(df[df['status'].isin(['Reject', 'Return'])])}")
