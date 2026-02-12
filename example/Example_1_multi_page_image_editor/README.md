# Example 1: Multi-Page Image Editor

This example demonstrates how to use `script2stlite` to convert a multi-page Streamlit application, specifically an image editor, into a single self-contained HTML file. This application includes multiple Python files organized in a `pages/` directory, an `assets/` folder, and specific package requirements (like `Pillow`).

`script2stlite` is a tool that packages your Streamlit application, along with its dependencies, into an HTML file that can be run in a web browser using [stlite](https://github.com/whitphx/stlite), without needing a Python backend server.

## Live Demo

You can view the output of this specific example hosted on GitHub Pages here: [https://lukeafullard.github.io/script2stlite/example/Example_1_multi_page_image_editor/Image_Editor.html](https://lukeafullard.github.io/script2stlite/example/Example_1_multi_page_image_editor/Image_Editor.html)

---

## One-Step Conversion (Recommended)

As of version 0.3.0, you can convert your app in a single step using the top-level `convert_app` function.

### 1. Prerequisites

Ensure you have your `requirements.txt` ready:
```text
streamlit
Pillow
```

### 2. Run the Conversion

Create a build script (e.g., `build.py`):

```python
import script2stlite

script2stlite.convert_app(
    directory="example/Example_1_multi_page_image_editor",
    app_name="Image Editor",
    entrypoint="app.py"
)
```

Run it to generate `Image_Editor.html`.

### Features
- **Multi-page support**: Demonstrates how `pages/` directory is automatically handled.
- **External libraries**: Uses `Pillow` for image manipulation.
- **Asset embedding**: Includes `assets/image.png` automatically.

---

## Legacy Instructions (Manual Configuration)

If you prefer explicit control over every file included, or are using an older version of `script2stlite`, you can use the original process with `settings.yaml`.

### Application Structure

The Image Editor application has the following structure:
*   `app.py`: The main entry point for the Streamlit application. It sets up the overall page configuration.
*   `pages/`: This directory contains the different pages of the application:
    *   `01_Home.py`: The landing page.
    *   `02_Upload_Image.py`: Page for uploading images.
    *   `03_Adjust_Image.py`: Page for performing image adjustments like brightness, contrast, rotation, and grayscale.
*   `assets/`: Contains static assets, like a sample image (`image.png`).
*   `settings.yaml`: The configuration file for `script2stlite`.

### 1. Install script2stlite

Ensure you have `script2stlite` installed. If not, you can typically install it using pip:

```bash
pip install script2stlite
```
*(Note: Refer to the main project README for the most up-to-date installation instructions.)*

### 2. Prepare Your Project Folder

If you were starting from scratch, you would use `converter.prepare_folder()`. This command creates a `settings.yaml` file (if one doesn't exist) and a `pages` directory. For this example, these are already provided.

```python
from script2stlite import Script2StliteConverter

# Initialize the converter for this example's directory
converter = Script2StliteConverter("example/Example_1_multi_page_image_editor")

# Prepare the folder (optional if settings.yaml and pages/ already exist)
# converter.prepare_folder()
```

### 3. Review and Modify `settings.yaml`

The `settings.yaml` file is key to correctly packaging the multi-page application. Here's the content for this Example 1:

```yaml
APP_NAME: "Image Editor"
APP_REQUIREMENTS:
  - streamlit
  - Pillow # For image manipulation
APP_ENTRYPOINT: app.py # Main app file that sets page config
CONFIG: false
APP_FILES:
  - pages/01_Home.py
  - pages/02_Upload_Image.py
  - pages/03_Adjust_Image.py
  - assets/image.png
```

Key aspects for a multi-page app:
*   **APP_NAME**: Defines the application's title and the output HTML filename (e.g., `Image_Editor.html`).
*   **APP_REQUIREMENTS**: Lists necessary Python packages. `Pillow` is crucial for the image processing features. Remember, these must be Pyodide-compatible.
*   **APP_ENTRYPOINT**: This should be your main script, typically the one that might contain `st.set_page_config()` and acts as the primary entry point. For multi-page apps, this is often a small `app.py` or similar, while individual pages reside in the `pages/` directory.
*   **APP_FILES**: This is where you list all the Python files for each page within the `pages` directory. You also include any assets like images or data files.
*   *Note: `script2stlite` automatically recognizes and processes the `pages/` directory convention for Streamlit multi-page apps if your entry point and page files are structured correctly. Listing them explicitly ensures they are included.*

### 4. Convert the Application to HTML

With `settings.yaml` configured, convert the application:

```python
from script2stlite import Script2StliteConverter

# Initialize the converter
converter = Script2StliteConverter("example/Example_1_multi_page_image_editor")

# Convert the application
converter.convert()

print(f"Conversion complete! Check for '{converter.directory}/Image_Editor.html'.")
```
This command bundles `app.py`, all files in `pages/`, the assets, and the specified requirements into `Image_Editor.html`.

### 5. View Your Application

Open the generated `Image_Editor.html` in a web browser. You should see the multi-page image editor application, allowing you to navigate between home, upload, and adjust pages.

This example showcases how `script2stlite` handles multi-page applications and dependencies, making it easy to share complex Streamlit projects as single HTML files.
