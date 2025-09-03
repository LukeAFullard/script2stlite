# Example 8: File Persistence Demo - Using `IDBFS_MOUNTPOINTS`

This example demonstrates how to achieve file persistence in a `stlite` application using the `IDBFS_MOUNTPOINTS` feature. The application writes a timestamp to a log file each time it's loaded, and this file is stored in the browser's IndexedDB, making it persistent across sessions.

`script2stlite` is a tool that packages your Streamlit application, along with its dependencies, into an HTML file that can be run in a web browser using [stlite](https://github.com/whitphx/stlite), without needing a Python backend server.

## Application Structure

The File Persistence Demo application has a simple structure:

-   `home.py`: The main Streamlit script that writes a timestamp to a log file and displays the file's contents.
-   `settings.yaml`: The configuration file for `script2stlite`, where the file persistence is enabled.

## Key Features Demonstrated

1.  **Persistent File Storage**: This example showcases the `IDBFS_MOUNTPOINTS` setting in `settings.yaml`. This feature allows you to specify directories that should be persisted in the browser's IndexedDB. Any files written to these directories by the application will be saved and available across page reloads and browser sessions.
2.  **Writing to the Persistent Filesystem**: The `home.py` script demonstrates how to write to a file within the mounted directory (`/mnt`). It appends the current timestamp to `log.txt` each time the app runs.
3.  **Reading from the Persistent Filesystem**: The application also reads the entire `log.txt` file and displays its contents, showing the accumulated timestamps from previous sessions.

## Steps to Convert This Streamlit App

The process is similar to other examples, with a focus on the `IDBFS_MOUNTPOINTS` setting.

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
converter = Script2StliteConverter("example/Example_8_file_persistence")

# Prepare the folder (optional if settings.yaml already exists)
# converter.prepare_folder()
```

### 3. Review and Modify `settings.yaml`

The `settings.yaml` file for this example is:

```yaml
APP_NAME: "File Persistence Demo"
APP_REQUIREMENTS:
  - streamlit
APP_ENTRYPOINT: home.py
CONFIG: "none"
IDBFS_MOUNTPOINTS: ['/mnt']
APP_FILES: []
```

Key aspects:

-   **`APP_NAME`**: Defines the application's title and the output HTML filename.
-   **`APP_REQUIREMENTS`**: Lists `streamlit`.
-   **`APP_ENTRYPOINT`**: The main `home.py` script.
-   **`IDBFS_MOUNTPOINTS`**: This is the crucial part. It's a list of directories that `stlite` will mount as a persistent filesystem using IndexedDB. In this case, the `/mnt` directory is persisted.

### 4. Convert the Application to HTML

With `settings.yaml` configured, convert the application.

```python
from script2stlite import Script2StliteConverter

# Initialize the converter
converter = Script2StliteConverter("example/Example_8_file_persistence")

# Convert the application
converter.convert()

print(f"Conversion complete! Check for '{converter.directory}/File_Persistence_Demo.html'.")
```

This command bundles `home.py` and the specified requirements into `File_Persistence_Demo.html`.

### 5. View Your Application

Open the generated `File_Persistence_Demo.html` in a web browser. Each time you reload the page, you will see a new timestamp added to the log file.

You can view the output of this specific example hosted on GitHub Pages here:
[https://lukeafullard.github.io/script2stlite/example/Example_8_file_persistence/File_Persistence_Demo.html](https://lukeafullard.github.io/script2stlite/example/Example_8_file_persistence/File_Persistence_Demo.html)

---

This example is a powerful demonstration of how to maintain state and user-generated data within a browser-based Streamlit application, all without a traditional server-side backend. For a complete experience, run this example first, then open **Example 9: IDBFS File Browser** to see how other applications can access the same persistent storage.
