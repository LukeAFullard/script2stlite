import pytest
import os
import yaml
from script2stlite.script2stlite import Script2StliteConverter

@pytest.fixture
def temp_project(tmp_path):
    """A fixture to create a temporary project directory with a basic setup."""
    project_dir = tmp_path / "test_project"
    project_dir.mkdir()

    # Create a dummy entrypoint file
    (project_dir / "app.py").write_text("import streamlit as st\nst.write('hello')")

    # Basic settings
    settings = {
        "APP_NAME": "Test App",
        "APP_ENTRYPOINT": "app.py",
        "APP_REQUIREMENTS": ["streamlit"],
        "APP_FILES": [],
    }

    with open(project_dir / "settings.yaml", "w") as f:
        yaml.dump(settings, f)

    return project_dir

def test_missing_entrypoint_in_settings(temp_project):
    """Test that a ValueError is raised if APP_ENTRYPOINT is missing from settings.yaml."""
    # Remove APP_ENTRYPOINT from settings
    with open(temp_project / "settings.yaml", "r") as f:
        settings = yaml.safe_load(f)
    del settings["APP_ENTRYPOINT"]
    with open(temp_project / "settings.yaml", "w") as f:
        yaml.dump(settings, f)

    with pytest.raises(ValueError, match="APP_ENTRYPOINT not defined in settings.yaml"):
        converter = Script2StliteConverter(directory=str(temp_project))
        # The error is raised during the call to create_html
        converter.convert()

def test_non_existent_entrypoint_file(temp_project):
    """Test that a FileNotFoundError is raised if the entrypoint file does not exist."""
    # Point to a non-existent file in settings
    with open(temp_project / "settings.yaml", "r") as f:
        settings = yaml.safe_load(f)
    settings["APP_ENTRYPOINT"] = "non_existent_app.py"
    with open(temp_project / "settings.yaml", "w") as f:
        yaml.dump(settings, f)

    converter = Script2StliteConverter(directory=str(temp_project))
    with pytest.raises(FileNotFoundError):
        converter.convert()

def test_non_existent_app_file(temp_project):
    """Test that a FileNotFoundError is raised if a file in APP_FILES does not exist."""
    # Add a non-existent file to APP_FILES
    with open(temp_project / "settings.yaml", "r") as f:
        settings = yaml.safe_load(f)
    settings["APP_FILES"] = ["non_existent_extra_file.py"]
    with open(temp_project / "settings.yaml", "w") as f:
        yaml.dump(settings, f)

    converter = Script2StliteConverter(directory=str(temp_project))
    with pytest.raises(ValueError, match="File non_existent_extra_file.py not found"):
        converter.convert()

def test_invalid_config_file_extension(temp_project):
    """Test that a ValueError is raised if the CONFIG file is not a .toml file."""
    # Create a dummy config file with a wrong extension
    (temp_project / "config.txt").write_text("some config")

    # Point to the invalid config file in settings
    with open(temp_project / "settings.yaml", "r") as f:
        settings = yaml.safe_load(f)
    settings["CONFIG"] = "config.txt"
    with open(temp_project / "settings.yaml", "w") as f:
        yaml.dump(settings, f)

    converter = Script2StliteConverter(directory=str(temp_project))
    with pytest.raises(ValueError, match="APP CONFIG must be a .toml file"):
        converter.convert()
