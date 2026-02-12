# Example 0: Simple App - Using `script2stlite`

This example demonstrates the workflow of using `script2stlite` to convert a simple Streamlit application, consisting of a main script (`home.py`), a utility module (`functions.py`), and an image (`assets/image.jpg`), into a single self-contained HTML file.

`script2stlite` is a tool that packages your Streamlit application, along with its dependencies, into an HTML file that can be run in a web browser using [stlite](https://github.com/whitphx/stlite), without needing a Python backend server.

## Live Demo

You can view the output of this specific example hosted on GitHub Pages here: [https://lukeafullard.github.io/script2stlite/example/Example_0_simple_app/my_simple_app.html](https://lukeafullard.github.io/script2stlite/example/Example_0_simple_app/my_simple_app.html)

---

## One-Step Conversion (Recommended)

As of version 0.3.0, you can convert your app in a single step using the top-level `convert_app` function. This method automatically discovers your app's dependencies and assets.

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
import script2stlite

script2stlite.convert_app(
    directory="example/Example_0_simple_app",
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

If you prefer explicit control over every file included, or are using an older version of `script2stlite`, you can use the original process with `settings.yaml`.

### 1. Install script2stlite

Ensure you have `script2stlite` installed. If not, you can typically install it using pip:

```bash
pip install script2stlite
```
*(Note: Refer to the main project README for the most up-to-date installation instructions.)*

### 2. Prepare Your Project Folder

The first step is to prepare your project folder. `script2stlite` provides a helper function to set up the necessary basic structure and configuration file.

You can do this by running a Python script with the following content:

```python
from script2stlite import Script2StliteConverter

# Initialize the converter for the current directory or a specific path
# If no path is provided, it will use the current working directory.
# For this example, let's assume your script is in the 'Example_0_simple_app' folder.
converter = Script2StliteConverter("example/Example_0_simple_app") # Or simply Script2StliteConverter() if running from within the folder

# Prepare the folder
converter.prepare_folder()

print("Folder prepared. You should now have a 'settings.yaml' file and a 'pages' directory (if they didn't exist).")
```

When you run `prepare_folder()`:
*   It creates a `pages` directory if one doesn't already exist. This directory is conventionally used for multi-page Streamlit applications. While this simple example doesn't use multiple pages, the folder is created by the preparation step.
*   It creates a `settings.yaml` file in your project directory if one doesn't already exist. This YAML file is crucial for configuring the conversion process. If `settings.yaml` already exists, `prepare_folder()` will not overwrite it.

### 3. Modify `settings.yaml`

The `settings.yaml` file tells `script2stlite` about your application's structure, dependencies, and main entry point. You'll need to edit this file to match your project.

Here's the content of `settings.yaml` for this Example_0_simple_app:

```yaml
APP_NAME: "my simple app" #give your app a nice name
APP_REQUIREMENTS: #app requirements separated by a '-' on each new line. Requirements MUST be compatible with pyodide. Suggest specifying versions.
  - streamlit
  - pandas
  - numpy
APP_ENTRYPOINT: home.py #entrypoint to app - main python file
CONFIG: false
APP_FILES: #each file separated by a '-'. Can be .py files or other filetypes that will be converted to binary and embeded in the html.
  - functions.py #additional files for the conversion to find and include.
  - assets/image.jpg
```

Let's break down these settings:
*   **APP_NAME**: A user-friendly name for your application. This name will also be used for the output HTML file (e.g., `my_simple_app.html`).
*   **APP_REQUIREMENTS**: A list of Python packages your application needs. Each package should be on a new line, preceded by a hyphen (`-`). **Important**: These packages must be compatible with Pyodide (the Python runtime for WebAssembly). It's good practice to specify package versions to ensure compatibility (e.g., `pandas==1.5.3`).
*   **APP_ENTRYPOINT**: The main Python script for your Streamlit application (e.g., `home.py`). This is the script that `streamlit run <your_script.py>` would typically target.
*   **APP_FILES**: A list of other files that your application uses. This can include:
    *   Additional Python modules (like `functions.py` in this example).
    *   Data files (e.g., CSV, JSON).
    *   Assets like images (like `assets/image.jpg` in this example).
    *   Paths should be relative to the directory containing `settings.yaml`.

For your own projects, you will need to update these fields according to your application's specific files and dependencies.

### 4. Convert the Application to HTML

Once your `settings.yaml` is configured, you can convert your application into a single HTML file.

Add the following to your Python script (or create a new one):

```python
from script2stlite import Script2StliteConverter
import yaml

# Initialize the converter, pointing to your project directory
converter = Script2StliteConverter("example/Example_0_simple_app") # Or simply Script2StliteConverter() if running from this folder

# Convert the application
# You can optionally specify stlite_version and pyodide_version
# If not specified, the latest compatible versions will be used.
converter.convert()

# To print the exact output filename like above, you'd need to load settings first:
with open(f"{converter.directory}/settings.yaml", 'r') as f:
    settings = yaml.safe_load(f)

print(f"Conversion complete! Check for '{converter.directory}/{settings['APP_NAME'].replace(' ','_')}.html'.")
```
For this example, it will be `example/Example_0_simple_app/my_simple_app.html`.

Running `convert()` will:
1.  Read your `settings.yaml`.
2.  Collect all specified files (`APP_ENTRYPOINT` and `APP_FILES`).
3.  Package them along with the necessary stlite components and your listed `APP_REQUIREMENTS` into a single HTML file.
4.  The output HTML file will be named based on the `APP_NAME` in your `settings.yaml` (e.g., `my_simple_app.html`).

### 5. View Your Application

After the conversion, you'll find an HTML file (e.g., `my_simple_app.html`) in your project directory.

*   **Locally**: You can open this HTML file directly in a modern web browser (like Chrome, Firefox, Edge, Safari) to run your Streamlit application.
*   **Online**: This HTML file is self-contained and can be hosted on any static web hosting service (like GitHub Pages, Netlify, etc.).
