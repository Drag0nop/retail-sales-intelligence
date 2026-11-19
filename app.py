import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Retail Sales Intelligence", page_icon="📊", layout="wide")

st.title("📊 Retail Sales Intelligence")
st.caption("Interactive sales, profit, customer, product and shipping analysis")

uploaded_file = st.sidebar.file_uploader("Upload sample_sales.csv", type=["csv"])

if uploaded_file is None:
    st.info("Upload your sample_sales.csv file using the sidebar to open the dashboard.")
    st.stop()

try:
    df = pd.read_csv(uploaded_file, encoding="utf-8")
except UnicodeDecodeError:
    uploaded_file.seek(0)
    df = pd.read_csv(uploaded_file, encoding="latin1")

# Standardize column names
df.columns = (
    df.columns.astype(str).str.strip().str.lower()
    .str.replace(" ", "_", regex=False)
)
df = df.rename(columns={"sub-category": "sub_category"})

required = [
    "order_id", "order_date", "ship_date", "ship_mode", "customer_id",
    "segment", "region", "category", "sub_category", "product_name",
    "sales", "quantity", "discount", "profit"
]
missing = [col for col in required if col not in df.columns]
if missing:
    st.error("The uploaded file is missing these required columns: " + ", ".join(missing))
    st.stop()

# Convert columns safely
for col in ["order_date", "ship_date"]:
    df[col] = pd.to_datetime(df[col], errors="coerce")
for col in ["sales", "quantity", "discount", "profit"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(subset=["order_date", "sales", "quantity", "discount", "profit"]).copy()
df["shipping_days"] = (df["ship_date"] - df["order_date"]).dt.days
df["year_month"] = df["order_date"].dt.to_period("M").astype(str)
df["year"] = df["order_date"].dt.year

# Sidebar filters
st.sidebar.header("Dashboard Filters")

def multi_filter(label, column):
    values = sorted(df[column].dropna().astype(str).unique().tolist())
    selected = st.sidebar.multiselect(label, values, default=values)
    return selected

regions = multi_filter("Region", "region")
categories = multi_filter("Category", "category")
segments = multi_filter("Customer Segment", "segment")
ship_modes = multi_filter("Ship Mode", "ship_mode")

filtered = df[
    df["region"].astype(str).isin(regions)
    & df["category"].astype(str).isin(categories)
    & df["segment"].astype(str).isin(segments)
    & df["ship_mode"].astype(str).isin(ship_modes)
].copy()

if filtered.empty:
    st.warning("No records match the selected filters. Change the filters in the sidebar.")
    st.stop()

# KPI cards
total_sales = filtered["sales"].sum()
total_profit = filtered["profit"].sum()
orders = filtered["order_id"].nunique()
customers = filtered["customer_id"].nunique()
avg_discount = filtered["discount"].mean()

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Sales", f"${total_sales:,.2f}")
c2.metric("Total Profit", f"${total_profit:,.2f}")
c3.metric("Orders", f"{orders:,}")
c4.metric("Customers", f"{customers:,}")
c5.metric("Average Discount", f"{avg_discount:.1%}")

st.divider()

# Sales and profit trends
left, right = st.columns(2)
with left:
    monthly = filtered.groupby("year_month", as_index=False)["sales"].sum()
    fig = px.line(monthly, x="year_month", y="sales", markers=True,
                  title="Monthly Sales Trend", labels={"year_month": "Month", "sales": "Sales"})
    st.plotly_chart(fig, use_container_width=True)

with right:
    category_sales = filtered.groupby("category", as_index=False)["sales"].sum().sort_values("sales", ascending=False)
    fig = px.bar(category_sales, x="category", y="sales", title="Sales by Category",
                 labels={"category": "Category", "sales": "Sales"}, text_auto=".2s")
    st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)
with left:
    region_profit = filtered.groupby("region", as_index=False)["profit"].sum().sort_values("profit", ascending=False)
    fig = px.bar(region_profit, x="region", y="profit", title="Profit by Region",
                 labels={"region": "Region", "profit": "Profit"}, text_auto=".2s")
    st.plotly_chart(fig, use_container_width=True)

with right:
    segment_sales = filtered.groupby("segment", as_index=False)["sales"].sum().sort_values("sales", ascending=False)
    fig = px.pie(segment_sales, names="segment", values="sales", title="Sales by Customer Segment")
    st.plotly_chart(fig, use_container_width=True)

# Product performance
left, right = st.columns(2)
with left:
    top_products = (filtered.groupby("product_name", as_index=False)["sales"].sum()
                    .nlargest(10, "sales").sort_values("sales"))
    fig = px.bar(top_products, x="sales", y="product_name", orientation="h",
                 title="Top 10 Products by Sales", labels={"sales": "Sales", "product_name": "Product"})
    st.plotly_chart(fig, use_container_width=True)

with right:
    sub_profit = filtered.groupby("sub_category", as_index=False)["profit"].sum().sort_values("profit")
    fig = px.bar(sub_profit, x="profit", y="sub_category", orientation="h",
                 title="Profit by Sub-Category", labels={"profit": "Profit", "sub_category": "Sub-Category"},
                 color="profit", color_continuous_scale="RdYlGn")
    st.plotly_chart(fig, use_container_width=True)

# Discount, quantity and profit relationships
left, right = st.columns(2)
with left:
    fig = px.scatter(filtered, x="discount", y="profit", color="category",
                     hover_data=["product_name", "sales"], title="Discount vs Profit",
                     labels={"discount": "Discount", "profit": "Profit"})
    st.plotly_chart(fig, use_container_width=True)

with right:
    numeric_corr = filtered[["sales", "quantity", "discount", "profit"]].corr().round(2)
    fig = px.imshow(numeric_corr, text_auto=True, color_continuous_scale="RdBu_r",
                    zmin=-1, zmax=1, title="Correlation Heatmap")
    st.plotly_chart(fig, use_container_width=True)

# Shipping and data quality
st.subheader("Shipping Analysis")
shipping = filtered["shipping_days"].dropna()
if not shipping.empty:
    a, b = st.columns(2)
    a.metric("Average Shipping Time", f"{shipping.mean():.1f} days")
    b.metric("Median Shipping Time", f"{shipping.median():.0f} days")
    ship_counts = filtered["shipping_days"].value_counts().sort_index().reset_index()
    ship_counts.columns = ["shipping_days", "records"]
    fig = px.bar(ship_counts, x="shipping_days", y="records", title="Shipping Duration Distribution",
                 labels={"shipping_days": "Shipping Days", "records": "Records"})
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Shipping duration is unavailable for the selected records.")

st.subheader("Key Business Metrics")
m1, m2, m3 = st.columns(3)
m1.metric("Average Order Sales", f"${filtered.groupby('order_id')['sales'].sum().mean():,.2f}")
m2.metric("Total Loss-Making Rows", f"{(filtered['profit'] < 0).sum():,}")
m3.metric("Distinct Products", f"{filtered['product_name'].nunique():,}")

st.subheader("Filtered Data")
st.dataframe(filtered, use_container_width=True, hide_index=True)

csv = filtered.to_csv(index=False).encode("utf-8")
st.download_button("Download filtered data as CSV", data=csv,
                   file_name="retail_sales_filtered.csv", mime="text/csv")

st.caption("Note: Dashboard results reflect the uploaded dataset and currently selected filters. Correlation does not establish causation.")
