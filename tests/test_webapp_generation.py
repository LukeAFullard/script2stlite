import pytest
from pathlib import Path
import yaml
from script2stlite.script2stlite import s2s_convert
import shutil

def test_simple_app_rendering_generation(tmp_path):
    # 1. Create a mock project
    project_dir = tmp_path / "my_project"
    project_dir.mkdir()
    (project_dir / "pages").mkdir()

    # Create settings.yaml
    settings = {
        "APP_NAME": "My Test App",
        "APP_ENTRYPOINT": "app.py",
        "APP_FILES": [],
        "APP_REQUIREMENTS": ["streamlit"],
        "CONFIG": False
    }
    with open(project_dir / "settings.yaml", "w") as f:
        yaml.dump(settings, f)

    # Create app.py
    with open(project_dir / "app.py", "w") as f:
        f.write("""
import streamlit as st
st.write('Hello, Streamlit!')
""")

    # 2. Run the conversion
    s2s_convert(directory=str(project_dir))

    # 3. Check that the HTML file is generated
    html_file = project_dir / "My_Test_App.html"
    assert html_file.is_file()

    # 4. Save the HTML file to the tests folder
    shutil.copy(html_file, "tests/generated_test_app.html")
