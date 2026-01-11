# Example 9: IDBFS File Browser

A file browser for the persistent IDBFS storage.

## One-Step Conversion (Recommended)

1.  **Prerequisites:**
    *   Ensure `requirements.txt` is present.

2.  **Convert:**
    Run the following Python script:

    ```python
    import script2stlite

    script2stlite.convert_app(
        directory="example/Example_9_idbfs_file_browser",
        app_name="IDBFS File Browser",
        entrypoint="home.py",
        idbfs_mountpoints=['/mnt'] # Specify mountpoints
    )
    ```

## Legacy Instructions

1.  **Prepare:**
    ```python
    from script2stlite import Script2StliteConverter
    converter = Script2StliteConverter("example/Example_9_idbfs_file_browser")
    converter.prepare_folder()
    ```
2.  **Configure:** Edit `settings.yaml` (set `IDBFS_MOUNTPOINTS: ['/mnt']`).
3.  **Convert:**
    ```python
    converter.convert()
    ```
