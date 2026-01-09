# Example 10: MannKenSen Analysis App

A statistical analysis app.

## One-Step Conversion (Recommended)

1.  **Prerequisites:**
    *   Ensure `requirements.txt` is present.

2.  **Convert:**
    Run the following Python script:

    ```python
    from script2stlite import Script2StliteConverter

    converter = Script2StliteConverter("example/Example_10_MannKS")
    converter.convert_from_entrypoint(
        app_name="MannKenSen Analysis App",
        entrypoint="main.py"
    )
    ```

## Legacy Instructions

1.  **Prepare:**
    ```python
    from script2stlite import Script2StliteConverter
    converter = Script2StliteConverter("example/Example_10_MannKS")
    converter.prepare_folder()
    ```
2.  **Configure:** Edit `settings.yaml`.
3.  **Convert:**
    ```python
    converter.convert()
    ```
