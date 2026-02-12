# Example 8: File Persistence Demo - Using `IDBFS_MOUNTPOINTS`

This example demonstrates how to achieve file persistence in a `stlite` application using the `IDBFS_MOUNTPOINTS` feature. The application writes a timestamp to a log file each time it's loaded, and this file is stored in the browser's IndexedDB, making it persistent across sessions.

`script2stlite` is a tool that packages your Streamlit application, along with its dependencies, into an HTML file that can be run in a web browser using [stlite](https://github.com/whitphx/stlite), without needing a Python backend server.

## Live Demo

You can view the output of this specific example hosted on GitHub Pages here: [https://lukeafullard.github.io/script2stlite/example/Example_8_file_persistence/File_Persistence_Demo.html](https://lukeafullard.github.io/script2stlite/example/Example_8_file_persistence/File_Persistence_Demo.html)

---

## One-Step Conversion (Recommended)

As of version 0.3.0, you can convert your app in a single step using the top-level `convert_app` function.

### 1. Prerequisites

Ensure `requirements.txt` is present in the directory.

### 2. Run the Conversion

Create a build script (e.g., `build.py`) and run it. Note how we specify the mount points:

```python
import script2stlite

script2stlite.convert_app(
    directory="example/Example_8_file_persistence",
    app_name="File Persistence Demo",
    entrypoint="home.py",
    idbfs_mountpoints=['/mnt'] # Specify mountpoints
)
```

Run it to generate `File_Persistence_Demo.html`.

---

## Key Features Demonstrated

1.  **Persistent File Storage**: This example showcases the `IDBFS_MOUNTPOINTS` setting. This feature allows you to specify directories that should be persisted in the browser's IndexedDB. Any files written to these directories by the application will be saved and available across page reloads and browser sessions.
2.  **Writing to the Persistent Filesystem**: The `home.py` script demonstrates how to write to a file within the mounted directory (`/mnt`). It appends the current timestamp to `log.txt` each time the app runs.
3.  **Reading from the Persistent Filesystem**: The application also reads the entire `log.txt` file and displays its contents, showing the accumulated timestamps from previous sessions.

## Application Structure

The File Persistence Demo application has a simple structure:

-   `home.py`: The main Streamlit script that writes a timestamp to a log file and displays the file's contents.
-   `settings.yaml`: The configuration file for `script2stlite`, where the file persistence is enabled.

---

## Legacy Instructions (Manual Configuration)

If you prefer explicit control over every file included, or are using an older version of `script2stlite`, you can use the original process with `settings.yaml`.

### 1. Prepare

```python
from script2stlite import Script2StliteConverter

# Initialize the converter for this example's directory
converter = Script2StliteConverter("example/Example_8_file_persistence")

# Prepare the folder (optional if settings.yaml already exists)
# converter.prepare_folder()
```

### 2. Configure `settings.yaml`

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

### 3. Convert

```python
from script2stlite import Script2StliteConverter

# Initialize the converter
converter = Script2StliteConverter("example/Example_8_file_persistence")

# Convert the application
converter.convert()

print(f"Conversion complete! Check for '{converter.directory}/File_Persistence_Demo.html'.")
```

This command bundles `home.py` and the specified requirements into `File_Persistence_Demo.html`.

---

This example is a powerful demonstration of how to maintain state and user-generated data within a browser-based Streamlit application, all without a traditional server-side backend. For a complete experience, run this example first, then open **Example 9: IDBFS File Browser** to see how other applications can access the same persistent storage.
