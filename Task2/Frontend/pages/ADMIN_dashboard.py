import streamlit as st
import requests
import pandas as pd
import math

API_BASE = st.secrets.get("API_BASE", "http://127.0.0.1:5000")

# Protect admin page
if "admin_logged_in" not in st.session_state or not st.session_state.admin_logged_in:
    st.switch_page("pages/_Admin_Login.py")

st.set_page_config(page_title="Admin Dashboard", layout="wide")

st.title("🔴 Admin Dashboard")

# Logout (top right)
col1, col2 = st.columns([6, 1])
with col2:
    if st.button("Logout"):
        st.session_state.admin_logged_in = False
        st.switch_page("pages/_Admin_Login.py")


# Fetch data
try:
    res = requests.get(f"{API_BASE}/api/feedback", timeout=20)
    data = res.json()
except:
    st.error("Backend unreachable")
    st.stop()

if not data:
    st.info("No feedback found.")
    st.stop()

df = pd.DataFrame(data)

if "created_at" in df.columns:
    df["created_at"] = pd.to_datetime(df["created_at"])


# METRICS
st.subheader("Overview")

total = len(df)
avg = df["rating"].mean()
pos = (df["rating"] >= 4).sum()
neg = (df["rating"] <= 2).sum()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total", total)
c2.metric("Avg Rating", f"{avg:.2f}")
c3.metric("Positive", pos)
c4.metric("Negative", neg)


# CHART
st.subheader("Rating Distribution")
st.bar_chart(df["rating"].value_counts().sort_index())


# SORTING
st.subheader("All Submissions")
sort_mode = st.radio("Sort by", ["Latest first", "Urgency"], horizontal=True)

df_sorted = df.copy()

if sort_mode == "Latest first" and "created_at" in df:
    df_sorted = df_sorted.sort_values("created_at", ascending=False)
elif sort_mode == "Urgency":
    df_sorted = df_sorted.sort_values(
        by=["rating", "created_at"] if "created_at" in df else ["rating"],
        ascending=[True, False] if "created_at" in df else [True]
    )


# PAGINATION
rows_per_page = st.selectbox("Rows per page", [2, 5, 10, 20], index=1)
pages = math.ceil(len(df_sorted) / rows_per_page)

page = st.radio("Pages", list(range(1, pages + 1)), horizontal=True)

start = (page - 1) * rows_per_page
end = start + rows_per_page

display_cols = ["created_at", "rating", "review", "ai_summary", "ai_actions"]
display_cols = [c for c in display_cols if c in df_sorted.columns]

st.caption(f"Showing {start+1}–{min(end,len(df_sorted))} of {len(df_sorted)}")

st.dataframe(
    df_sorted.iloc[start:end][display_cols],
    use_container_width=True
)
