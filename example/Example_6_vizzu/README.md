# Example 6: Vizzu Example (Custom Config)

This example shows how to include a `config.toml` file.

## One-Step Conversion (Recommended)

1.  **Prerequisites:**
    *   Ensure `requirements.txt` is present.

2.  **Convert:**
    Run the following Python script:

    ```python
    import script2stlite

    script2stlite.convert_app(
        directory="example/Example_6_vizzu",
        app_name="Vizzu example",
        entrypoint="streamlitvizzu.py",
        config=".streamlit/config.toml"  # Pass the config file path
    )
    ```

## Legacy Instructions

1.  **Prepare:**
    ```python
    from script2stlite import Script2StliteConverter
    converter = Script2StliteConverter("example/Example_6_vizzu")
    converter.prepare_folder()
    ```
2.  **Configure:** Edit `settings.yaml` (set `CONFIG: .streamlit/config.toml`).
3.  **Convert:**
    ```python
    converter.convert()
    ```
