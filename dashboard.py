from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Mamaearth | Tertiary Sales & Inventory",
    page_icon="🌿",
    layout="wide",
)

DATA_FILE = Path(__file__).with_name("database.csv")
REQUIRED_COLUMNS = [
    "Mothly", "Zone", "Client Type", "Records", "NetTertiary",
    "SalesQty", "SecondaryValue", "OpeningValue", "ClosingValue",
    "ReturnsValue",
]
PALETTE = ["#477B61", "#8EAE91", "#C6A96B", "#789B8A", "#B97970", "#91AFA8"]

st.markdown(
    """
    <style>
      :root {
        --page-bg: #f1f6f1; --panel: #ffffff; --ink: #18352b;
        --muted: #62776c; --line: #dce9df; --navy: #244b3b;
        --blue: #477b61; --teal: #8eae91; --green: #397653;
        --shadow: 0 8px 28px rgba(36,75,59,.07);
      }
      .stApp {background: radial-gradient(ellipse at 8% 0%, rgba(151,190,151,.16), transparent 38%), var(--page-bg); color: var(--ink);}
      .block-container {max-width: 1700px; padding: 1.6rem 2rem 2.5rem;}
      h1, h2, h3 {color: var(--ink); letter-spacing: -.45px;}
      h1 {font-size: 1.75rem !important; font-weight: 760 !important;}
      h2 {font-size: 1.05rem !important; font-weight: 720 !important;}
      h3 {font-size: .9rem !important; font-weight: 700 !important;}
      div[data-testid="stCaptionContainer"], .stMarkdown small {color: var(--muted);}
      [data-testid="stMetric"] {
        background: var(--panel); border: 1px solid var(--line);
        border-radius: 13px; padding: 15px 16px; min-height: 112px; border-top: 3px solid #a9c9ad;
        box-shadow: var(--shadow); gap: 7px;
      }
      [data-testid="stMetricLabel"] {color: var(--muted); font-size: .72rem; font-weight: 650;}
      [data-testid="stMetricValue"] {color: var(--ink); font-size: 1.55rem; font-weight: 760;}
      [data-testid="stMetricDelta"] {font-size: .68rem; font-weight: 700;}
      div[data-testid="stVerticalBlockBorderWrapper"] {
        border-color: var(--line); border-radius: 13px; box-shadow: var(--shadow);
        background: var(--panel);
      }
      div[data-testid="stSelectbox"] label {
        color: #526c5d; font-size: .68rem; font-weight: 750;
        letter-spacing: .045em; text-transform: uppercase;
      }
      div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        border-radius: 9px; border-color: var(--line); background: #fff; min-height: 39px;
      }
      div[data-testid="stButton"] button, div[data-testid="stDownloadButton"] button {
        border-radius: 9px; border: 1px solid var(--line); font-weight: 650;
      }
      div[data-testid="stDownloadButton"] button {
        background: #315f49; color: #fff; border-color: #315f49;
      }
      [data-testid="stPlotlyChart"] {background: transparent;}
      hr {border-color: var(--line);}
      @media(max-width: 760px) {
        .block-container {padding: 1rem .8rem 2rem;}
        [data-testid="stMetricValue"] {font-size: 1.15rem;}
      }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_data() -> pd.DataFrame:
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            "database.csv is missing. Keep database.csv in the same folder as dashboard.py."
        )
    frame = pd.read_csv(DATA_FILE, parse_dates=["Mothly"])
    missing = [column for column in REQUIRED_COLUMNS if column not in frame.columns]
    if missing:
        raise ValueError(f"database.csv is missing required columns: {', '.join(missing)}")
    frame = frame.rename(columns={"Mothly": "Month", "Client Type": "ClientType"})
    numeric = [
        "Records", "NetTertiary", "SalesQty", "SecondaryValue",
        "OpeningValue", "ClosingValue", "ReturnsValue",
    ]
    for column in numeric:
        frame[column] = pd.to_numeric(frame[column], errors="coerce").fillna(0)
    frame["MonthLabel"] = frame["Month"].dt.strftime("%b %Y")
    return frame


def crore(value: float) -> str:
    return f"₹{value / 10_000_000:,.2f} Cr"


try:
    data = load_data()
except Exception as exc:
    st.error(f"Unable to load the dashboard database: {exc}")
    st.stop()

months_available = sorted(data["Month"].dropna().unique())
month_labels = {pd.Timestamp(month): pd.Timestamp(month).strftime("%b %Y") for month in months_available}

top_title, top_actions = st.columns([3, 1])
with top_title:
    st.markdown(
        '<div style="font-size:10px;letter-spacing:1.5px;color:#4776e6;font-weight:800;">BUSINESS PERFORMANCE / OVERVIEW</div>',
        unsafe_allow_html=True,
    )
    st.title("🌿 Mamaearth")
    st.caption("TERTIARY SALES & INVENTORY INTELLIGENCE  |  Executive dashboard")
with top_actions:
    st.write("")
    st.download_button(
        "↓ Export data",
        data=data.to_csv(index=False).encode("utf-8"),
        file_name="mamaearth_dashboard_data.csv",
        mime="text/csv",
        use_container_width=True,
    )

# Compact filter bar, styled to match the supplied executive dashboard reference.
with st.container(border=True):
    st.markdown(
        '<div style="font-size:10px;letter-spacing:1.2px;color:#778397;font-weight:800;margin-bottom:8px;">DASHBOARD FILTERS</div>',
        unsafe_allow_html=True,
    )
    filter_period, filter_zone, filter_client = st.columns([20, 9, 15])
    with filter_period:
        period_label = st.selectbox(
            "1. Reporting period",
            ["All available months", "Last 6 months", "Last 3 months"],
            index=0,
        )
    with filter_zone:
        zone_options = ["All zones"] + sorted(data["Zone"].dropna().unique().tolist())
        selected_zone = st.selectbox("2. Zone", zone_options)
    with filter_client:
        client_options = ["All client types"] + sorted(data["ClientType"].dropna().unique().tolist())
        selected_client = st.selectbox("3. Client type", client_options)

st.caption(
    f"Source: repository database.csv  ·  Coverage: "
    f"{pd.Timestamp(months_available[0]).strftime('%b %Y')} – "
    f"{pd.Timestamp(months_available[-1]).strftime('%b %Y')}"
)

period_count = {
    "All available months": len(months_available),
    "Last 6 months": 6,
    "Last 3 months": 3,
}[period_label]
selected_months = months_available[-period_count:]
filtered = data[data["Month"].isin(selected_months)].copy()
if selected_zone != "All zones":
    filtered = filtered[filtered["Zone"] == selected_zone]
if selected_client != "All client types":
    filtered = filtered[filtered["ClientType"] == selected_client]

if filtered.empty:
    st.warning("No records match the selected filters.")
    st.stop()

filtered = filtered.sort_values("Month")
monthly = (
    filtered.groupby("Month", as_index=False)
    .agg(
        NetTertiary=("NetTertiary", "sum"),
        SalesQty=("SalesQty", "sum"),
        Records=("Records", "sum"),
        SecondaryValue=("SecondaryValue", "sum"),
        OpeningValue=("OpeningValue", "sum"),
        ClosingValue=("ClosingValue", "sum"),
        ReturnsValue=("ReturnsValue", "sum"),
    )
    .sort_values("Month")
)
total_net = float(filtered["NetTertiary"].sum())
total_qty = int(filtered["SalesQty"].sum())
total_records = int(filtered["Records"].sum())
total_secondary = float(filtered["SecondaryValue"].sum())
total_returns = float(filtered["ReturnsValue"].sum())
total_closing = float(filtered["ClosingValue"].sum())

mom = None
if len(monthly) >= 2:
    prior = float(monthly.iloc[-2]["NetTertiary"])
    latest = float(monthly.iloc[-1]["NetTertiary"])
    if prior:
        mom = (latest / prior - 1) * 100

st.markdown("## Executive KPI scorecard")
st.caption(
    f"{period_label}  ·  {selected_zone}  ·  {selected_client}  ·  "
    f"{len(monthly)} month(s) represented"
)

kpi_cols = st.columns(5)
kpi_cols[0].metric(
    "Net tertiary sales",
    crore(total_net),
    f"{mom:+.1f}% vs prior month" if mom is not None else None,
)
kpi_cols[1].metric("Tertiary sales quantity", f"{total_qty:,.0f}")
kpi_cols[2].metric("Client-month records", f"{total_records:,}")
kpi_cols[3].metric("Secondary value", crore(total_secondary))
kpi_cols[4].metric("Returns value", crore(total_returns))

st.caption(
    "Net tertiary sales uses the source field NetTertiary. Values are shown as reported; "
    "this extract does not contain verified profit, margin, order, customer-acquisition, "
    "or conversion metrics."
)

st.divider()
st.markdown("## Sales performance")

left, right = st.columns([1.55, 1])
with left:
    trend = monthly.copy()
    trend["Month"] = trend["Month"].dt.strftime("%b %Y")
    fig = px.line(
        trend,
        x="Month",
        y="NetTertiary",
        markers=True,
        color_discrete_sequence=[PALETTE[0]],
        labels={"NetTertiary": "Net tertiary sales (₹)", "Month": ""},
    )
    fig.update_traces(line=dict(width=3), marker=dict(size=8))
    fig.update_layout(height=350, margin=dict(l=8, r=8, t=18, b=8), yaxis_tickformat=",.0f")
    st.plotly_chart(fig, use_container_width=True)

with right:
    zone_mix = (
        filtered.groupby("Zone", as_index=False)["NetTertiary"]
        .sum()
        .sort_values("NetTertiary", ascending=True)
    )
    fig = px.bar(
        zone_mix,
        x="NetTertiary",
        y="Zone",
        orientation="h",
        color="Zone",
        color_discrete_sequence=PALETTE,
        labels={"NetTertiary": "Net tertiary sales (₹)", "Zone": ""},
    )
    fig.update_layout(height=350, showlegend=False, margin=dict(l=8, r=8, t=18, b=8))
    st.plotly_chart(fig, use_container_width=True)

st.divider()
st.markdown("## Sales mix & operating movement")

c1, c2, c3 = st.columns(3)
with c1:
    client_mix = (
        filtered.groupby("ClientType", as_index=False)["NetTertiary"]
        .sum()
        .sort_values("NetTertiary", ascending=False)
    )
    fig = px.pie(
        client_mix,
        names="ClientType",
        values="NetTertiary",
        hole=0.58,
        color_discrete_sequence=PALETTE,
    )
    fig.update_layout(height=310, margin=dict(l=5, r=5, t=15, b=5), legend_title_text="")
    st.plotly_chart(fig, use_container_width=True)

with c2:
    compare = monthly[["Month", "NetTertiary", "SecondaryValue"]].copy()
    compare["Month"] = compare["Month"].dt.strftime("%b %Y")
    compare = compare.melt(
        id_vars="Month",
        value_vars=["NetTertiary", "SecondaryValue"],
        var_name="Metric",
        value_name="Value",
    )
    compare["Metric"] = compare["Metric"].map(
        {"NetTertiary": "Net tertiary", "SecondaryValue": "Secondary"}
    )
    fig = px.bar(
        compare,
        x="Month",
        y="Value",
        color="Metric",
        barmode="group",
        color_discrete_sequence=PALETTE[:2],
        labels={"Value": "Value (₹)", "Month": ""},
    )
    fig.update_layout(height=310, margin=dict(l=5, r=5, t=15, b=5), legend_title_text="")
    st.plotly_chart(fig, use_container_width=True)

with c3:
    stock = monthly[["Month", "OpeningValue", "ClosingValue"]].copy()
    stock["Month"] = stock["Month"].dt.strftime("%b %Y")
    stock = stock.melt(
        id_vars="Month",
        value_vars=["OpeningValue", "ClosingValue"],
        var_name="Metric",
        value_name="Value",
    )
    stock["Metric"] = stock["Metric"].map(
        {"OpeningValue": "Opening value", "ClosingValue": "Closing value"}
    )
    fig = px.bar(
        stock,
        x="Month",
        y="Value",
        color="Metric",
        barmode="group",
        color_discrete_sequence=PALETTE[2:4],
        labels={"Value": "Reported value (₹)", "Month": ""},
    )
    fig.update_layout(height=310, margin=dict(l=5, r=5, t=15, b=5), legend_title_text="")
    st.plotly_chart(fig, use_container_width=True)

st.divider()
st.markdown("## Zone and client-type performance")
summary = (
    filtered.groupby(["Zone", "ClientType"], as_index=False)
    .agg(
        ClientMonthRecords=("Records", "sum"),
        NetTertiary=("NetTertiary", "sum"),
        SalesQty=("SalesQty", "sum"),
        SecondaryValue=("SecondaryValue", "sum"),
        ReturnsValue=("ReturnsValue", "sum"),
        ClosingValue=("ClosingValue", "sum"),
    )
    .sort_values("NetTertiary", ascending=False)
)
display = summary.rename(
    columns={
        "Zone": "Zone",
        "ClientType": "Client type",
        "ClientMonthRecords": "Client-month records",
        "NetTertiary": "Net tertiary sales (₹)",
        "SalesQty": "Sales quantity",
        "SecondaryValue": "Secondary value (₹)",
        "ReturnsValue": "Returns value (₹)",
        "ClosingValue": "Closing value (₹)",
    }
)
st.dataframe(display, use_container_width=True, hide_index=True)

st.download_button(
    "⬇ Download filtered dashboard data (CSV)",
    data=filtered.to_csv(index=False).encode("utf-8"),
    file_name="mamaearth_filtered_dashboard_data.csv",
    mime="text/csv",
)

with st.expander("Data notes & interpretation"):
    st.markdown(
        """
        - The repository database is an **aggregated, sanitized extract** grouped by month, zone, and client type.
        - It contains 105 aggregate rows representing 13,663 source client-month records across April–October 2026.
        - The latest month has fewer source records than the preceding month and may be a partial reporting month; interpret its month-on-month comparison cautiously.
        - Opening and closing values are shown as supplied. Negative balances are present in the source and have not been silently adjusted.
        - The source extract does not provide product-level, channel-level, customer acquisition, conversion, profit, or margin measures. Those metrics are intentionally not fabricated.
        - Refresh the repository data by replacing database.csv with a newly aggregated extract that retains the same column names.
        """
    )

st.caption("Mamaearth | Executive tertiary sales and inventory dashboard · Data source: database.csv")
