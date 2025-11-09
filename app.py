import streamlit as st
import pandas as pd
import os
import plotly.express as px

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

# --- DETECT WINE & FOOD COLUMN ---
wine_col = next((c for c in df.columns if "wine" in c.lower()), None)
food_col = next((c for c in df.columns if "food" in c.lower()), None)

if not wine_col or not food_col:
    st.error("Required columns 'wine' or 'food' not found in the dataset.")
    st.stop()

# --- SIDEBAR HEADER ---
st.sidebar.markdown(
    """
    <div style='
        background-color:#F7EDE2;
        padding:15px;
        border-radius:10px;
        text-align:center;
        margin-bottom:10px;
    '>
        <h1 style='color:#AA8287; margin-bottom:5px;'>🍷 Taste Harmony</h1>
        <p style='font-size:12px; color:#AA8287; margin-top:0;'>
        Explore how wines complement various foods. Find your perfect pairing!
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# --- SIDEBAR MENU ---
menu = st.sidebar.radio(
    "Navigate",
    ["Overview", "Pairing Explorer"],
    label_visibility="collapsed"
)

# --- SIDEBAR FILTER (EXPANDER) ---
with st.sidebar.expander("Filter Wine 🍷", expanded=True):
    wine_list = ["All"] + sorted(df[wine_col].dropna().unique().tolist())
    selected_wine = st.selectbox("Select Wine Type", wine_list)

# --- FILTER DATA ---
if selected_wine != "All":
    df_filtered = df[df[wine_col] == selected_wine]
else:
    df_filtered = df.copy()

# --- SIDEBAR FOOTER (STICKY) ---
st.sidebar.markdown(
    """
    <div style="
        position: fixed;
        bottom: 0;
        width: 15rem;
        text-align: center;
        padding: 12px;
        background-color: #F7EDE2;
        border-radius:10px;
        color: #555;
        font-size: 10px;
    ">
        © 2025 Wine & Food Pairing Analysis - by Lidya
    </div>
    """,
    unsafe_allow_html=True
)

# --- PAGE CONTENT ---
if menu == "Overview" and selected_wine == "All":
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

# --- TOP 3 FOOD PAIRINGS ---
st.subheader("🍾 Top 3 Food Pairings")
top3 = df_filtered[food_col].value_counts().head(3).reset_index()
top3.columns = ["Food", "Count"]

cols = st.columns(len(top3))
for i, row in enumerate(top3.itertuples()):
    with cols[i]:
        st.metric(f"#{i+1} {row.Food}", f"{row.Count} pairings")

# --- HORIZONTAL BAR CHART DOMINAN FOOD PER WINE ---
top_food = df_filtered[food_col].value_counts().reset_index()
top_food.columns = ["Food", "Count"]

fig = px.bar(
    top_food,
    x="Count",
    y="Food",
    orientation="h",
    color="Count",
    text="Count",
    color_continuous_scale="Reds",
)

fig.update_layout(
    yaxis={'categoryorder':'total ascending'},
    xaxis_title="Number of Pairings",
    yaxis_title="Food",
    showlegend=False,
)

st.plotly_chart(fig, use_container_width=True)

# --- STACKED BAR CHART ALL WINE VS FOOD ---
if selected_wine == "All":
    st.subheader("🍷 Wine vs Food Pairing Comparison")
    pivot = df.pivot_table(
        index=food_col,
        columns=wine_col,
        aggfunc='size',
        fill_value=0
    )

    fig2 = px.bar(
        pivot,
        x=pivot.index,
        y=pivot.columns,
        text_auto=True
    )
    fig2.update_layout(
        xaxis_title="Food",
        yaxis_title="Count",
        barmode="stack",
        legend_title="Wine"
    )
    st.plotly_chart(fig2, use_container_width=True)

# --- CAPTION ONLY FOR OVERALL ---
if selected_wine == "All":
    st.markdown(
        "<p style='font-size:10px; color:#AA8287; text-align:center;'>Note: The longer the bar, the more frequently that type of wine is paired with the food.</p>",
        unsafe_allow_html=True
    )
