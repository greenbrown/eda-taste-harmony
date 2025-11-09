import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="🍷 Taste Harmony", layout="wide")

# --- LOAD DATA ---
@st.cache_data
def load_data():
    path = "data/wine_food_pairing.csv"
    if not os.path.exists(path):
        st.error(f"File not found: {path}")
        st.stop()
    return pd.read_csv(path)

df = load_data()

# --- DETECT WINE COLUMN ---
wine_col = None
for c in df.columns:
    if "wine" in c.lower():
        wine_col = c
        break

if not wine_col:
    st.error("Kolom yang mengandung 'wine' tidak ditemukan di dataset.")
    st.stop()

# --- DETECT FOOD COLUMN ---
food_col = None
for c in df.columns:
    if "food" in c.lower():
        food_col = c
        break

if not food_col:
    st.error("Kolom yang mengandung 'food' tidak ditemukan di dataset.")
    st.stop()

# --- SIDEBAR ---
st.sidebar.markdown(
    "<h1 style='color:#AA8287; text-align:left;'>🍷 Taste Harmony</h1>",
    unsafe_allow_html=True
)

st.sidebar.markdown(
    """
    <p style='font-size:13px; color:#AA8287; text-align:justify; margin-top:-10px;'>
    Helps you explore how different wines complement various foods. Whether you're a wine enthusiast or a foodie, discover perfect pairings and enhance your dining experience!
    </p>
    <hr style='border:1px solid #E0E0E0;'>
    """,
    unsafe_allow_html=True,
)

menu = st.sidebar.radio(
    "Navigate",
    ["Overview", "Pairing Explorer"],
    label_visibility="collapsed"
)


# --- FILTER ---
wine_list = ["All"] + sorted(df[wine_col].dropna().unique().tolist())
selected_wine = st.sidebar.selectbox("Select Wine Type 🍷", wine_list)

if selected_wine != "All":
    df_filtered = df[df[wine_col] == selected_wine]
else:
    df_filtered = df.copy()

# Spacer container
spacer = st.sidebar.empty()

# Footer sidebar
st.sidebar.markdown(
    """
    <div style="
        position: fixed;
        bottom: 0;
        width: 15rem;  /* sesuaikan lebar sidebar */
        text-align: center;
        padding: 10px;
        background-color: #f1f1f1;
        color: #555;
        font-size: 14px;
    ">
        © 2025 Wine & Food Pairing Analysis - by Lidya 
    </div>
    """,
    unsafe_allow_html=True
)

# --- PAGE CONTENT ---
if menu == "Overview":
    st.markdown("<h2 style='color:#AA8287;'>🍇 Overview</h2>", unsafe_allow_html=True)
    st.write(
        "Discover how different wines complement various foods. "
        "Explore pairing trends and uncover perfect matches!"
    )

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Pairings", len(df))
    with col2:
        st.metric("Unique Wines", df[wine_col].nunique())

    st.write("---")

    # Top 3 Pairings (overall)
    st.subheader("🍾 Top 3 Food Pairings (All Wines)")
    top3_overall = (
        df[food_col].value_counts().head(3).reset_index()
    )
    top3_overall.columns = ["Food", "Count"]

    cols = st.columns(3)
    for i, row in enumerate(top3_overall.itertuples()):
        with cols[i]:
            st.metric(f"#{i+1} {row.Food}", f"{row.Count} pairings")

elif menu == "Pairing Explorer":
    st.markdown("<h2 style='color:#AA8287;'>🍽️ Pairing Explorer</h2>", unsafe_allow_html=True)

     # Chart
    fig = px.histogram(
        df_filtered,
        x=food_col,
        color=wine_col,
        title=f"Food Pairing Distribution for {selected_wine if selected_wine != 'All' else 'All Wines'}",
        text_auto=True
    )
    fig.update_layout(
        template="plotly_white",
        title_font_color="#AA8287",
        font_color="#333",
        bargap=0.3
    )
    st.plotly_chart(fig, use_container_width=True)

    # --- TOP 3 SUMMARY ---
    st.subheader("🍾 Top 3 Food Pairings")

    # Revisi: pastikan nama kolom sesuai
    top3 = (
        df_filtered[food_col]
        .value_counts()
        .head(3)
        .reset_index()
    )
    top3.columns = ["Food", "Count"] 

    if not top3.empty:
        cols = st.columns(len(top3))
        for i, row in enumerate(top3.itertuples()):
            with cols[i]:
                st.metric(f"#{i+1} {row.Food}", f"{row.Count} pairings")
    else:
        st.info("No data available for this selection.")