import streamlit as st
import pandas as pd
import csv
from utils.sidebar import render_sidebar

render_sidebar()
st.title("🛠 User Management")

st.info("This page is read-only for now since login-based admin control is disabled.")

# Load user data from CSV
USER_CSV = "user_db.csv"

try:
    with open(USER_CSV, "r") as f:
        reader = csv.DictReader(f)
        users = list(reader)
    df = pd.DataFrame(users)
    st.dataframe(df)
except FileNotFoundError:
    st.warning("No user database found.")
