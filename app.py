
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# -----------------------------
# PAGE CONFIGURATION
# -----------------------------
st.set_page_config(
    page_title="Retail Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Retail Sales Dashboard")
st.write("Analyze sales performance, customers, and product categories.")


# -----------------------------
# LOAD DATA
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "retail_sales_cleaned.csv"

if not DATA_FILE.exists():
    DATA_FILE = BASE_DIR / "retail.csv"


@st.cache_data
def load_data(path):

    try:
        df = pd.read_csv(path, encoding="utf-8-sig")
    except UnicodeDecodeError:
        df = pd.read_csv(path, encoding="cp1252")

    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(r"[\s-]+", "_", regex=True)
    )

    df["order_date"] = pd.to_datetime(
        df["order_date"],
        errors="coerce",
        dayfirst=True
    )

    df["sales"] = pd.to_numeric(
        df["sales"], errors="coerce"
    )

    df["quantity"] = pd.to_numeric(
        df["quantity"], errors="coerce"
    )

    df = df.dropna(
        subset=["order_date", "sales", "quantity"]
    )

    return df


if not DATA_FILE.exists():
    st.error("Dataset not found. Please place the CSV file beside app.py.")
    st.stop()

df = load_data(str(DATA_FILE))

if df.empty:
    st.error("No valid records found in the dataset.")
    st.stop()


# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("Filters")

regions = st.sidebar.multiselect(
    "Select Region",
    sorted(df["region"].dropna().unique()),
    default=sorted(df["region"].dropna().unique())
)

categories = st.sidebar.multiselect(
    "Select Category",
    sorted(df["category"].dropna().unique()),
    default=sorted(df["category"].dropna().unique())
)

segments = st.sidebar.multiselect(
    "Select Customer Segment",
    sorted(df["segment"].dropna().unique()),
    default=sorted(df["segment"].dropna().unique())
)

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(
        df["order_date"].min().date(),
        df["order_date"].max().date()
    )
)


# -----------------------------
# FILTER DATA
# -----------------------------
filtered_df = df.copy()

if len(date_range) == 2:

    start_date, end_date = date_range

    filtered_df = filtered_df[
        filtered_df["order_date"].dt.date.between(
            start_date, end_date
        )
    ]

filtered_df = filtered_df[
    filtered_df["region"].isin(regions)
    & filtered_df["category"].isin(categories)
    & filtered_df["segment"].isin(segments)
]

if filtered_df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()


# -----------------------------
# KPI METRICS
# -----------------------------
total_sales = filtered_df["sales"].sum()

total_orders = filtered_df["order_id"].nunique()

total_customers = filtered_df["customer_id"].nunique()

average_order_value = (
    filtered_df.groupby("order_id")["sales"].sum().mean()
)

st.subheader("Business Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Sales",
    f"₹{total_sales:,.2f}"
)

col2.metric(
    "Total Orders",
    f"{total_orders:,}"
)

col3.metric(
    "Total Customers",
    f"{total_customers:,}"
)

col4.metric(
    "Average Order Value",
    f"₹{average_order_value:,.2f}"
)


st.divider()


# -----------------------------
# SALES TREND
# -----------------------------
st.subheader("Sales Over Time")

monthly_sales = (
    filtered_df
    .assign(month=filtered_df["order_date"].dt.to_period("M").astype(str))
    .groupby("month", as_index=False)["sales"]
    .sum()
)

fig = px.line(
    monthly_sales,
    x="month",
    y="sales",
    markers=True,
    title="Monthly Sales Trend"
)

fig.update_layout(
    xaxis_title="Month",
    yaxis_title="Sales (₹)",
    template="plotly_white"
)

fig.update_yaxes(tickprefix="₹", tickformat="~s")

st.plotly_chart(fig, width="stretch")


# -----------------------------
# CATEGORY AND REGION ANALYSIS
# -----------------------------
st.subheader("Sales Analysis")

col1, col2 = st.columns(2)

with col1:

    category_sales = (
        filtered_df.groupby("category", as_index=False)["sales"]
        .sum()
        .sort_values("sales", ascending=False)
    )

    fig = px.bar(
        category_sales,
        x="category",
        y="sales",
        title="Sales by Category",
        color="category"
    )

    fig.update_layout(
        template="plotly_white",
        yaxis_title="Sales (₹)"
    )

    fig.update_yaxes(tickprefix="₹", tickformat="~s")

    st.plotly_chart(fig, width="stretch")


with col2:

    region_sales = (
        filtered_df.groupby("region", as_index=False)["sales"]
        .sum()
        .sort_values("sales", ascending=False)
    )

    fig = px.pie(
        region_sales,
        names="region",
        values="sales",
        hole=0.4,
        title="Sales by Region"
    )

    fig.update_traces(
        hovertemplate="%{label}<br>₹%{value:,.2f}<extra></extra>"
    )

    fig.update_layout(template="plotly_white")

    st.plotly_chart(fig, width="stretch")


# -----------------------------
# CUSTOMER SEGMENT ANALYSIS
# -----------------------------
st.subheader("Customer Analysis")

col1, col2 = st.columns(2)

with col1:

    segment_sales = (
        filtered_df.groupby("segment", as_index=False)["sales"]
        .sum()
    )

    fig = px.bar(
        segment_sales,
        x="segment",
        y="sales",
        title="Sales by Customer Segment",
        color="segment"
    )

    fig.update_layout(
        template="plotly_white",
        yaxis_title="Sales (₹)"
    )

    fig.update_yaxes(tickprefix="₹", tickformat="~s")

    st.plotly_chart(fig, width="stretch")


with col2:

    top_customers = (
        filtered_df.groupby("customer_name", as_index=False)["sales"]
        .sum()
        .nlargest(10, "sales")
        .sort_values("sales")
    )

    fig = px.bar(
        top_customers,
        x="sales",
        y="customer_name",
        orientation="h",
        title="Top 10 Customers"
    )

    fig.update_layout(
        template="plotly_white",
        xaxis_title="Sales (₹)"
    )

    fig.update_xaxes(tickprefix="₹", tickformat="~s")

    st.plotly_chart(fig, width="stretch")


# -----------------------------
# DATA TABLE
# -----------------------------
st.divider()

st.subheader("Dataset")

st.write(f"Total Records: {len(filtered_df):,}")

st.dataframe(
    filtered_df,
    width="stretch",
    hide_index=True
)


# -----------------------------
# DOWNLOAD DATA
# -----------------------------
csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered Dataset",
    data=csv,
    file_name="retail_sales_filtered.csv",
    mime="text/csv"
)


# -----------------------------
# FOOTER
# -----------------------------
st.caption(
    f"Retail Sales Dashboard | Dataset: {DATA_FILE.name}"
)
