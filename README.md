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

The current app is a foundation shell. Data ingestion and business analysis will be implemented in later phases. SQLite is available through Python's standard library and will only be introduced if persistent local storage is useful.

## Project structure and file purposes

| Path | Purpose |
| --- | --- |
| `app.py` | Streamlit entry point and page composition. |
| `requirements.txt` | Python packages needed by the project. |
| `README.md` | Setup instructions, architecture overview, and file guide. |
| `data/` | Local input datasets supplied by the user. |
| `src/__init__.py` | Marks `src` as the reusable data and analytics package. |
| `src/data_loader.py` | Future CSV/Excel loading and input validation. |
| `src/data_cleaning.py` | Future reusable cleaning and type-normalization routines. |
| `src/analytics.py` | Future business metrics and aggregations. |
| `src/visualizations.py` | Future Plotly chart construction. |
| `src/report_generator.py` | Future export of analysis summaries and reports. |
| `database/__init__.py` | Marks `database` as the local persistence package. |
| `database/db.py` | Future SQLite connection and persistence helpers, if needed. |
| `components/__init__.py` | Marks `components` as reusable Streamlit UI components. |
| `components/sidebar.py` | Future sidebar controls and dataset filters. |
| `components/kpi_cards.py` | Future reusable KPI card rendering. |
| `components/charts.py` | Future chart display components. |
| `assets/style.css` | Optional app styling overrides. |
| `tests/test_cleaning.py` | Future unit tests for data cleaning behavior. |
| `tests/test_analytics.py` | Future unit tests for calculated metrics. |
| `outputs/reports/` | Local destination for generated reports. |

No sample or fabricated sales data is included. This keeps displayed results tied to an actual dataset provided for analysis.
