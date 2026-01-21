import os
import pytest
from script2stlite.discovery import discover_all_files

def test_inclusion_of_all_files(tmp_path):
    """
    Verify that all files in the directory are discovered, regardless of usage.
    This covers dynamic imports, f-string assets, and unused files.
    """
    app_dir = tmp_path / "app"
    app_dir.mkdir()

    # Create various files
    (app_dir / "main.py").write_text("import foo")
    (app_dir / "foo.py").write_text("x=1")
    (app_dir / "data.csv").write_text("data")
    (app_dir / "unused.txt").write_text("unused")
    (app_dir / ".env").write_text("SECRET=1") # Should be ignored by default

    # Create subdirectories
    (app_dir / "pages").mkdir()
    (app_dir / "pages/page1.py").write_text("st.write('page')")

    (app_dir / "utils").mkdir()
    (app_dir / "utils/__init__.py").write_text("")
    (app_dir / "utils/helper.py").write_text("def help(): pass")

    # Run discovery
    files = discover_all_files(str(app_dir))

    # Assertions
    assert "main.py" in files
    assert "foo.py" in files
    assert "data.csv" in files
    assert "unused.txt" in files
    assert "pages/page1.py" in files
    assert "utils/__init__.py" in files
    assert "utils/helper.py" in files

    # Default ignores
    assert ".env" not in files

def test_ignored_directories(tmp_path):
    """
    Verify that standard ignored directories are skipped.
    """
    app_dir = tmp_path / "app"
    app_dir.mkdir()

    (app_dir / "code.py").write_text("print(1)")

    # .git
    (app_dir / ".git").mkdir()
    (app_dir / ".git/config").write_text("config")

    # __pycache__
    (app_dir / "__pycache__").mkdir()
    (app_dir / "__pycache__/code.cpython-39.pyc").write_text("bin")

    # venv
    (app_dir / "venv").mkdir()
    (app_dir / "venv/bin").mkdir()
    (app_dir / "venv/bin/python").write_text("bin")

    files = discover_all_files(str(app_dir))

    assert "code.py" in files
    assert ".git/config" not in files
    assert "__pycache__/code.cpython-39.pyc" not in files
    assert "venv/bin/python" not in files

def test_custom_ignores(tmp_path):
    """
    Verify that custom ignore sets work.
    """
    app_dir = tmp_path / "app"
    app_dir.mkdir()

    (app_dir / "keep.txt").write_text("keep")
    (app_dir / "ignore_me.txt").write_text("ignore")

    files = discover_all_files(str(app_dir), ignore_files={'ignore_me.txt'})

    assert "keep.txt" in files
    assert "ignore_me.txt" not in files
