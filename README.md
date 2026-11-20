# Mamaearth Tertiary Sales & Inventory Dashboard

A Streamlit + Plotly executive dashboard using the sanitized, compressed business data extract in `database_source_part*.csv.gz.b64`.

## Dashboard features

- Net tertiary sales and sales-quantity KPIs
- Client-month record counts, secondary value, and returns value
- Month-wise tertiary sales trend
- Zone-wise, state-wise, and client-type sales mix
- Secondary value comparison
- Opening and closing value trends
- Zone/state/client-type/SourceType/SourceName performance table
- Filters for reporting period, month, zone, state, client type, SourceType, and SourceName
- Filtered CSV export

## Run locally

1. Install Python 3.10 or newer.
2. Clone this repository and open a terminal in the project folder.
3. Install dependencies:

   `pip install -r requirements.txt`

4. Start the dashboard:

   `streamlit run dashboard.py`

Streamlit will print a local URL (typically http://localhost:8501) to open in your browser.

## Database

- The `database_source_part*.csv.gz.b64` files are the dashboard's data source and must remain in the same folder as `dashboard.py`. Each file contains a gzip-compressed CSV encoded as Base64; the app decodes and combines all parts automatically at startup.
- The repository copy is a **sanitized aggregate**, grouped by reporting month, zone, state, client type, and SourceName. It represents 13,663 source client-month records across April–October 2026, covering 256 named sources plus an Unknown bucket. SourceType is reconciled from the workbook's source classification, including the 21 D-Mart records that share the Mamaearth Pvt Ltd SourceName.
- Direct contact fields, staff names, phone numbers, and internal identifiers from the uploaded workbook are not included in the repository extract.
- To refresh the dashboard data, regenerate the sanitized aggregate with these columns, split it into manageable parts, then gzip-compress and Base64-encode each part as `database_source_part*.csv.gz.b64`:

  `Mothly, Zone, State, Client Type, SourceName, Records, NetTertiary, SalesQty, SecondaryValue, OpeningValue, ClosingValue, ReturnsValue`

## Data interpretation

- Net tertiary sales are sourced from the workbook's `NetTertiary` field.
- Opening and closing values are retained as reported. Negative balances are present in the source and are not adjusted by the dashboard.
- October 2026 has fewer source records than September and may be a partial reporting month; interpret the latest month-on-month comparison cautiously.
- The uploaded workbook does not provide verified profit, margin, order, customer acquisition, conversion, product, or channel measures in the aggregated extract. These metrics are not fabricated or displayed.

