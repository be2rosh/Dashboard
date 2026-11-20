from __future__ import annotations

from io import StringIO
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Mamaearth | Business Intelligence", page_icon="🌿", layout="wide")

# -------------------------------------------------------------------
# Mamaearth Executive BI Dashboard
# Demo dataset only: replace DATA with verified business data for use
# in operational or financial decisions.
# -------------------------------------------------------------------
MONTHS = ["Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov"]
CATEGORIES = ["Electronics", "Fashion", "Home", "Beauty"]
REGIONS = ["North", "South", "West", "East"]
CHANNELS = ["Online", "Retail", "Partner"]

DATA = {
    "revenue": [29, 31, 28, 35, 38, 36, 42, 45, 43, 48, 51, 56],
    "previous": [26, 28, 27, 31, 33, 34, 37, 39, 40, 42, 44, 47],
    "target": [30, 30, 31, 33, 35, 37, 39, 41, 43, 45, 47, 50],
    "customers": [310, 340, 325, 380, 405, 420, 450, 470, 490, 525, 550, 590],
    "regions": {"North": 32, "South": 25, "West": 42, "East": 18},
    "categories": {"Electronics": 40, "Fashion": 25, "Home": 20, "Beauty": 15},
    "category_margin": {"Electronics": .28, "Fashion": .284, "Home": .29, "Beauty": .307},
    "products": {
        "Smartphone X": 14.2, "Wireless Audio": 11.8, "Running Shoes": 9.7,
        "Smart Watch": 8.9, "Home Decor Set": 7.8, "Skincare Kit": 7.1,
        "Laptop Pro": 6.8, "Travel Backpack": 6.1, "Coffee Maker": 5.6,
        "Fitness Band": 4.9,
    },
    "channels": {"Online": 56, "Retail": 31, "Partner": 13},
    "statuses": {"Delivered": 76, "Processing": 14, "Returned": 6, "Cancelled": 4},
    "segments": {"New": 34, "Returning": 48, "VIP": 18},
}

PALETTE = ["#4776e6", "#20b8a6", "#e6a23c", "#8b72d8", "#e4778b", "#65a7d8"]
st.markdown("""
<style>
.block-container {padding-top: 1.5rem; padding-bottom: 2.5rem;}
[data-testid="stMetric"] {background:#ffffff; border:1px solid #e8edf3; padding:14px 16px; border-radius:12px;}
[data-testid="stMetricLabel"] {color:#778397;}
h1, h2, h3 {letter-spacing:-.3px;}
div[data-testid="stCaptionContainer"] {color:#778397;}
</style>
""", unsafe_allow_html=True)

st.title("🌿 Mamaearth")
st.caption("BUSINESS INTELLIGENCE  |  Executive performance overview")
st.info("Demo data notice: all figures are synthetic illustrations, not verified Mamaearth business results.")

with st.sidebar:
    st.header("Dashboard filters")
    period_label = st.selectbox("Date range", ["Last 12 months", "Last 6 months", "Last 3 months"])
    period = {"Last 12 months": 12, "Last 6 months": 6, "Last 3 months": 3}[period_label]
    region_filter = st.selectbox("Region", ["All"] + REGIONS)
    category_filter = st.selectbox("Category", ["All"] + CATEGORIES)
    channel_filter = st.selectbox("Channel", ["All"] + CHANNELS)
    comparison = st.selectbox("Comparison", ["Previous period", "Target"])
    st.divider()
    st.caption("FY 2025–26 · Illustrative demo workspace")

# Keep filter adjustments consistent throughout all views.
region_factor = 1.0 if region_filter == "All" else DATA["regions"][region_filter] / sum(DATA["regions"].values()) * 4
category_factor = 1.0 if category_filter == "All" else DATA["categories"][category_filter] / 25
channel_factor = 1.0 if channel_filter == "All" else DATA["channels"][channel_filter] / 40
scale = region_factor * category_factor * channel_factor

months = MONTHS[-period:]
revenue = pd.Series(DATA["revenue"][-period:], index=months, dtype=float) * scale
previous = pd.Series(DATA["previous"][-period:], index=months, dtype=float) * scale
target = pd.Series(DATA["target"][-period:], index=months, dtype=float) * scale
customer_counts = pd.Series(DATA["customers"][-period:], index=months, dtype=float) * scale
total_revenue = float(revenue.sum())
previous_revenue = float(previous.sum())
target_revenue = float(target.sum())
orders = max(1, round(total_revenue * 17.4))
customers = max(1, round(orders * .62))
profit = total_revenue * .265
aov = total_revenue * 100000 / orders
growth = (total_revenue / previous_revenue - 1) * 100 if previous_revenue else 0
target_attainment = total_revenue / target_revenue * 100 if target_revenue else 0
mom_growth = (revenue.iloc[-1] / revenue.iloc[-2] - 1) * 100 if len(revenue) > 1 and revenue.iloc[-2] else 0
comparison_value = previous_revenue if comparison == "Previous period" else target_revenue
comparison_growth = (total_revenue / comparison_value - 1) * 100 if comparison_value else 0
new_customers = round(customers * DATA["segments"]["New"] / 100)
returning_customers = round(customers * DATA["segments"]["Returning"] / 100)

st.subheader("Executive KPI scorecard")
st.caption(f"{period_label} · {region_filter} region · {category_filter} category · {channel_filter} channel")
kpis = [
    ("Total revenue", f"₹{total_revenue:,.1f}L", f"{comparison_growth:+.1f}% vs {comparison.lower()}"),
    ("Total sales", f"₹{total_revenue:,.1f}L", "Revenue value"),
    ("Total orders", f"{orders:,}", "Estimated demo orders"),
    ("Total customers", f"{customers:,}", "Estimated demo customers"),
    ("New customers", f"{new_customers:,}", "Illustrative segment split"),
    ("Returning customers", f"{returning_customers:,}", "Illustrative segment split"),
    ("Average order value", f"₹{aov:,.0f}", "Revenue ÷ orders"),
    ("Profit", f"₹{profit:,.1f}L", "Estimated at 26.5% margin"),
    ("Profit margin", "26.5%", "Illustrative assumption"),
    ("Growth rate", f"{growth:+.1f}%", "Against previous period"),
    ("Conversion rate", "3.8%", "Illustrative assumption"),
    ("Customer retention", "68.4%", "Illustrative assumption"),
    ("Target achievement", f"{target_attainment:.1f}%", "Revenue ÷ target"),
    ("YoY growth", "14.8%", "Illustrative assumption"),
    ("MoM growth", f"{mom_growth:+.1f}%", "Latest month vs prior month"),
]
for row in range(3):
    cols = st.columns(5)
    for col, (label, value, help_text) in zip(cols, kpis[row * 5:row * 5 + 5]):
        col.metric(label, value, help_text)

st.divider()
st.subheader("Revenue & growth performance")
left, right = st.columns([1.6, 1])
with left:
    trend = pd.DataFrame({"Revenue": revenue, "Previous period": previous}).reset_index(names="Month")
    fig = px.line(trend, x="Month", y=["Revenue", "Previous period"], markers=True,
                  color_discrete_sequence=[PALETTE[0], PALETTE[1]])
    fig.update_layout(height=330, margin=dict(l=10, r=10, t=20, b=10), legend_title_text="")
    fig.update_yaxes(title="Revenue (₹ lakh)", rangemode="tozero")
    st.plotly_chart(fig, use_container_width=True)
with right:
    category_data = DATA["categories"] if category_filter == "All" else {category_filter: DATA["categories"][category_filter]}
    cat_df = pd.DataFrame({"Category": list(category_data), "Share": list(category_data.values())})
    fig = px.pie(cat_df, names="Category", values="Share", hole=.62, color_discrete_sequence=PALETTE)
    fig.update_layout(height=330, margin=dict(l=5, r=5, t=20, b=10), legend_title_text="")
    st.plotly_chart(fig, use_container_width=True)

c1, c2, c3 = st.columns(3)
with c1:
    region_values = DATA["regions"] if region_filter == "All" else {region_filter: DATA["regions"][region_filter]}
    rdf = pd.DataFrame({"Region": list(region_values), "Revenue": [v * scale for v in region_values.values()]})
    fig = px.bar(rdf, x="Region", y="Revenue", color="Region", color_discrete_sequence=PALETTE)
    fig.update_layout(height=280, showlegend=False, margin=dict(l=5, r=5, t=15, b=5))
    st.plotly_chart(fig, use_container_width=True)
with c2:
    cats = [category_filter] if category_filter != "All" else CATEGORIES
    pdf = pd.DataFrame({"Category": cats, "Gross profit": [total_revenue * DATA["categories"][c] / 100 * DATA["category_margin"][c] for c in cats]})
    fig = px.bar(pdf, x="Category", y="Gross profit", color="Category", color_discrete_sequence=PALETTE)
    fig.update_layout(height=280, showlegend=False, margin=dict(l=5, r=5, t=15, b=5))
    st.plotly_chart(fig, use_container_width=True)
with c3:
    sdf = pd.DataFrame({"Status": list(DATA["statuses"]), "Share": list(DATA["statuses"].values())})
    fig = px.pie(sdf, names="Status", values="Share", hole=.58, color_discrete_sequence=PALETTE)
    fig.update_layout(height=280, margin=dict(l=5, r=5, t=15, b=5), legend_title_text="")
    st.plotly_chart(fig, use_container_width=True)

st.divider()
st.subheader("Customer intelligence")
c1, c2 = st.columns([1.5, 1])
with c1:
    cdf = customer_counts.rename("New customers").rename_axis("Month").reset_index()
    fig = px.bar(cdf, x="Month", y="New customers", color_discrete_sequence=[PALETTE[3]])
    fig.update_layout(height=300, margin=dict(l=5, r=5, t=15, b=5))
    st.plotly_chart(fig, use_container_width=True)
with c2:
    segdf = pd.DataFrame({"Segment": list(DATA["segments"]), "Customers": list(DATA["segments"].values())})
    fig = px.pie(segdf, names="Segment", values="Customers", hole=.6, color_discrete_sequence=PALETTE)
    fig.update_layout(height=300, margin=dict(l=5, r=5, t=15, b=5), legend_title_text="")
    st.plotly_chart(fig, use_container_width=True)

st.divider()
st.subheader("Product & channel performance")
c1, c2 = st.columns([1.4, 1])
with c1:
    products = pd.DataFrame({"Product": list(DATA["products"]), "Revenue": list(DATA["products"].values())})
    if category_filter != "All":
        product_category = {"Smartphone X":"Electronics", "Wireless Audio":"Electronics", "Smart Watch":"Electronics",
                            "Laptop Pro":"Electronics", "Running Shoes":"Fashion", "Travel Backpack":"Fashion",
                            "Home Decor Set":"Home", "Coffee Maker":"Home", "Skincare Kit":"Beauty", "Fitness Band":"Beauty"}
        products = products[products["Product"].map(product_category) == category_filter]
    products = products.sort_values("Revenue", ascending=True)
    fig = px.bar(products, x="Revenue", y="Product", orientation="h", color_discrete_sequence=[PALETTE[0]])
    fig.update_layout(height=390, margin=dict(l=5, r=5, t=15, b=5), yaxis_title="")
    st.plotly_chart(fig, use_container_width=True)
with c2:
    chdf = pd.DataFrame({"Channel": list(DATA["channels"]), "Share": list(DATA["channels"].values())})
    if channel_filter != "All":
        chdf = chdf[chdf["Channel"] == channel_filter]
    fig = px.bar(chdf, x="Channel", y="Share", color="Channel", color_discrete_sequence=PALETTE)
    fig.update_layout(height=390, margin=dict(l=5, r=5, t=15, b=5), showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

st.divider()
st.subheader("Target achievement & operating performance")
c1, c2 = st.columns([1.5, 1])
with c1:
    target_df = pd.DataFrame({"Month": months, "Actual": revenue.values, "Target": target.values})
    fig = go.Figure()
    fig.add_trace(go.Bar(x=target_df["Month"], y=target_df["Target"], name="Target", marker_color="#dce4ef"))
    fig.add_trace(go.Scatter(x=target_df["Month"], y=target_df["Actual"], name="Actual", mode="lines+markers", line=dict(color=PALETTE[0], width=3)))
    fig.update_layout(height=320, margin=dict(l=5, r=5, t=15, b=5), barmode="overlay", legend_title_text="", yaxis_title="₹ lakh")
    st.plotly_chart(fig, use_container_width=True)
with c2:
    funnel = pd.DataFrame({"Stage": ["Website visits", "Product views", "Add to cart", "Checkout started", "Orders completed"],
                           "Count": [84200, 32600, 12480, 7820, 4260]})
    fig = px.funnel(funnel, x="Count", y="Stage", color_discrete_sequence=[PALETTE[0]])
    fig.update_layout(height=320, margin=dict(l=5, r=5, t=15, b=5))
    st.plotly_chart(fig, use_container_width=True)

st.divider()
st.subheader("Detailed performance table")
selected_categories = [category_filter] if category_filter != "All" else CATEGORIES
detail_rows = []
for cat in selected_categories:
    cat_revenue = total_revenue * DATA["categories"][cat] / 100
    cat_orders = max(1, round(orders * DATA["categories"][cat] / 100))
    margin = DATA["category_margin"][cat]
    cat_profit = cat_revenue * margin
    detail_rows.append({"Product category": cat, "Revenue (₹ lakh)": round(cat_revenue, 2),
                        "Orders": cat_orders, "Average order value (₹)": round(cat_revenue * 100000 / cat_orders),
                        "Profit (₹ lakh)": round(cat_profit, 2), "Profit margin": f"{margin:.1%}",
                        "Performance": "Above plan" if margin >= .28 else "Monitor"})
detail_df = pd.DataFrame(detail_rows)
st.dataframe(detail_df, use_container_width=True, hide_index=True)

st.download_button("⬇ Download filtered data (CSV)", detail_df.to_csv(index=False).encode("utf-8"),
                   file_name="mamaearth_dashboard_export.csv", mime="text/csv")

st.divider()
st.subheader("Business insights & recommended actions")
i1, i2, i3 = st.columns(3)
i1.info(f"**Growth opportunity**\n\nRevenue is {growth:+.1f}% against the previous period. Review the strongest acquisition and channel drivers.")
i2.info(f"**Category mix**\n\n{max(DATA['categories'], key=DATA['categories'].get)} is the largest category in the illustrative dataset. Monitor concentration and margin.")
i3.info(f"**Customer strategy**\n\nReturning customers represent {DATA['segments']['Returning']}% of the sample. Test loyalty and replenishment campaigns.")

st.caption("All monetary values are illustrative INR lakh unless stated otherwise. Replace the sample data and assumptions with verified source data before making business decisions.")
