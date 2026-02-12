# PixelHue: Image Color Palette Generator - `script2stlite` Example

This directory contains Juncel Datinggaling's PixelHue Streamlit application, which has been converted into a self-contained static web application using the `script2stlite` package. PixelHue analyzes an image and extracts its dominant colors to generate a palette.

## Live Demo

You can view the output of this specific example hosted on GitHub Pages here: [https://lukeafullard.github.io/script2stlite/example/Example_5_PixelHue/PixelHue.html](https://lukeafullard.github.io/script2stlite/example/Example_5_PixelHue/PixelHue.html)

---

## One-Step Conversion (Recommended)

As of version 0.3.0, you can convert your app in a single step using the top-level `convert_app` function.

### 1. Prerequisites

Ensure `requirements.txt` is present in the directory.

### 2. Run the Conversion

Create a build script (e.g., `build.py`) and run it:

```python
import script2stlite

script2stlite.convert_app(
    directory="example/Example_5_PixelHue",
    app_name="PixelHue",
    entrypoint="main.py"
)
```

Run it to generate `PixelHue.html`.

---

## Original Application Credit

The PixelHue application was originally created by **Juncel Datinggaling**. We appreciate their work in developing this tool.

*   **Original Creator:** Juncel Datinggaling
*   **Original GitHub Repository:** [j-ncel/PixelHue](https://github.com/j-ncel/PixelHue)
*   **Original Live Streamlit App (requires Python backend):** [pixelhue.streamlit.app](https://pixelhue.streamlit.app/)

## `script2stlite`

The `script2stlite` package is a tool for converting Streamlit Python scripts into static HTML files that run entirely in the browser, powered by Pyodide. This is particularly useful as it allows complex Streamlit apps, even those with machine learning dependencies like scikit-learn, to run client-side without a Python backend.

This conversion simplifies deployment, allowing the application to be hosted on static web services like GitHub Pages or shared as a single HTML file.

## Functionality

The application allows users to:
1.  Upload an image (JPG, PNG, etc.).
2.  Specify the number of dominant colors to extract.
3.  View the uploaded image alongside the generated color palette (with HEX codes).

`script2stlite` turns the streamlit app to an stlite app to allow the app to run in the browser via Pyodide. The source Python script for this application is [main.py](./main.py) (which uses [palette_extractor.py](./palette_extractor.py)).

---

## Legacy Instructions (Manual Configuration)

If you prefer the manual configuration workflow:

### 1. Prepare

```python
from script2stlite import Script2StliteConverter
converter = Script2StliteConverter("example/Example_5_PixelHue")
converter.prepare_folder()
```

### 2. Configure `settings.yaml`

The `settings.yaml` file for this example is configured as follows:

```yaml
APP_NAME: "PixelHue"  #give your app a nice name
APP_REQUIREMENTS: #app requirements separated by a '-' on each new line. Requirements MUST be compatible with pyodide. Suggest specifying versions.
  - streamlit
  - scikit-learn==1.7.0
  - numpy
  - pillow
APP_ENTRYPOINT: main.py #entrypoint to app - change this to your main python file
CONFIG: false
APP_FILES:  #each file separated by a '-'. Can be .py files or other filetypes that will be converted to binary and embeded in the html.
  - koala.png
  - palette_extractor.py
```

### 3. Convert

```python
converter.convert()
```
