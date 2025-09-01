import pytest
from pathlib import Path
import yaml
from script2stlite.script2stlite import s2s_convert
import shutil
import os
from script2stlite.functions import load_yaml_from_file

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


EXAMPLE_DIRS = [
    "Example_0_simple_app",
    "Example_1_multi_page_image_editor",
    "Example_2_bitcoin_price_app",
    "Example_3_streamlit_chect_sheet",
    "Example_4_echarts_demo",
    "Example_5_PixelHue",
    "Example_6_vizzu",
]

@pytest.mark.parametrize("example_dir_name", EXAMPLE_DIRS)
def test_generate_example_apps(example_dir_name, tmp_path):
    example_dir = os.path.join("example", example_dir_name)

    # Copy example dir to a temp dir
    temp_example_dir = tmp_path / example_dir_name
    shutil.copytree(example_dir, temp_example_dir)

    # Run the conversion on the temp dir
    s2s_convert(directory=str(temp_example_dir))

    # Find the generated HTML file in the temp dir
    settings = load_yaml_from_file(os.path.join(temp_example_dir, "settings.yaml"))
    app_name = settings.get("APP_NAME")
    html_file_name = f"{app_name.replace(' ', '_')}.html"
    generated_html_path = os.path.join(temp_example_dir, html_file_name)

    assert os.path.exists(generated_html_path)

    # Save the HTML file to the tests folder
    dest_file_name = f"generated_{example_dir_name}.html"
    shutil.copy(generated_html_path, os.path.join("tests", dest_file_name))
