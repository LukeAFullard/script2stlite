# Example 2: Bitcoin Price Tracker

This example shows how to convert a Streamlit app that fetches data from an API (CoinDesk) and visualizes it using Plotly.

## One-Step Conversion (Recommended)

Ensure you have your `requirements.txt` ready:
```text
streamlit
requests
plotly
pandas
```

Create a build script (e.g., `build.py`):

```python
import script2stlite

script2stlite.convert_app(
    directory="example/Example_2_bitcoin_price_app",
    app_name="Current BTC vs USD Price Tracker",
    entrypoint="app.py"
)
```

Run it to generate `Current_BTC_vs_USD_Price_Tracker.html`.

## Features
- **Data Fetching**: Uses `requests` to get live data.
- **Visualization**: Uses `plotly` for interactive charts.
- **Pandas**: Uses `pandas` for data manipulation.
