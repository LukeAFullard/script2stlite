# Example 3: Streamlit Cheat Sheet

A conversion of the official Streamlit cheat sheet.

## One-Step Conversion (Recommended)

1.  **Prerequisites:**
    *   Ensure `requirements.txt` is present.

2.  **Convert:**
    Run the following Python script:

    ```python
    from script2stlite import Script2StliteConverter

    converter = Script2StliteConverter("example/Example_3_streamlit_chect_sheet")
    converter.convert_from_entrypoint(
        app_name="Streamlit cheat sheet",
        entrypoint="app.py"
    )
    ```

## Legacy Instructions

1.  **Prepare:**
    ```python
    from script2stlite import Script2StliteConverter
    converter = Script2StliteConverter("example/Example_3_streamlit_chect_sheet")
    converter.prepare_folder()
    ```
2.  **Configure:** Edit `settings.yaml`.
3.  **Convert:**
    ```python
    converter.convert()
    ```
