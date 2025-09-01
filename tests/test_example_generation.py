import pytest
from pathlib import Path
import shutil
import yaml
from script2stlite.script2stlite import Script2StliteConverter

def test_bitcoin_app_generation(tmp_path):
    # 1. Define paths
    example_dir_src = Path("example/Example_2_bitcoin_price_app")
    project_dir_tmp = tmp_path / "bitcoin_app"
    output_dir = Path("tests")
    output_filename = "generated_bitcoin_app.html"
    output_html_path = output_dir / output_filename

    # 2. Copy example project to a temporary directory
    shutil.copytree(example_dir_src, project_dir_tmp)

    # 3. Run the conversion in the temporary directory
    converter = Script2StliteConverter(directory=str(project_dir_tmp))
    converter.convert()

    # 4. Locate the generated HTML file in the temporary directory
    with open(project_dir_tmp / "settings.yaml", "r") as f:
        settings = yaml.safe_load(f)
    app_name = settings["APP_NAME"]
    generated_filename = app_name.replace(" ", "_") + ".html"
    generated_html_path = project_dir_tmp / generated_filename

    # 5. Check that the HTML file was generated
    assert generated_html_path.is_file(), f"Generated HTML file not found at {generated_html_path}"

    # 6. Copy the generated HTML file to the tests folder
    output_dir.mkdir(exist_ok=True)
    shutil.copy(generated_html_path, output_html_path)

    # 7. Final check in the tests directory
    assert output_html_path.is_file(), f"HTML file not found in tests directory at {output_html_path}"
