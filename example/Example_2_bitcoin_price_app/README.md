# Example 2: Bitcoin Price Tracker

This example fetches data from an API and displays it using Plotly.

## One-Step Conversion (Recommended)

1.  **Prerequisites:**
    *   Ensure `requirements.txt` is present.

2.  **Convert:**
    Run the following Python script:

    ```python
    import script2stlite

    script2stlite.convert_app(
        directory="example/Example_2_bitcoin_price_app",
        app_name="Current BTC vs USD Price Tracker",
        entrypoint="app.py"
    )
    ```

## Legacy Instructions

1.  **Prepare:**
    ```python
    from script2stlite import Script2StliteConverter
    converter = Script2StliteConverter("example/Example_2_bitcoin_price_app")
    converter.prepare_folder()
    ```
2.  **Configure:** Edit `settings.yaml`.
3.  **Convert:**
    ```python
    converter.convert()
    ```
