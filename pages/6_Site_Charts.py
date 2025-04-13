import streamlit as st
import pandas as pd
import plotly.express as px
from db import load_payments
from auth import get_current_user, get_all_users
from utils.sidebar import render_sidebar
from datetime import datetime

# User must be logged in
user = get_current_user()
if not user:
    st.warning("Login required.")
    st.stop()

render_sidebar()
st.title("🏗️ Site / Region Charts")

# Get current user's role
users = get_all_users()
user_data = next((u for u in users if u["email"] == user), None)
role = user_data["role"] if user_data else "unknown"

# Restrict access to HQ roles only
if role not in ["hq_admin", "hq_project_director", "super_admin"]:
    st.warning("Access denied. Only HQ roles can view this page.")
    st.stop()

# Load payment data
payments = load_payments()
df = pd.DataFrame(payments)

if df.empty:
    st.info("No payment records found.")
    st.stop()

# Convert date field
df["submitted_at"] = pd.to_datetime(df["submitted_at"])
df["month"] = df["submitted_at"].dt.strftime("%Y-%m")

# Use email prefix as 'site' name
df["site"] = df["submitted_by"].str.split("@").str[0]

# Chart 1: Total amount per site
st.subheader("💰 Total Payment Requests by Site")
site_totals = df.groupby("site")["amount"].sum().reset_index()
fig1 = px.bar(site_totals, x="site", y="amount", title="Total Requested by Site", labels={"amount": "Amount ($)"})
st.plotly_chart(fig1, use_container_width=True)

# Chart 2: Monthly payment trends per site
st.subheader("📅 Monthly Trend by Site")
monthly = df.groupby(["month", "site"])["amount"].sum().reset_index()
fig2 = px.line(monthly, x="month", y="amount", color="site", markers=True, title="Monthly Trends")
st.plotly_chart(fig2, use_container_width=True)

# Raw data table
st.subheader("📋 Raw Payment Data by Site")
st.dataframe(df[["site", "contractor", "amount", "status", "submitted_at"]])
