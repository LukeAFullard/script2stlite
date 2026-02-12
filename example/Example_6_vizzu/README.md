# Vizzu Streamlit Example

This directory contains an example of a Streamlit application using Vizzu for interactive data visualizations.

## Live Demo

This example has been adapted to run as a static web page using `script2stlite`.

*   **stlite HTML Page:** [https://lukeafullard.github.io/script2stlite/example/Example_6_vizzu/Vizzu_example.html](https://lukeafullard.github.io/script2stlite/example/Example_6_vizzu/Vizzu_example.html)

---

## One-Step Conversion (Recommended)

As of version 0.3.0, you can convert your app in a single step using the top-level `convert_app` function.

### 1. Prerequisites

Ensure `requirements.txt` is present in the directory.

### 2. Run the Conversion

Create a build script (e.g., `build.py`) and run it. Note how we pass the configuration file:

```python
import script2stlite

script2stlite.convert_app(
    directory="example/Example_6_vizzu",
    app_name="Vizzu example",
    entrypoint="streamlitvizzu.py",
    config=".streamlit/config.toml"  # Pass the config file path
)
```

Run it to generate `Vizzu_example.html`.

---

## Original Application Credit

The original Streamlit application was developed by **Germán Andrés** and **Castaño Vásquez**.

*   **Original GitHub Repository:** [gcastano/Streamlit-Demo-Apps/tree/main/StreamlitVizzu](https://github.com/gcastano/Streamlit-Demo-Apps/tree/main/StreamlitVizzu)
*   **Original Hosted Streamlit App:** [https://paris2024-olpympics-summary.streamlit.app/](https://paris2024-olpympics-summary.streamlit.app/)

---

## Legacy Instructions (Manual Configuration)

If you prefer the manual configuration workflow:

### 1. Prepare

```python
from script2stlite import Script2StliteConverter
converter = Script2StliteConverter("example/Example_6_vizzu")
converter.prepare_folder()
```

### 2. Configure `settings.yaml`

This example demonstrates the use of a `config.toml` file. The `settings.yaml` for `script2stlite` includes the `CONFIG` entry to specify the configuration file:

```yaml
APP_NAME: "Vizzu example"  #give your app a nice name
APP_REQUIREMENTS: #app requirements separated by a '-' on each new line. Requirements MUST be compatible with pyodide. Suggest specifying versions.
  - streamlit
  - ipyvizzu
  - pandas
  - ipyvizzu-story
APP_ENTRYPOINT: streamlitvizzu.py #entrypoint to app - change this to your main python file
CONFIG: .streamlit/config.toml
APP_FILES:  #each file separated by a '-'. Can be .py files or other filetypes that will be converted to binary and embeded in the html.
  - streamlitvizzuParalympics.py
  - Paris2024_Paralympics_Emblem.jpg
  - paralympic_2024_medallists.csv
  - medallists_with_age.csv
  - medallists.csv
  - Logo_Paris2024_OlyEmbleme.png
```

### 3. Convert

```python
converter.convert()
```
