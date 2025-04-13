import streamlit as st
import pandas as pd
import plotly.express as px
from db import load_payments
from utils.sidebar import render_sidebar
from utils.taskbar import render_taskbar

render_sidebar()
render_taskbar()
st.title("📍 Site-Based Charts")

payments = load_payments()
df = pd.DataFrame(payments)

if df.empty:
    st.info("No data available.")
    st.stop()

df["submitted_at"] = pd.to_datetime(df["submitted_at"])
df["month"] = df["submitted_at"].dt.to_period("M").astype(str)

st.subheader("📊 Monthly Total by Contractor")
monthly = df.groupby(["contractor", "month"])["amount"].sum().reset_index()
fig1 = px.bar(monthly, x="month", y="amount", color="contractor", barmode="group", title="Monthly Payment Volume")
st.plotly_chart(fig1, use_container_width=True)

st.subheader("📊 Total per Contractor")
total = df.groupby("contractor")["amount"].sum().reset_index()
fig2 = px.pie(total, names="contractor", values="amount", hole=0.4, title="Total by Contractor")
st.plotly_chart(fig2, use_container_width=True)
