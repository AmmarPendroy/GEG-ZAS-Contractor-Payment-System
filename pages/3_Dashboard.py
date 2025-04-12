import streamlit as st
import sqlite3
import pandas as pd
from auth import get_current_user

user = get_current_user()
if not user:
    st.warning("Please login to view the dashboard.")
    st.stop()

st.title("📊 GEG-ZAS Payment Dashboard")
st.header("GEG-ZAS Contractor Payment System")

conn = sqlite3.connect("database.db")
df = pd.read_sql_query("SELECT * FROM payment_requests", conn)
conn.close()

st.subheader("Summary Table")
summary = df.groupby(["contractor", "status"]).agg({"amount": "sum"}).unstack(fill_value=0)
st.dataframe(summary)

st.subheader("Request Status Breakdown")
st.metric("Pending", df[df["status"] == "Pending"].shape[0])
st.metric("Approved", df[df["status"] == "Approved"].shape[0])
st.metric("Rejected", df[df["status"] == "Rejected"].shape[0])
