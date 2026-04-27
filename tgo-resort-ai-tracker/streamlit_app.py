"""
TGO Resort AI Properties Tracker - Streamlit Dashboard
"""

import streamlit as st
import sqlite3
import pandas as pd
from pathlib import Path
from datetime import datetime

st.set_page_config(page_title="TGO Resort Tracker", layout="wide")
st.title("🏡 TGO Resort Properties AI Tracker")
st.markdown("**AI-powered weekly listing tracker** | Built with LangChain + Groq")

DB_FILE = Path("data/listings_history.db")


@st.cache_data
def load_data():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql("SELECT * FROM listings ORDER BY snapshot_date DESC", conn)
    conn.close()
    return df


df = load_data()

if df.empty:
    st.warning("No data yet. Run scraper.py first.")
    st.stop()

# Sidebar
st.sidebar.header("Filters")
dates = sorted(df['snapshot_date'].unique(), reverse=True)
selected_date = st.sidebar.selectbox("View Snapshot", dates)

# Main view
col1, col2, col3 = st.columns(3)
current_df = df[df['snapshot_date'] == selected_date]

col1.metric("Total Listings", len(current_df))
col2.metric("Avg Price", f"${current_df['price'].mean():,.0f}" if not current_df.empty else "N/A")
col3.metric("Snapshots Available", len(dates))

st.subheader(f"Listings on {selected_date}")
st.dataframe(
    current_df[['address', 'price']].sort_values('price', ascending=False),
    use_container_width=True,
    hide_index=True
)

# Change Detection
st.subheader("📈 Weekly Change Detection")
if len(dates) >= 2:
    latest = dates[0]
    previous = dates[1]

    latest_df = df[df['snapshot_date'] == latest]
    prev_df = df[df['snapshot_date'] == previous]

    latest_set = set(latest_df['address'])
    prev_set = set(prev_df['address'])

    new = latest_df[~latest_df['address'].isin(prev_set)]
    removed = prev_df[~prev_df['address'].isin(latest_set)]

    st.write(f"**{latest} vs {previous}**")
    c1, c2, c3 = st.columns(3)
    c1.metric("🆕 New Listings", len(new))
    c2.metric("❌ Removed", len(removed))

    if not new.empty:
        st.write("**New Listings**")
        st.dataframe(new[['address', 'price']], use_container_width=True, hide_index=True)

    if not removed.empty:
        st.write("**Removed Listings**")
        st.dataframe(removed[['address', 'price']], use_container_width=True, hide_index=True)
else:
    st.info("Run the scraper again with updated data to see changes.")

st.caption("Project built as AI ETL learning portfolio | Python + LangChain + Groq + Streamlit")