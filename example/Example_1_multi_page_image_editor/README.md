# Example 1: Multi-Page Image Editor

This example demonstrates how to convert a multi-page Streamlit application.

## One-Step Conversion (Recommended)

1.  **Prerequisites:**
    *   Ensure `requirements.txt` is present (it should list `streamlit` and `Pillow`).

2.  **Convert:**
    Run the following Python script:

    ```python
    import script2stlite

    script2stlite.convert_app(
        directory="example/Example_1_multi_page_image_editor",
        app_name="Image Editor",
        entrypoint="app.py"
    )
    ```

    `script2stlite` will automatically detect the `pages/` directory and include all subpages (`01_Home.py`, etc.) and assets.

## Legacy Instructions

1.  **Prepare:**
    ```python
    from script2stlite import Script2StliteConverter
    converter = Script2StliteConverter("example/Example_1_multi_page_image_editor")
    converter.prepare_folder()
    ```
2.  **Configure:** Edit `settings.yaml`.
3.  **Convert:**
    ```python
    converter.convert()
    ```
