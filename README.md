# Retail Sales Intelligence Dashboard

A locally running college industrial training project for exploring retail sales data. The project uses Python, Streamlit, Pandas, NumPy, Plotly, and pytest. It does not require paid services, API keys, or an external database.

## Run locally

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run app.py
```

The app provides a seven-page local dashboard with CSV upload, an explicitly synthetic demo dataset, shared date/category/region filters, KPIs, interactive Plotly charts, data quality details, and filtered CSV/summary downloads. The uploaded source remains separate from the cleaned working dataset. SQLite is available through Python's standard library and is not needed for the current workflow.

## Project structure and file purposes

| Path | Purpose |
| --- | --- |
| `app.py` | Streamlit entry point and page composition. |
| `requirements.txt` | Python packages needed by the project. |
| `README.md` | Setup instructions, architecture overview, and file guide. |
| `data/` | Local input datasets, including a labeled synthetic demo CSV. |
| `src/__init__.py` | Marks `src` as the reusable data and analytics package. |
| `src/data_loader.py` | CSV loading, required-column validation, and non-destructive data profiling. |
| `src/data_cleaning.py` | Non-destructive cleaning, explicit rejection reasons, and before/after quality summary. |
| `src/analytics.py` | Independent sales metrics and grouped analyses with shared date filters. |
| `src/visualizations.py` | Reusable themed Plotly chart builders for sales, profit, category, region, products, and customers. |
| `src/report_generator.py` | Future export of analysis summaries and reports. |
| `database/__init__.py` | Marks `database` as the local persistence package. |
| `database/db.py` | Future SQLite connection and persistence helpers, if needed. |
| `components/__init__.py` | Marks `components` as reusable Streamlit UI components. |
| `components/sidebar.py` | Navigation, CSV/demo selection, and shared date/category/region filters. |
| `components/kpi_cards.py` | Reusable filtered KPI cards. |
| `components/charts.py` | Shared Plotly chart rendering helper. |
| `assets/style.css` | Dark navy and cyan dashboard styling. |
| `tests/test_cleaning.py` | Unit tests for cleaning behavior and rejection reporting. |
| `tests/test_analytics.py` | Unit tests for sales metrics and grouped analysis. |
| `tests/test_data_loader.py` | Tests for valid/invalid CSV loading, schema validation, and quality profiling. |
| `outputs/reports/` | Local destination for generated reports. |

`data/sample_sales.csv` contains synthetic records for demonstrating upload and inspection behavior only. It is labeled as synthetic in the UI and must not be treated as real business data or used to claim real analytical findings.

### Cleaning module

`src.data_cleaning.clean_dataset(frame)` returns a `CleaningResult` containing `raw_data`, `cleaned_data`, `rejected_records`, a `summary`, and a tuple of `decisions`. Missing fields are reported and retained without imputation. Exact duplicate copies and rows with invalid dates, invalid numeric values, negative quantities, or negative sales are listed in `rejected_records` with their original values and a reason. Negative profit is allowed because losses can be valid sales outcomes.

### Analytics module

`src.analytics` provides independent functions for revenue, profit, quantity, distinct order count, average order value, monthly/yearly revenue, category/region totals, top product rankings, and customer purchasing summaries. Every function accepts optional inclusive `start_date` and `end_date` bounds. Order counts use distinct non-missing Order IDs rather than line-item counts. Averages return zero when the order denominator is zero.

### Visualizations

`src.visualizations` contains reusable Plotly builders for monthly sales and profit trends, category and regional performance, top products, category sales distribution, and customer purchasing. All figures use the same dark navy/cyan styling and show a readable empty state when the selected period has no records. The Streamlit page displays these charts after the uploaded file passes the required-column check.
