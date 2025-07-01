# Example 2: Bitcoin Price Tracker - Using `script2stlite` with `requests`

This example demonstrates how to use `script2stlite` to convert a Streamlit application that utilizes the `requests` library to fetch data from an external API. Specifically, this app displays the current Bitcoin price in USD by calling the CoinDesk API.

A key feature highlighted in this example is the ability to specify exact versions for `stlite` and `pyodide` during the conversion process, ensuring consistent and reproducible builds.

`script2stlite` is a tool that packages your Streamlit application, along with its dependencies, into an HTML file that can be run in a web browser using [stlite](https://github.com/whitphx/stlite), without needing a Python backend server.

## Application Structure

The Bitcoin Price Tracker application has a simple structure:

-   `app.py`: The main Streamlit script that fetches and displays the Bitcoin price.
-   `settings.yaml`: The configuration file for `script2stlite`.

## Key Features Demonstrated

1.  **Using the `requests` library**: The application makes an HTTP GET request to an external API (`https://api.coindesk.com/v1/bpi/currentprice.json`) from within the `stlite` environment to fetch real-time data. This shows that network requests are possible in `stlite` applications if the target API supports CORS or if run in an environment that relaxes same-origin policies (though typically, public APIs are accessible).
2.  **Specifying `stlite` and `pyodide` versions**: This example explicitly sets the versions for `stlite` and `pyodide` to ensure the application behaves consistently across different environments and times. This was achieved by calling the `convert` method with specific arguments:
    ```python
    converter.convert(stlite_version='0.82.0', pyodide_version='0.26.4')
    ```
    where `converter` is an instance of the `Script2StliteConverter` class. This is crucial for long-term stability and debugging.

## Steps to Convert This Streamlit App

The process is similar to other examples, with a focus on the `requests` dependency and version specification.

### 1. Install `script2stlite`

Ensure you have `script2stlite` installed. If not, you can typically install it using pip:

```bash
pip install script2stlite
```
*(Note: Refer to the main project README for the most up-to-date installation instructions.)*

### 2. Prepare Your Project Folder (Optional)

If you were starting from scratch, you might use `converter.prepare_folder()`. For this example, `settings.yaml` is already provided.

```python
from script2stlite import Script2StliteConverter

# Initialize the converter for this example's directory
converter = Script2StliteConverter("example/Example_2_bitcoin_price_app")

# Prepare the folder (optional if settings.yaml already exists)
# converter.prepare_folder()
```

### 3. Review and Modify `settings.yaml`

The `settings.yaml` file for this example is:

```yaml
APP_NAME: "Current BTC vs USD Price Tracker"  #give your app a nice name
APP_REQUIREMENTS: #app requirements separated by a '-' on each new line. Requirements MUST be compatible with pyodide. Suggest specifying versions.
  - streamlit
  - requests
  - plotly
  - pandas
APP_ENTRYPOINT: app.py #entrypoint to app - change this to your main python file
CONFIG: false
APP_FILES:  #each file separated by a '-'. Can be .py files or other filetypes that will be converted to binary and embeded in the html.
  - assets/image.png #you can include non python files - they will be embedded in the html in binary format
```

Key aspects:

-   **`APP_NAME`**: Defines the application's title and the output HTML filename.
-   **`APP_REQUIREMENTS`**: Lists `streamlit`, `requests`, `plotly`, and `pandas`. These libraries must be compatible with the Pyodide environment. `requests` is crucial for making API calls, and `plotly`/`pandas` are often used for data manipulation and visualization.
-   **`APP_ENTRYPOINT`**: The main `app.py` script.
-   **`APP_FILES`**: Includes `assets/image.png`, demonstrating that non-Python files like images can be bundled with the application.

### 4. Convert the Application to HTML

With `settings.yaml` configured, convert the application. This is where we specify the `stlite` and `pyodide` versions.

```python
from script2stlite import Script2StliteConverter

# Initialize the converter
converter = Script2StliteConverter("example/Example_2_bitcoin_price_app")

# Convert the application, specifying stlite and pyodide versions
converter.convert(stlite_version='0.82.0', pyodide_version='0.26.4')

print(f"Conversion complete! Check for '{converter.directory}/Current_BTC_vs_USD_Price_Tracker.html'.")
```

This command bundles `app.py` and the specified requirements into `Current_BTC_vs_USD_Price_Tracker.html`, using `stlite v0.82.0` and `pyodide v0.26.4`.

### 5. View Your Application

Open the generated `Current_BTC_vs_USD_Price_Tracker.html` in a web browser. You should see the application fetching and displaying the current Bitcoin price.

You can view the output of this specific example hosted on GitHub Pages here:
[https://lukeafullard.github.io/script2stlite/example/Example_2_bitcoin_price_app/Current_BTC_vs_USD_Price_Tracker.html](https://lukeafullard.github.io/script2stlite/example/Example_2_bitcoin_price_app/Current_BTC_vs_USD_Price_Tracker.html)

---

This example highlights `script2stlite`'s capability to package applications that interact with external APIs and demonstrates the important practice of pinning `stlite` and `pyodide` versions for stable, reproducible browser-based applications.
