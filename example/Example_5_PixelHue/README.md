# Example 5: PixelHue (ML Example)

An example using scikit-learn for image color extraction.

## One-Step Conversion (Recommended)

1.  **Prerequisites:**
    *   Ensure `requirements.txt` is present.

2.  **Convert:**
    Run the following Python script:

    ```python
    from script2stlite import Script2StliteConverter

    converter = Script2StliteConverter("example/Example_5_PixelHue")
    converter.convert_from_entrypoint(
        app_name="PixelHue",
        entrypoint="main.py"
    )
    ```

## Legacy Instructions

1.  **Prepare:**
    ```python
    from script2stlite import Script2StliteConverter
    converter = Script2StliteConverter("example/Example_5_PixelHue")
    converter.prepare_folder()
    ```
2.  **Configure:** Edit `settings.yaml`.
3.  **Convert:**
    ```python
    converter.convert()
    ```
