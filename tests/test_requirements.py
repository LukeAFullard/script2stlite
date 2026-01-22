import os
import pytest
from script2stlite import Script2StliteConverter

def test_requirements_file_merging(tmp_path):
    # Setup temporary app
    app_dir = tmp_path / "req_app"
    app_dir.mkdir()

    (app_dir / "main.py").write_text("import streamlit as st", encoding="utf-8")

    # settings.yaml with one requirement
    (app_dir / "settings.yaml").write_text(
        """
APP_NAME: "Req App"
APP_REQUIREMENTS:
  - streamlit
APP_ENTRYPOINT: main.py
APP_FILES: []
        """,
        encoding="utf-8"
    )

    # requirements.txt with new and duplicate requirements
    (app_dir / "requirements.txt").write_text(
        """
pandas
streamlit
numpy>=1.20
# A comment
        """,
        encoding="utf-8"
    )

    converter = Script2StliteConverter(directory=str(app_dir))
    converter.convert()

    output_html = app_dir / "Req_App.html"
    assert output_html.exists()

    content = output_html.read_text(encoding="utf-8")

    # Parse requirements from the generated HTML JS object: requirements: ['...', ...]
    # We can just check string presence for now

    # streamlit should be there (from settings or reqs)
    assert "'streamlit'" in content

    # pandas should be there (from reqs)
    assert "'pandas'" in content

    # numpy>=1.20 should be there (from reqs)
    assert "'numpy>=1.20'" in content

def test_requirements_file_only(tmp_path):
    # Setup temporary app with NO requirements in settings
    app_dir = tmp_path / "req_app_2"
    app_dir.mkdir()

    (app_dir / "main.py").write_text("import streamlit as st", encoding="utf-8")

    (app_dir / "settings.yaml").write_text(
        """
APP_NAME: "Req App 2"
# No APP_REQUIREMENTS key
APP_ENTRYPOINT: main.py
APP_FILES: []
        """,
        encoding="utf-8"
    )

    (app_dir / "requirements.txt").write_text("matplotlib", encoding="utf-8")

    converter = Script2StliteConverter(directory=str(app_dir))
    converter.convert()

    output_html = app_dir / "Req_App_2.html"
    content = output_html.read_text(encoding="utf-8")

    assert "'matplotlib'" in content
