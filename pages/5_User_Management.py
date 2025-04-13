import streamlit as st
import pandas as pd
import csv
from utils.sidebar import render_sidebar
from utils.taskbar import render_taskbar

render_sidebar()
render_taskbar()
st.title("🛠 User Management")

USER_CSV = "user_db.csv"

try:
    with open(USER_CSV, "r") as f:
        reader = csv.DictReader(f)
        users = list(reader)
    df = pd.DataFrame(users)
    st.dataframe(df)
except FileNotFoundError:
    st.warning("No user database found.")
