# Example 9: IDBFS File Browser - Accessing Persistent Storage

This example serves as a companion to **Example 8: File Persistence Demo**. Its purpose is to demonstrate that files written to an `IDBFS` mount point are not only persistent within a single application but can also be accessed by other `stlite` applications running on the same domain.

This application will list the contents of the `/mnt` directory, which is configured to be a persistent storage area using the browser's IndexedDB.

`script2stlite` is a tool that packages your Streamlit application, along with its dependencies, into an HTML file that can be run in a web browser using [stlite](https://github.com/whitphx/stlite), without needing a Python backend server.

## Application Structure

The IDBFS File Browser application has a simple structure:

-   `home.py`: The main Streamlit script that lists the files and directories within the `/mnt` directory.
-   `settings.yaml`: The configuration file for `script2stlite`, which specifies the same `IDBFS_MOUNTPOINTS` as Example 8.

## Key Features Demonstrated

1.  **Shared Persistent Storage**: This example confirms that the `IDBFS_MOUNTPOINTS` provides a shared and persistent filesystem. By using the same mount point (`/mnt`) as Example 8, this application can access and display the files created by the other.
2.  **Inter-App Communication via Filesystem**: This demonstrates a powerful pattern for `stlite` applications: using the persistent filesystem as a way for different apps to share data or state without a server.
3.  **Reading Directory Contents**: The `home.py` script uses standard Python `os.walk()` to traverse the `/mnt` directory and list its contents, showing how to interact with the persistent filesystem.

## Steps to Convert This Streamlit App

The conversion process is standard, but the key is to run this example after running Example 8.

### 1. Run Example 8 First

Before running this application, you must first run **Example 8: File Persistence Demo** at least once. This will create the `/mnt/log.txt` file in your browser's IndexedDB.

### 2. Install `script2stlite`

Ensure you have `script2stlite` installed. If not, you can typically install it using pip:

```bash
pip install script2stlite
```
*(Note: Refer to the main project README for the most up-to-date installation instructions.)*

### 3. Review and Modify `settings.yaml`

The `settings.yaml` file for this example is:

```yaml
APP_NAME: "IDBFS File Browser"
APP_REQUIREMENTS:
  - streamlit
APP_ENTRYPOINT: home.py
CONFIG: "none"
IDBFS_MOUNTPOINTS: ['/mnt']
APP_FILES: []
```

Key aspects:

-   **`IDBFS_MOUNTPOINTS`**: Crucially, this is set to `['/mnt']`, the same as in Example 8. This tells `stlite` to connect to the same persistent storage area.

### 4. Convert the Application to HTML

With `settings.yaml` configured, convert the application.

```python
from script2stlite import Script2StliteConverter

# Initialize the converter
converter = Script2StliteConverter("example/Example_9_idbfs_file_browser")

# Convert the application
converter.convert()

print(f"Conversion complete! Check for '{converter.directory}/IDBFS_File_Browser.html'.")
```

### 5. View Your Application

Open the generated `IDBFS_File_Browser.html` in a web browser. You should see `log.txt` listed as a file in the `/mnt` directory. If you run Example 8 again, another timestamp will be added to the log, but the file listing here will remain the same.

You can view the output of this specific example hosted on GitHub Pages here:
[https://lukeafullard.github.io/script2stlite/example/Example_9_idbfs_file_browser/IDBFS_File_Browser.html](https://lukeafullard.github.io/script2stlite/example/Example_9_idbfs_file_browser/IDBFS_File_Browser.html)

---

This example, in conjunction with Example 8, effectively demonstrates the power and utility of the `IDBFS_MOUNTPOINTS` feature for creating stateful, browser-based applications with `script2stlite`.
