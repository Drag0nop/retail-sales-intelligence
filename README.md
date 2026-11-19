# Retail Sales Intelligence Dashboard

A local Streamlit dashboard for exploring retail sales trends by date, category, region, customer segment, and customer. The dashboard reads the project's included CSV automatically; you do not need to upload a file.

## Run the dashboard

Use Python 3.9 or newer. From the project folder, create and activate a virtual environment, install the dependencies, and start Streamlit:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

On macOS or Linux, activate the environment with:

```bash
source .venv/bin/activate
```

Streamlit prints a local URL in the terminal, usually `http://localhost:8501`. Open it in a browser. Stop the server with **Ctrl+C** in the terminal.

## Data and analysis

The app first looks for `retail_sales_cleaned.csv` beside `app.py`. If that file is missing, it loads `retail.csv` instead. Both files are included in this project. The cleaned CSV is the preferred source and is produced by the final cell of `analysis.ipynb`.

The dashboard provides:

- Date, region, category, and customer segment filters
- Summary metrics for sales, distinct orders, customers, and average order value
- Monthly sales, category and regional comparisons, customer segment mix, top customers, and sales versus quantity charts
- A filtered records table and a button to download the filtered rows as a CSV

The dataset has sales and quantity fields, but no profit, discount, or product name fields. The dashboard and notebook use metrics supported by the data and do not estimate those missing values.

`analysis.ipynb` contains the exploratory analysis and writes `retail_sales_cleaned.csv` when its last cell runs. To work with the notebook, open it in Jupyter Notebook or JupyterLab and run its cells in order. The notebook uses `retail.csv` as its input.

## Project files

| File | Purpose |
| --- | --- |
| `app.py` | Streamlit dashboard, filters, charts, and automatic CSV loading. |
| `analysis.ipynb` | Notebook exploration and generation of the cleaned CSV. |
| `retail.csv` | Source retail records used by the notebook and as the app's fallback. |
| `retail_sales_cleaned.csv` | Cleaned dataset loaded by the app by default. |
| `requirements.txt` | Python dependencies for the dashboard and project. |
| `README.md` | Project overview and run instructions. |

## Dependencies

The dashboard uses Streamlit for the interface, Pandas for data handling, and Plotly for interactive charts. Install the versions declared in `requirements.txt` with the setup command above.
