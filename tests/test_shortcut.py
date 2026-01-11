import os
import pytest
import script2stlite

def test_convert_app_shortcut(tmp_path):
    # Setup temporary app
    app_dir = tmp_path / "shortcut_app"
    app_dir.mkdir()

    (app_dir / "app.py").write_text("import streamlit as st", encoding="utf-8")

    # Run shortcut function
    script2stlite.convert_app(
        directory=str(app_dir),
        app_name="Shortcut App",
        entrypoint="app.py"
    )

    output_html = app_dir / "Shortcut_App.html"
    assert output_html.exists()

    content = output_html.read_text(encoding="utf-8")
    assert "<title>Shortcut App</title>" in content
    assert 'entrypoint: "app.py"' in content
