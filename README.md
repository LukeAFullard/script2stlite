# script2stlite

A Python package to convert Streamlit applications into single, self-contained HTML files that run entirely in the browser using [stlite](https://github.com/whitphx/stlite).

This allows you to easily share or deploy your Streamlit apps as static web pages without needing a Python backend server.  

This project was created to easily allow **existing** streamlit apps to be converted to stlite web apps. Another GREAT way to generate stlite web apps is using [https://edit.share.stlite.net/](https://edit.share.stlite.net/)  

The creator of stlite and edit.share.stlite.net is [Yuichiro Tachibana (whitphx)](https://github.com/whitphx/stlite)

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

## Quick Start with `Example_0_simple_app`

This quick start guide uses the example application located in the `example/Example_0_simple_app` directory of this repository.

### 1. Initialize the Converter and Prepare the Folder

First, you'll use the `Script2StliteConverter` class. Point it to the directory containing the example application. Then, call `prepare_folder()` to ensure the necessary `settings.yaml` file is present (it will be created from a template if it doesn't exist) and a `pages` subdirectory is available.

```python
from script2stlite import Script2StliteConverter

# Initialize the converter with the path to the example app
# If you have cloned the repository, this path will be relative to the repo root.
converter = Script2StliteConverter(directory="example/Example_0_simple_app")

# Prepare the folder. This creates 'settings.yaml' if it's missing
# and ensures a 'pages' directory exists.
# For this example, 'settings.yaml' is already provided.
converter.prepare_folder()
```

### 2. Review `settings.yaml`

The `prepare_folder()` step ensures a `settings.yaml` file is in place. For `Example_0_simple_app`, the `settings.yaml` file looks like this:

```yaml
APP_NAME: "my simple app"  #give your app a nice name
APP_REQUIREMENTS: #app requirements separated by a '-' on each new line. Requirements MUST be compatible with pyodide. Suggest specifying versions.
  - streamlit
  - pandas
  - numpy
APP_ENTRYPOINT: home.py #entrypoint to app - main python file
APP_FILES:  #each file separated by a '-'. Can be .py files or other filetypes that will be converted to binary and embeded in the html.
  - functions.py #additional files for the conversion to find and include.
  - assets/image.jpg
```

**Key fields in this example:**
*   `APP_NAME`: "my simple app" - This will be used for the HTML file name and page title.
*   `APP_REQUIREMENTS`: Lists `streamlit`, `pandas`, and `numpy`.
*   `APP_ENTRYPOINT`: `home.py` - This is the main script for the Streamlit app.
*   `APP_FILES`: Includes `functions.py` (a supporting Python module) and `assets/image.jpg` (an image asset).

### 3. Review the Streamlit Application Code

The main application script for this example is `example/Example_0_simple_app/home.py`:

```python
import streamlit as st
from functions import random_pandas_dataframe

#say something
st.write("This text is from home.py")

#get a dataframe
st.write("The dataframe below is from functions.py")
df = random_pandas_dataframe()
st.write(df)

#show an image
st.write("The image below in in the assets folder, but is embeded into the html file.")
st.image("assets/image.jpg")
```
This script imports a function from `functions.py` (which is listed in `APP_FILES`), displays some text, shows a Pandas DataFrame, and an image.

### 4. Convert Your Project to HTML

With the folder prepared and settings reviewed, you can convert the project into a single HTML file using the `convert()` method:

```python
# Assuming 'converter' is the Script2StliteConverter instance from Step 1.
converter.convert()

# This will read 'settings.yaml' from 'example/Example_0_simple_app',
# bundle all specified files, and generate 'my_simple_app.html'
# inside the 'example/Example_0_simple_app' directory.
```

After running this, you will find `my_simple_app.html` in the `example/Example_0_simple_app` directory. You can open this file in any modern web browser to run the Streamlit application.

You can also view a hosted version of this example here:
[https://lukeafullard.github.io/script2stlite/example/Example_0_simple_app/my_simple_app.html](https://lukeafullard.github.io/script2stlite/example/Example_0_simple_app/my_simple_app.html)

## Other Examples

For more examples (as they become available), please check the `example` directory in this repository. Each subfolder there will typically contain a self-contained Streamlit application ready for conversion with `script2stlite`.

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

# Example: Pin stlite to version 0.82.0 and Pyodide to 0.27.4
# Ensure settings.yaml and app files are ready in "my_stlite_app" first.
# converter.prepare_folder() # if needed
converter.convert(
    stlite_version="0.82.0",  # Check available stlite versions
    pyodide_version="0.27.4"  # Check available Pyodide versions compatible with stlite
)
```

`script2stlite` comes with lists of known compatible versions (see `stlite_versions` directory in the repository). If you specify a version not listed, it might lead to errors if the CDN links are incorrect or the versions are incompatible. By default, the latest known compatible versions are used.

### Overriding Package Versions in Requirements

The `Script2StliteConverter.convert()` method includes a `packages` parameter (a dictionary). This parameter is intended for fine-grained control over package versions, potentially overriding what's listed in `APP_REQUIREMENTS` or how they are formatted for `micropip`.

**Example:**

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

However, for most use cases, defining your requirements directly in the `APP_REQUIREMENTS` list in `settings.yaml` with appropriate version specifiers (e.g., `pandas==1.5.3`, `matplotlib>=3.5`) is the recommended approach. The `packages` parameter offers an override mechanism primarily for scenarios where the user would like to keepa series of stlite apps on the same package versions. In theory this should reduce loading time for users since a single version of a package is downloaded, rather than multiple versions.

## Contributing

Contributions are welcome! If you have suggestions for improvements, new features, or bug fixes, please feel free to:

1.  Open an issue to discuss the change.
2.  Fork the repository and submit a pull request.

Please ensure that your code adheres to standard Python conventions.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
