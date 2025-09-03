import os
import pytest
import yaml
from script2stlite.script2stlite import s2s_prepare_folder, s2s_convert
from script2stlite.functions import load_yaml_from_file

def test_s2s_prepare_folder(tmp_path):
    # Test creating folder structure in an empty directory
    project_dir = tmp_path / "my_project"
    project_dir.mkdir()

    s2s_prepare_folder(str(project_dir))

    pages_dir = project_dir / "pages"
    settings_file = project_dir / "settings.yaml"

    assert pages_dir.is_dir()
    assert settings_file.is_file()

    # Verify content of settings.yaml (optional, but good practice)
    settings_data = load_yaml_from_file(settings_file)
    assert "APP_NAME" in settings_data

    # Test that it doesn't overwrite existing settings.yaml
    with open(settings_file, "w") as f:
        f.write("APP_NAME: My Custom App\n")

    s2s_prepare_folder(str(project_dir))

    new_settings_data = load_yaml_from_file(settings_file)
    assert new_settings_data["APP_NAME"] == "My Custom App"

    # Test with non-existent directory (should raise ValueError)
    with pytest.raises(ValueError):
        s2s_prepare_folder("non_existent_dir")


def test_s2s_convert_simple_app(tmp_path, mocker):
    # 1. Create a mock project
    project_dir = tmp_path / "my_project"
    project_dir.mkdir()
    (project_dir / "pages").mkdir()
    (project_dir / "assets").mkdir()

    # Create settings.yaml
    settings = {
        "APP_NAME": "My Test App",
        "APP_ENTRYPOINT": "app.py",
        "APP_FILES": ["pages/page1.py", "assets/image.png"],
        "APP_REQUIREMENTS": ["numpy", "pandas"],
    }
    with open(project_dir / "settings.yaml", "w") as f:
        yaml.dump(settings, f)

    # Create app.py
    with open(project_dir / "app.py", "w") as f:
        f.write("import streamlit as st\nst.write('Hello from app.py')")

    # Create pages/page1.py
    with open(project_dir / "pages" / "page1.py", "w") as f:
        f.write("import streamlit as st\nst.write('Hello from page1.py')")

    # Create assets/image.png (a dummy binary file)
    with open(project_dir / "assets" / "image.png", "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82")

    # 2. Mock load_all_versions
    mock_versions = (
        {"0.1.0": "css_url"}, "css_url",
        {"0.1.0": "js_url"}, "js_url",
        {"0.1.0": "pyodide_url"}, "pyodide_url"
    )
    mocker.patch('script2stlite.script2stlite.load_all_versions', return_value=mock_versions)

    # 3. Run the conversion
    s2s_convert(directory=str(project_dir))

    # 4. Check the output
    html_file = project_dir / "My_Test_App.html"
    assert html_file.is_file()

    html_content = html_file.read_text()

    # Check for stlite URLs
    assert "css_url" in html_content
    assert "js_url" in html_content

    # Check for app name
    assert "<title>My Test App</title>" in html_content

    # Check for requirements
    assert "'numpy', 'pandas'" in html_content

    # Check for entrypoint
    assert "entrypoint: \"app.py\"" in html_content

    # Check for main app code
    assert "st.write('Hello from app.py')" in html_content

    # Check for other files
    assert "pages/page1.py" in html_content
    assert "st.write('Hello from page1.py')" in html_content
    assert "assets/image.png" in html_content
    # Check for base64 encoded image data
    assert "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAACklEQVR4nGMAAQAABQABDQottAAAAABJRU5ErkJggg==" in html_content


def test_s2s_convert_shared_worker(tmp_path, mocker):
    # 1. Create a mock project
    project_dir = tmp_path / "my_project_shared"
    project_dir.mkdir()

    # Create settings.yaml with SHARED_WORKER: true
    settings = {
        "APP_NAME": "My Shared Worker App",
        "APP_ENTRYPOINT": "app.py",
        "SHARED_WORKER": True,
    }
    with open(project_dir / "settings.yaml", "w") as f:
        yaml.dump(settings, f)

    # Create app.py
    with open(project_dir / "app.py", "w") as f:
        f.write("import streamlit as st\nst.write('Hello from shared worker app')")

    # 2. Mock load_all_versions
    mock_versions = (
        {"0.1.0": "css_url"}, "css_url",
        {"0.1.0": "js_url"}, "js_url",
        {"0.1.0": "pyodide_url"}, "pyodide_url"
    )
    mocker.patch('script2stlite.script2stlite.load_all_versions', return_value=mock_versions)

    # 3. Run the conversion
    s2s_convert(directory=str(project_dir))

    # 4. Check the output
    html_file = project_dir / "My_Shared_Worker_App.html"
    assert html_file.is_file()

    html_content = html_file.read_text()
    assert "sharedWorker: true," in html_content
