import os
import pytest
from script2stlite import Script2StliteConverter

def test_convert_from_entrypoint(tmp_path):
    # Setup temporary app
    app_dir = tmp_path / "simple_app"
    app_dir.mkdir()

    # Create main app file
    (app_dir / "app.py").write_text("import streamlit as st\nimport helper", encoding="utf-8")
    (app_dir / "helper.py").write_text("x=1", encoding="utf-8")

    # Create requirements.txt
    (app_dir / "requirements.txt").write_text("pandas", encoding="utf-8")

    # Instantiate converter
    converter = Script2StliteConverter(directory=str(app_dir))

    # Run new conversion method
    converter.convert_from_entrypoint(
        app_name="Simple App",
        entrypoint="app.py"
    )

    output_html = app_dir / "Simple_App.html"
    assert output_html.exists()

    content = output_html.read_text(encoding="utf-8")

    # Check App Name
    assert "<title>Simple App</title>" in content

    # Check Requirements (pandas from requirements.txt)
    assert "'pandas'" in content

    # Check Entrypoint
    assert 'entrypoint: "app.py"' in content

    # Check Auto-Discovery (helper.py)
    assert '"helper.py":' in content

def test_convert_from_entrypoint_with_extra_files(tmp_path):
    # Setup
    app_dir = tmp_path / "extra_app"
    app_dir.mkdir()
    (app_dir / "app.py").write_text("print('hi')", encoding="utf-8")
    (app_dir / "manual_asset.txt").write_text("data", encoding="utf-8")

    converter = Script2StliteConverter(directory=str(app_dir))

    converter.convert_from_entrypoint(
        app_name="Extra App",
        entrypoint="app.py",
        extra_files=["manual_asset.txt"]
    )

    output_html = app_dir / "Extra_App.html"
    assert output_html.exists()

    content = output_html.read_text(encoding="utf-8")
    assert '"manual_asset.txt":' in content
