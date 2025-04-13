import streamlit as st
import json
import pandas as pd
import plotly.express as px
from utils.sidebar import load_sidebar

# Load sidebar
load_sidebar()

st.title("📊 Contractor Payment Dashboard")

# Load payment data
def load_data():
    try:
        with open("payments.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

payments = load_data()
df = pd.DataFrame(payments)

# Check if there's any data
if df.empty:
    st.info("No payment records found.")
    st.stop()

# Convert status to lowercase for consistency
df["status"] = df["status"].str.lower()

# Filter section
with st.sidebar:
    st.header("🔍 Filters")
    contractors = sorted(df["contractor"].unique())
    selected_contractor = st.selectbox("Select Contractor", ["All"] + contractors)

    status_filter = st.multiselect("Filter by Status", options=df["status"].unique(), default=df["status"].unique())

# Apply filters
filtered_df = df.copy()

if selected_contractor != "All":
    filtered_df = filtered_df[filtered_df["contractor"] == selected_contractor]

if status_filter:
    filtered_df = filtered_df[filtered_df["status"].isin(status_filter)]

# Summary stats
st.subheader("📌 Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Total Requests", len(filtered_df))
col2.metric("Approved", (df["status"] == "approved").sum())
col3.metric("Pending", (df["status"] == "pending").sum())

# Chart
st.subheader("📈 Payment Status Distribution")
status_counts = filtered_df["status"].value_counts().reset_index()
status_counts.columns = ["Status", "Count"]

fig = px.pie(status_counts, names="Status", values="Count", title="Status Breakdown", hole=0.4)
st.plotly_chart(fig, use_container_width=True)

# Raw data
st.subheader("📋 Payment Records")
st.dataframe(filtered_df, use_container_width=True)
