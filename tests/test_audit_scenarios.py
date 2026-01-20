import os
import pytest
from script2stlite.discovery import find_imports, find_assets

def test_audit_f_string_asset(tmp_path):
    """
    Caveat: Assets referenced via constructed strings (e.g. f-strings) are NOT detected.
    Only static string literals are detected.
    """
    app_dir = tmp_path / "app"
    app_dir.mkdir()

    # Create a dummy data file
    (app_dir / "data.csv").write_text("data")

    # Case 1: F-string (Dynamic) - NOT Detected
    code_dynamic = """
filename = "data"
ext = ".csv"
st.write(f"{filename}{ext}")
    """
    (app_dir / "app_dynamic.py").write_text(code_dynamic)

    assets_dynamic = find_assets(str(app_dir / "app_dynamic.py"), str(app_dir))
    assert "data.csv" not in assets_dynamic

    # Case 2: Static String Literal - Detected
    code_static = """
st.write("data.csv")
    """
    (app_dir / "app_static.py").write_text(code_static)

    assets_static = find_assets(str(app_dir / "app_static.py"), str(app_dir))
    assert "data.csv" in assets_static


def test_audit_dynamic_imports(tmp_path):
    """
    Caveat: Dynamic imports (e.g. importlib) are NOT detected.
    """
    app_dir = tmp_path / "app"
    app_dir.mkdir()

    (app_dir / "helper.py").write_text("x=1")

    code_dynamic = """
import importlib
importlib.import_module('helper')
    """
    (app_dir / "app.py").write_text(code_dynamic)

    imports = find_imports(str(app_dir / "app.py"), str(app_dir))
    assert "helper.py" not in imports


def test_audit_false_positive_asset(tmp_path):
    """
    Caveat/Issue: String literals that match a local filename are included as assets,
    even if the string is used for something else (e.g. an exclusion list, a variable value).
    """
    app_dir = tmp_path / "app"
    app_dir.mkdir()

    # A file that we might NOT want to include, or just happens to exist
    (app_dir / "secret.key").write_text("SECRET")

    # Code that mentions the filename in a string
    code = """
exclude_files = ["secret.key"]
print("Ignored files:", exclude_files)
    """
    (app_dir / "app.py").write_text(code)

    assets = find_assets(str(app_dir / "app.py"), str(app_dir))

    # Current behavior: It IS found and included.
    assert "secret.key" in assets

def test_audit_wildcard_imports(tmp_path):
    """
    Caveat: 'from package import *' only includes package/__init__.py.
    It does not scan the package directory for other modules unless __init__.py imports them.
    Logic relying on __all__ to export non-imported submodules will fail to bundle them.
    """
    app_dir = tmp_path / "app"
    app_dir.mkdir()

    pkg_dir = app_dir / "pkg"
    pkg_dir.mkdir()
    (pkg_dir / "__init__.py").write_text("__all__ = ['submodule']")
    (pkg_dir / "submodule.py").write_text("x=1")

    code = """
from pkg import *
    """
    (app_dir / "app.py").write_text(code)

    imports = find_imports(str(app_dir / "app.py"), str(app_dir))

    # It finds __init__.py
    assert "pkg/__init__.py" in imports
    # It does NOT find submodule.py because it wasn't imported in __init__.py
    assert "pkg/submodule.py" not in imports

def test_audit_complex_imports(tmp_path):
    """
    Verification: Complex relative and nested imports work correctly.
    """
    app_dir = tmp_path / "app"
    app_dir.mkdir()

    # Structure:
    # app.py -> imports pkg.sub.deep
    # pkg/sub/deep.py -> imports ..sibling and .local

    pkg_dir = app_dir / "pkg"
    pkg_dir.mkdir()
    (pkg_dir / "__init__.py").write_text("")
    (pkg_dir / "sibling.py").write_text("s=1")

    sub_dir = pkg_dir / "sub"
    sub_dir.mkdir()
    (sub_dir / "__init__.py").write_text("")
    (sub_dir / "local.py").write_text("l=1")
    (sub_dir / "deep.py").write_text("from .. import sibling\nfrom . import local")

    (app_dir / "app.py").write_text("import pkg.sub.deep")

    imports = find_imports(str(app_dir / "app.py"), str(app_dir))

    assert "pkg/sub/deep.py" in imports
    assert "pkg/sibling.py" in imports
    assert "pkg/sub/local.py" in imports
