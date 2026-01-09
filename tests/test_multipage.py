import os
import pytest
from script2stlite import Script2StliteConverter

def test_multipage_auto_discovery(tmp_path):
    # Setup temporary app
    app_dir = tmp_path / "multipage_app"
    app_dir.mkdir()

    # Main entrypoint
    (app_dir / "app.py").write_text("import streamlit as st\nst.write('Home')", encoding="utf-8")

    # Pages directory
    pages_dir = app_dir / "pages"
    pages_dir.mkdir()
    (pages_dir / "page1.py").write_text("import streamlit as st\nst.write('Page 1')", encoding="utf-8")
    (pages_dir / "page2.py").write_text("import helper\nst.write('Page 2')", encoding="utf-8")

    # Helper module used by a page (to test recursive discovery from pages)
    (app_dir / "helper.py").write_text("def foo(): pass", encoding="utf-8")

    converter = Script2StliteConverter(directory=str(app_dir))

    # Run conversion
    converter.convert_from_entrypoint(
        app_name="Multipage App",
        entrypoint="app.py"
    )

    output_html = app_dir / "Multipage_App.html"
    assert output_html.exists()

    content = output_html.read_text(encoding="utf-8")

    # Check for pages
    # Currently expected to FAIL until implemented
    assert '"pages/page1.py":' in content
    assert '"pages/page2.py":' in content

    # Check for recursive dependency from page2
    assert '"helper.py":' in content
