# Example 3: Streamlit Cheat Sheet - `stlite` Conversion Example

This directory contains an example of a Streamlit application, the "Streamlit Cheat Sheet," which has been converted into a self-contained `stlite` application using the `script2stlite` package.

## Live Demo

You can view the output of this specific example hosted on GitHub Pages here: [https://lukeafullard.github.io/script2stlite/example/Example_3_streamlit_chect_sheet/Streamlit_cheat_sheet.html](https://lukeafullard.github.io/script2stlite/example/Example_3_streamlit_chect_sheet/Streamlit_cheat_sheet.html)

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
    directory="example/Example_3_streamlit_chect_sheet",
    app_name="Streamlit cheat sheet",
    entrypoint="app.py"
)
```

Run it to generate `Streamlit_cheat_sheet.html`.

---

## Original Application Credit

The original "Streamlit Cheat Sheet" application was created by **Daniel Lewis**. We extend our gratitude to him for developing this excellent resource for the Streamlit community.

*   **Original Application Source Code**: [https://github.com/daniellewisDL/streamlit-cheat-sheet](https://github.com/daniellewisDL/streamlit-cheat-sheet)
*   **Original App Running on Streamlit Servers**: [https://cheat-sheet.streamlit.app/](https://cheat-sheet.streamlit.app/)

## `script2stlite` and `stlite`

The `script2stlite` package is a useful tool for converting existing Streamlit applications into `stlite` applications. `stlite` allows you to run Streamlit apps entirely in the browser, packaged as a single HTML file. This is incredibly beneficial as it eliminates the need for traditional server-side hosting, making deployment simpler and more accessible.

With `stlite`, your Streamlit app becomes a portable HTML file that can be easily shared or hosted on static web hosting services like GitHub Pages.

---

## Legacy Instructions (Manual Configuration)

If you prefer the manual configuration workflow:

1.  **Prepare:**
    ```python
    from script2stlite import Script2StliteConverter
    converter = Script2StliteConverter("example/Example_3_streamlit_chect_sheet")
    converter.prepare_folder()
    ```
2.  **Configure:** Edit the generated `settings.yaml`.
3.  **Convert:**
    ```python
    converter.convert()
    ```
