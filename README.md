# script2stlite

A Python package to convert Streamlit applications into single, self-contained HTML files that run entirely in the browser using [stlite](https://github.com/whitphx/stlite).

This allows you to easily share or deploy your Streamlit apps as static web pages without needing a Python backend server.

## Features

*   **Prepare Project Folders**: Initialize a directory with the necessary structure (`pages` subdirectory) and a template `settings.yaml` configuration file.
*   **Convert to HTML**: Bundle your Streamlit application (main script, pages, requirements, and other assets) into a single HTML file.
*   **Class-Based Conversion**: Offers a `Script2StliteConverter` class for an object-oriented approach to managing the conversion process.
*   **Version Pinning**: Allows specifying particular versions of `stlite` and `Pyodide` to be used for the conversion.
*   **Automatic Dependency Handling**: Reads your Python package requirements from `settings.yaml` and includes them in the `stlite` build.

## Installation

You can install `script2stlite` using pip:

```bash
pip install script2stlite
```

## Quick Start

Here's how to get started with `script2stlite`:

### 1. Prepare Your Project Folder

First, you need a directory for your Streamlit application. `script2stlite` uses a class `Script2StliteConverter` to manage project setup and conversion.

```python
from script2stlite import Script2StliteConverter

# Initialize the converter, optionally specifying a target directory.
# If no directory is provided, it defaults to the current working directory.
converter = Script2StliteConverter(directory="my_stlite_app")

# This will create 'my_stlite_app' (if it doesn't exist),
# a 'pages' subdirectory inside it, and a template 'settings.yaml' file.
converter.prepare_folder()
```

This sets up the basic structure needed for your `stlite` application.

### 2. Configure `settings.yaml`

The `s2s_prepare_folder` command creates a `settings.yaml` file in your project directory. You'll need to customize this file. Here’s an example:

```yaml
APP_NAME: "My Awesome Stlite App"
APP_ENTRYPOINT: "streamlit_app.py"  # Your main Streamlit script
APP_REQUIREMENTS:
  - "streamlit"
  - "pandas"
  - "numpy"
  # Add any other packages your app needs
APP_FILES:
  - "pages/01_📊_Data_Explorer.py" # For multi-page apps
  - "pages/02_ℹ️_About.py"
  - "utils/helpers.py"          # Other Python modules
  - "data/my_data.csv"          # Data files
  - "assets/logo.png"           # Image assets
# - "models/model.pkl"          # Binary files like pickled models (will be base64 encoded)
```

**Explanation of `settings.yaml` fields:**

*   `APP_NAME`: The name of your application. This will be used as the title of the generated HTML page and the filename.
*   `APP_ENTRYPOINT`: The main Python script for your Streamlit application (e.g., `streamlit_app.py`). This path is relative to your project directory (where `settings.yaml` is located).
*   `APP_REQUIREMENTS`: A list of Python packages required by your application. These packages must be Pyodide-compatible.
*   `APP_FILES`: A list of other files and directories to include in the `stlite` bundle. All paths are relative to your project directory.
    *   For multi-page Streamlit apps, include your page scripts here, typically located in a `pages` subdirectory (e.g., `pages/page1.py`, `pages/page2.py`).
    *   You can also include other Python modules, data files (CSV, JSON, etc.), and assets (images, etc.).
    *   Binary files (e.g., `.png`, `.jpg`, `.pkl`) will be base64 encoded and embedded into the HTML. Python (`.py`) and text-based files (`.csv`, `.txt`, etc.) will be embedded as raw text.

Make sure all files listed in `APP_ENTRYPOINT` and `APP_FILES` exist at their specified paths relative to your project directory.

### 3. Create Your Streamlit App Files

Create your main Streamlit script (e.g., `streamlit_app.py`) and any other scripts or files (like those in the `pages` directory or data files) that your application needs.

**Example `streamlit_app.py`:**
```python
import streamlit as st
import pandas as pd

st.title("Simple Stlite App")

st.write("Welcome to your Streamlit app running in the browser!")

# Example: Load data if 'data/my_data.csv' is in APP_FILES
try:
    df = pd.read_csv("data/my_data.csv")
    st.dataframe(df)
except FileNotFoundError:
    st.warning("data/my_data.csv not found. Add it to your project and settings.yaml.")
except Exception as e:
    st.error(f"Could not load data/my_data.csv: {e}")


name = st.text_input("Enter your name:", "World")
st.write(f"Hello, {name}!")
```

**Example `pages/01_📊_Data_Explorer.py` (for a multi-page app):**
```python
import streamlit as st

st.set_page_config(page_title="Data Explorer", layout="wide")

st.title("📊 Data Explorer")
st.write("This is a page in your multi-page app!")
# Add more Streamlit components here
```

### 4. Convert Your Project to HTML

Once your `settings.yaml` is configured and your app files are ready, you can convert the project into a single HTML file using the `convert` method of your `Script2StliteConverter` instance.

```python
# Assuming 'converter' is the Script2StliteConverter instance from step 1,
# and you have configured "my_stlite_app/settings.yaml" and created your app files.
# For example:
# from script2stlite import Script2StliteConverter
# converter = Script2StliteConverter(directory="my_stlite_app")
# (after settings.yaml and app files are ready in "my_stlite_app")

converter.convert()
# This will read 'settings.yaml' from 'my_stlite_app',
# bundle all specified files, and generate 'My Awesome Stlite App.html'
# (or whatever APP_NAME is) inside the 'my_stlite_app' directory.
```

The `Script2StliteConverter` class is the primary way to interact with `script2stlite`. While functional equivalents like `s2s_prepare_folder` and `s2s_convert` exist, using the class provides a more cohesive workflow, especially if you need to perform multiple operations or manage state.

After conversion, you can open the generated HTML file in any modern web browser to run your Streamlit application.

## How it Works

`script2stlite` streamlines the process of packaging your Streamlit application for browser-only execution. Here's a simplified overview:

1.  **Configuration Reading**: The tool reads your project's structure and dependencies from the `settings.yaml` file. This includes your main application script (`APP_ENTRYPOINT`), any additional pages or Python modules (`APP_FILES`), and Python package requirements (`APP_REQUIREMENTS`).
2.  **File Aggregation**: It collects all specified Python scripts, data files, and assets. Python files and text-based data files are read as strings. Binary files (like images) are base64 encoded.
3.  **HTML Generation**: `script2stlite` uses an HTML template that is pre-configured to use `stlite`. It injects your application's details into this template:
    *   The content of your main Streamlit script (`APP_ENTRYPOINT`) becomes the primary script executed by `stlite`.
    *   Other Python files and data files from `APP_FILES` are embedded into the `stlite` virtual filesystem, making them accessible to your application at runtime.
    *   The package `APP_REQUIREMENTS` are listed for `stlite` to install via `micropip` from Pyodide.
    *   Links to the necessary `stlite` CSS and JavaScript bundles, and the specified Pyodide version, are included.
4.  **Bundling**: The result is a single HTML file. This file contains your entire Streamlit application (code, data, assets) and the `stlite` runtime environment.
5.  **Browser Execution**: When you open this HTML file in a web browser:
    *   `stlite` initializes Pyodide, which is a port of Python to WebAssembly.
    *   The specified Python packages are downloaded and installed into the Pyodide environment.
    *   Your Streamlit application code is executed by the Python interpreter running in the browser.
    *   Streamlit components are rendered directly in the HTML page, providing the interactive experience.

Essentially, `script2stlite` automates the setup described in the `stlite` documentation for self-hosting, packaging everything neatly into one portable HTML file. It leverages `stlite`'s ability to run Streamlit applications without a server by bringing the Python runtime and Streamlit framework into the browser environment.

## Limitations

Since `script2stlite` relies on `stlite` and Pyodide, it inherits their limitations. Key considerations include:

*   **Pyodide Package Compatibility**:
    *   All Python packages listed in `APP_REQUIREMENTS` must be compatible with Pyodide. This generally means they should be pure Python or have pre-compiled WebAssembly wheels available.
    *   Packages with complex binary dependencies that are not specifically ported to the Pyodide environment will not work.
    *   For more details on Pyodide package support, see:
        *   [Pyodide FAQ on pure Python wheels](https://pyodide.org/en/stable/usage/faq.html#why-can-t-micropip-find-a-pure-python-wheel-for-a-package)
        *   [Packages available in Pyodide](https://pyodide.org/en/stable/usage/packages-in-pyodide.html)

*   **Inherited `stlite` Limitations**:
    *   `st.spinner()`: May not display correctly with blocking methods due to the single-threaded browser environment. A workaround is to use `await asyncio.sleep(0.1)` before the blocking call.
    *   `st.bokeh_chart()`: Currently does not work as Pyodide uses Bokeh 3.x while Streamlit supports 2.x.
    *   `time.sleep()`: Is a no-op. Use `await asyncio.sleep()` instead (requires using `async` functions and top-level await where necessary).
    *   `st.write_stream()`: Should be used with async generator functions for reliable behavior.
    *   **DataFrame Serialization**: Minor differences in how some data types in DataFrame columns are handled by `st.dataframe()`, `st.data_editor()`, `st.table()`, and Altair-based charts, because `stlite` uses Parquet for serialization instead of Arrow IPC.
    *   **Micropip Version Resolution**: Package version resolution by `micropip` (used by Pyodide) can sometimes fail or lead to unexpected versions, especially with complex dependencies.
    *   For a comprehensive list of `stlite` limitations, refer to the official [stlite documentation](https://github.com/whitphx/stlite#limitations).

*   **File System**:
    *   The default file system (MEMFS) provided by `stlite`/Pyodide is ephemeral. Any files written by your application at runtime (e.g., saving a generated file) will be lost when the browser tab is closed or reloaded.
    *   `stlite` supports persistent storage using IDBFS (IndexedDB File System). However, `script2stlite` does not currently offer a direct configuration option in `settings.yaml` to set up IDBFS mount points. Implementing persistent storage would require manual modification of the generated HTML to include the `idbfsMountpoints` option in the `stlite.mount()` call, as described in the [stlite documentation on file persistence](https://github.com/whitphx/stlite#file-persistence-with-indexeddb-backend).

*   **HTTP Requests**:
    *   Standard Python networking libraries like `socket` do not work directly in the browser.
    *   For making HTTP requests, use Pyodide-specific mechanisms like `pyodide.http.pyfetch()` or `pyodide.http.open_url()`.
    *   The `requests` library and parts of `urllib` are patched by `pyodide-http` to work in many common cases, but some advanced features might not be available. See the [stlite documentation on HTTP requests](https://github.com/whitphx/stlite#http-requests) and [pyodide-http](https://github.com/koenvo/pyodide-http) for details.

*   **Performance**:
    *   Initial load time can be significant, as the browser needs to download Pyodide, `stlite`, and your application's packages.
    *   CPU-intensive Python operations will run slower in the browser (via WebAssembly) compared to a native Python environment.

*   **Browser Environment**:
    *   Direct access to the local file system (outside the virtual Pyodide FS) or system resources is not possible due to browser security restrictions.

## Advanced Usage

### Specifying `stlite` and `Pyodide` Versions

You can control the versions of `stlite` (which also dictates the Streamlit version) and `Pyodide` used in the generated HTML file. This is useful for ensuring compatibility or using specific features from particular releases.

Pass the `stlite_version` and/or `pyodide_version` arguments to the `convert` method of the `Script2StliteConverter` class.

```python
from script2stlite import Script2StliteConverter

converter = Script2StliteConverter(directory="my_stlite_app")

# Example: Pin stlite to version 0.46.0 and Pyodide to 0.23.4
# Ensure settings.yaml and app files are ready in "my_stlite_app" first.
# converter.prepare_folder() # if needed
converter.convert(
    stlite_version="0.46.0",  # Check available stlite versions
    pyodide_version="0.23.4"  # Check available Pyodide versions compatible with stlite
)
```

`script2stlite` comes with lists of known compatible versions (see `stlite_versions` directory in the package). If you specify a version not listed, it might lead to errors if the CDN links are incorrect or the versions are incompatible. By default, the latest known compatible versions are used.

### Overriding Package Versions in Requirements (Conceptual)

The `Script2StliteConverter.convert()` method includes a `packages` parameter (a dictionary). This parameter is intended for fine-grained control over package versions, potentially overriding what's listed in `APP_REQUIREMENTS` or how they are formatted for `micropip`.

**Example (Illustrative):**

```python
from script2stlite import Script2StliteConverter

converter = Script2StliteConverter(directory="my_stlite_app")

# This is a more advanced use case, typically APP_REQUIREMENTS is sufficient.
# Ensure settings.yaml and app files are ready in "my_stlite_app" first.
# converter.prepare_folder() # if needed
converter.convert(
    packages={"pandas": "pandas==1.5.3", "numpy": "numpy>=1.20.0,<1.23.0"}
)
```

In this example, if `APP_REQUIREMENTS` in `settings.yaml` just listed `pandas` and `numpy`, the `packages` argument would provide more specific version constraints for `micropip`.

However, for most use cases, defining your requirements directly in the `APP_REQUIREMENTS` list in `settings.yaml` with appropriate version specifiers (e.g., `pandas==1.5.3`, `matplotlib>=3.5`) is the recommended approach. The `packages` parameter offers an override mechanism primarily for scenarios where `settings.yaml` cannot be easily modified or for programmatic adjustments.

## Contributing

Contributions are welcome! If you have suggestions for improvements, new features, or bug fixes, please feel free to:

1.  Open an issue to discuss the change.
2.  Fork the repository and submit a pull request.

Please ensure that your code adheres to standard Python conventions and include tests if applicable.

(If a `CONTRIBUTING.md` file exists with more detailed guidelines, it would be linked here.)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
