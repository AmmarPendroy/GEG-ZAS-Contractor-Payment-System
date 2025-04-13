import streamlit as st
import pandas as pd
import plotly.express as px
from db import load_payments
from auth import get_current_user
from utils.sidebar import render_sidebar

st.set_page_config(page_title="Site Charts", page_icon="🌍")

user = get_current_user()
if not user:
    st.warning("🔒 Login required.")
    st.stop()

render_sidebar()
st.title("🌍 Site-Based Payment Overview")
st.caption("View and compare site payments by contractor or month")

df = pd.DataFrame(load_payments())
if df.empty:
    st.info("No payment data available.")
    st.stop()

# Derive site/project from email (e.g., zas_project_manager → ZAS Site)
df["site"] = df["submitted_by"].apply(lambda x: x.split("@")[0].split(".")[0].upper())
df["month"] = pd.to_datetime(df["submitted_at"]).dt.strftime("%B %Y")

# Chart 1: Total per site
st.subheader("🏗️ Total Payment Requests by Site")
site_chart = df.groupby("site")["amount"].sum().reset_index()
fig1 = px.bar(site_chart, x="site", y="amount", title="Payments by Site", text_auto=".2s")
st.plotly_chart(fig1, use_container_width=True)

# Chart 2: Site activity by month
st.subheader("📆 Site Submission Activity by Month")
monthly_chart = df.groupby(["site", "month"])["amount"].sum().reset_index()
fig2 = px.line(monthly_chart, x="month", y="amount", color="site", markers=True, title="Monthly Activity")
st.plotly_chart(fig2, use_container_width=True)
