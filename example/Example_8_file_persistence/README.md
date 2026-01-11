# Example 8: File Persistence Demo

Demonstrates using IDBFS for persistent storage.

## One-Step Conversion (Recommended)

1.  **Prerequisites:**
    *   Ensure `requirements.txt` is present.

2.  **Convert:**
    Run the following Python script:

    ```python
    import script2stlite

    script2stlite.convert_app(
        directory="example/Example_8_file_persistence",
        app_name="File Persistence Demo",
        entrypoint="home.py",
        idbfs_mountpoints=['/mnt'] # Specify mountpoints
    )
    ```

## Legacy Instructions

1.  **Prepare:**
    ```python
    from script2stlite import Script2StliteConverter
    converter = Script2StliteConverter("example/Example_8_file_persistence")
    converter.prepare_folder()
    ```
2.  **Configure:** Edit `settings.yaml` (set `IDBFS_MOUNTPOINTS: ['/mnt']`).
3.  **Convert:**
    ```python
    converter.convert()
    ```
