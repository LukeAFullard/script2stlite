# Example 1: Multi-Page Image Editor

This example demonstrates how to convert a multi-page Streamlit application with image processing capabilities (using Pillow) into a standalone HTML file.

## One-Step Conversion (Recommended)

Ensure you have your `requirements.txt` ready:
```text
streamlit
Pillow
```

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

## Features
- **Multi-page support**: Demonstrates how `pages/` directory is automatically handled.
- **External libraries**: Uses `Pillow` for image manipulation.
- **Asset embedding**: Includes `assets/image.png` automatically.
