# Example 0: Simple App - Using `script2stlite`

This example demonstrates the workflow of using `script2stlite` to convert a simple Streamlit application, consisting of a main script (`home.py`), a utility module (`functions.py`), and an image (`assets/image.jpg`), into a single self-contained HTML file.

`script2stlite` is a tool that packages your Streamlit application, along with its dependencies, into an HTML file that can be run in a web browser using [stlite](https://github.com/whitphx/stlite), without needing a Python backend server.

## One-Step Conversion (Recommended)

As of version 0.3.0, you can convert your app in a single step using the `convert_from_entrypoint` method. This method automatically discovers your app's dependencies and assets.

### 1. Prerequisites

Ensure your project folder contains:
*   Your Streamlit scripts (e.g., `home.py`, `functions.py`).
*   Any assets (e.g., `assets/image.jpg`).
*   A `requirements.txt` file listing your dependencies.

For this example, `requirements.txt` should contain:
```text
streamlit
pandas
numpy
```

### 2. Run the Conversion

Create a python script (e.g., `build.py`) with the following content and run it:

```python
from script2stlite import Script2StliteConverter

# Initialize the converter pointing to this example folder
converter = Script2StliteConverter(directory="example/Example_0_simple_app")

# Convert the app
converter.convert_from_entrypoint(
    app_name="my simple app",
    entrypoint="home.py"
)
```

Running this script will:
1.  Parse `home.py` and automatically find that it imports `functions.py`.
2.  Scan your code and automatically find the reference to `assets/image.jpg`.
3.  Read `requirements.txt` to install `streamlit`, `pandas`, and `numpy`.
4.  Generate `my_simple_app.html` in the directory.

### 3. View Your Application

Open the generated `my_simple_app.html` in your browser!

---

## Legacy Instructions (Manual Configuration)

If you prefer explicit control over every file included, or are using an older version of `script2stlite`, you can use the original 4-step process with `settings.yaml`.

### 1. Prepare Your Project Folder

Run the following Python code to generate a `settings.yaml` template:

```python
from script2stlite import Script2StliteConverter

converter = Script2StliteConverter("example/Example_0_simple_app")
converter.prepare_folder()
```

### 2. Modify `settings.yaml`

Edit the generated `settings.yaml` to match your project:

```yaml
APP_NAME: "my simple app"
APP_REQUIREMENTS:
  - streamlit
  - pandas
  - numpy
APP_ENTRYPOINT: home.py
CONFIG: false
APP_FILES:
  - functions.py
  - assets/image.jpg
```

### 3. Convert the Application

Run the conversion method:

```python
from script2stlite import Script2StliteConverter

converter = Script2StliteConverter("example/Example_0_simple_app")
converter.convert()
```

This reads the `settings.yaml` and generates the HTML file. Note that in v0.3.0+, `converter.convert()` also performs auto-discovery, merging discovered files with those listed in your `settings.yaml`.
