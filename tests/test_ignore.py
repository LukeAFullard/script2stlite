import os
import pytest
import shutil
from pathlib import Path
from script2stlite.script2stlite import convert_app

def test_ignore_files(tmp_path):
    # 1. Setup temporary directory
    app_dir = tmp_path / "app_ignore_test"
    app_dir.mkdir()

    # 2. Create files
    (app_dir / "app.py").write_text("import streamlit as st\nst.write('Hello')")
    (app_dir / "data.csv").write_text("a,b,c\n1,2,3")
    (app_dir / ".env").write_text("SECRET_KEY=123") # Default ignore
    (app_dir / "secret.txt").write_text("do not include me") # User ignore
    (app_dir / "included.txt").write_text("include me")

    # Create ignored directory (default)
    (app_dir / "build").mkdir()
    (app_dir / "build" / "data.txt").write_text("secret data")

    # Create ignored directory (user)
    (app_dir / "user_secret_dir").mkdir()
    (app_dir / "user_secret_dir" / "data.txt").write_text("user secret data")

    # 3. Convert app with user ignores
    convert_app(
        directory=str(app_dir),
        app_name="Ignore Test App",
        entrypoint="app.py",
        ignore_files=["secret.txt"],
        ignore_dirs=["user_secret_dir"]
    )

    # 4. Check generated HTML
    html_file = app_dir / "Ignore_Test_App.html"
    assert html_file.exists()

    html_content = html_file.read_text(encoding="utf-8")

    # 5. Assertions
    # Entrypoint should be there (content of app.py is embedded, but maybe not filename as key if it is entrypoint, wait.
    # Entrypoint is APP_HOME, embedded separately.
    assert "Hello" in html_content

    # APP_FILES:
    # "data.csv" should be present
    assert '"data.csv":' in html_content
    # "included.txt" should be present
    assert '"included.txt":' in html_content

    # Default ignored file should NOT be present
    assert '".env":' not in html_content
    assert '"build/data.txt":' not in html_content
    # Note: discover_all_files returns relative paths.

    # User ignored file should NOT be present
    assert '"secret.txt":' not in html_content

    # User ignored directory should NOT be present
    assert '"user_secret_dir/data.txt":' not in html_content
