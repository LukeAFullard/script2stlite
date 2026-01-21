import os
import pytest
from script2stlite.discovery import discover_all_files
from script2stlite import Script2StliteConverter

def test_discover_all_files(tmp_path):
    # Setup temporary app structure
    app_dir = tmp_path / "app"
    app_dir.mkdir()

    # Create files
    entrypoint = app_dir / "app.py"
    entrypoint.write_text("content", encoding="utf-8")

    (app_dir / "helper.py").write_text("content", encoding="utf-8")

    utils_dir = app_dir / "utils"
    utils_dir.mkdir()
    (utils_dir / "__init__.py").write_text("", encoding="utf-8")
    (utils_dir / "formatting.py").write_text("content", encoding="utf-8")

    assets_dir = app_dir / "assets"
    assets_dir.mkdir()
    (assets_dir / "logo.png").write_bytes(b"fake image data")

    data_dir = app_dir / "data"
    data_dir.mkdir()
    (data_dir / "info.txt").write_text("Some info", encoding="utf-8")

    # Test discover_all_files
    root_dir = str(app_dir)
    files = discover_all_files(root_dir)

    assert "app.py" in files
    assert "helper.py" in files
    assert "utils/__init__.py" in files
    assert "utils/formatting.py" in files
    assert "assets/logo.png" in files
    assert "data/info.txt" in files

def test_integration_with_converter(tmp_path):
    # Setup temporary app
    app_dir = tmp_path / "test_app"
    app_dir.mkdir()

    (app_dir / "main.py").write_text("import sub; st.write('Hi')", encoding="utf-8")
    (app_dir / "sub.py").write_text("x=1", encoding="utf-8")
    (app_dir / "settings.yaml").write_text(
        """
APP_NAME: "Test App"
APP_REQUIREMENTS:
  - streamlit
APP_ENTRYPOINT: main.py
APP_FILES: []
        """,
        encoding="utf-8"
    )

    converter = Script2StliteConverter(directory=str(app_dir))
    converter.convert()

    output_html = app_dir / "Test_App.html"
    assert output_html.exists()

    content = output_html.read_text(encoding="utf-8")
    assert '"sub.py":' in content
