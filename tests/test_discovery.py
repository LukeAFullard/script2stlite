import os
import pytest
from script2stlite.discovery import find_imports, find_assets
from script2stlite import Script2StliteConverter

def test_find_imports_and_assets(tmp_path):
    # Setup temporary app structure
    app_dir = tmp_path / "app"
    app_dir.mkdir()

    # Create main app file
    entrypoint = app_dir / "app.py"
    entrypoint.write_text(
        """
import streamlit as st
import helper
from utils import formatting

st.write("Hello")
st.image("assets/logo.png")
with open("data/info.txt") as f:
    st.write(f.read())
        """,
        encoding="utf-8"
    )

    # Create imported modules
    (app_dir / "helper.py").write_text("def help(): pass", encoding="utf-8")

    utils_dir = app_dir / "utils"
    utils_dir.mkdir()
    (utils_dir / "__init__.py").write_text("", encoding="utf-8")
    (utils_dir / "formatting.py").write_text("def format(): pass", encoding="utf-8")

    # Create assets
    assets_dir = app_dir / "assets"
    assets_dir.mkdir()
    (assets_dir / "logo.png").write_bytes(b"fake image data")

    data_dir = app_dir / "data"
    data_dir.mkdir()
    (data_dir / "info.txt").write_text("Some info", encoding="utf-8")

    # Test find_imports
    root_dir = str(app_dir)
    script_path = str(entrypoint)

    imports = find_imports(script_path, root_dir)
    assert "helper.py" in imports
    # Depending on implementation, utils/__init__.py might be implicitly found if we imported from utils
    # or utils/formatting.py if we imported from utils.formatting or from utils import formatting
    # The current implementation resolves 'utils' if 'from utils import ...' ?
    # In 'from utils import formatting', node.module is 'utils' (if from list) or 'utils.formatting'?
    # Wait, 'from utils import formatting':
    # node.module = 'utils'
    # alias.name = 'formatting'
    # resolve_module('utils', ...) -> utils.py or utils/__init__.py
    # resolve_module('formatting', base=utils_dir) -> formatting.py

    # Let's check what my code actually does with 'from utils import formatting'
    # It likely sees node.module='utils'. It resolves 'utils'.
    # Then it sees alias 'formatting'?
    # In `find_imports`:
    # elif isinstance(node, ast.ImportFrom):
    #   ...
    #   if module_name: ... local_files = resolve_module(module_name, base_dir)

    # So if `from utils import formatting`, module_name is 'utils'. It finds `utils/__init__.py`.
    # It does NOT verify 'formatting' inside unless I iterate alias.names?
    # My current implementation for `if module_name:` only resolves the module_name.
    # So it catches `utils/__init__.py`.
    # It might miss `utils/formatting.py` if I don't look at names.
    # However, `helper.py` should be found (import helper).

    # Let's verify what is found.
    # We now strictly expect "utils/formatting.py" because "from utils import formatting"
    # implies we want the formatting submodule if it exists as a file.
    assert "utils/formatting.py" in imports

    # Test find_assets
    assets = find_assets(script_path, root_dir, imports)
    assert "assets/logo.png" in assets
    assert "data/info.txt" in assets
    assert "app.py" not in assets

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
