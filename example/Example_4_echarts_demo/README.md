# Example 4: ECharts Demo

A complex app with many submodules and data files.

## One-Step Conversion (Recommended)

1.  **Prerequisites:**
    *   Ensure `requirements.txt` is present.

2.  **Convert:**
    Run the following Python script:

    ```python
    from script2stlite import Script2StliteConverter

    converter = Script2StliteConverter("example/Example_4_echarts_demo")
    converter.convert_from_entrypoint(
        app_name="Streamlit echarts demo",
        entrypoint="app.py"
    )
    ```

    `script2stlite` will recursively discover all imported modules in `demo_echarts/` and `demo_pyecharts/`, as well as data files in `data/`.

## Legacy Instructions

1.  **Prepare:**
    ```python
    from script2stlite import Script2StliteConverter
    converter = Script2StliteConverter("example/Example_4_echarts_demo")
    converter.prepare_folder()
    ```
2.  **Configure:** Edit `settings.yaml`.
3.  **Convert:**
    ```python
    converter.convert()
    ```
