import pytest
import os
import requests
import yaml
import tomli
from unittest.mock import MagicMock, patch, mock_open
from script2stlite.functions import (
    get_value_of_max_key,
    load_yaml_from_url,
    load_yaml_from_file,
    load_toml_from_file,
    parse_requirements,
    load_text_from_file,
    create_directory,
    copy_file_from_subfolder,
    load_text_from_subfolder,
    create_html,
    get_current_directory,
    write_text_file
)

def test_get_value_of_max_key_empty():
    """Test get_value_of_max_key raises ValueError for empty dict."""
    with pytest.raises(ValueError, match="Cannot get max key from an empty dictionary"):
        get_value_of_max_key({})

def test_get_value_of_max_key_incomparable():
    """Test get_value_of_max_key raises TypeError for incomparable keys."""
    with pytest.raises(TypeError, match="Dictionary keys are not comparable"):
        get_value_of_max_key({1: 'a', '2': 'b'})

def test_load_yaml_from_url_errors():
    """Test load_yaml_from_url error handling."""
    url = "http://example.com/file.yaml"

    # Network error
    with patch('requests.get', side_effect=requests.exceptions.RequestException("Network Error")):
        with pytest.raises(RuntimeError, match="Failed to fetch YAML file"):
            load_yaml_from_url(url)

    # Parse error
    with patch('requests.get') as mock_get:
        mock_get.return_value.text = ": invalid yaml"
        mock_get.return_value.raise_for_status = MagicMock()
        with pytest.raises(RuntimeError, match="Failed to parse YAML content"):
            load_yaml_from_url(url)

    # Not a dict
    with patch('requests.get') as mock_get:
        mock_get.return_value.text = "- list item"
        mock_get.return_value.raise_for_status = MagicMock()
        with pytest.raises(ValueError, match="YAML content is not a dictionary"):
            load_yaml_from_url(url)

def test_load_yaml_from_file_errors(tmp_path):
    """Test load_yaml_from_file error handling."""
    f = tmp_path / "bad.yaml"

    # Parse error
    f.write_text(": invalid yaml", encoding="utf-8")
    with pytest.raises(RuntimeError, match="Failed to parse YAML content"):
        load_yaml_from_file(f)

    # Not a dict
    f.write_text("- list item", encoding="utf-8")
    with pytest.raises(ValueError, match="YAML content is not a dictionary"):
        load_yaml_from_file(f)

def test_load_toml_from_file_errors(tmp_path):
    """Test load_toml_from_file error handling."""
    f = tmp_path / "bad.toml"

    # Parse error
    f.write_text("invalid toml =", encoding="utf-8")
    with pytest.raises(RuntimeError, match="Failed to parse TOML content"):
        load_toml_from_file(f)

    # Not a dict? TOML at top level is always a table/dict, so hard to trigger "not dict" unless tomli returns something else?
    # tomli.load returns a dict. So maybe that check is defensive.
    # We can mock tomli.load to return a list to test it.
    with patch('tomli.load', return_value=[]):
        with pytest.raises(ValueError, match="TOML content is not a dictionary"):
            load_toml_from_file(f)

def test_parse_requirements_error(tmp_path):
    """Test parse_requirements handles exceptions."""
    f = tmp_path / "reqs.txt"
    f.touch()

    # Mock open to raise exception
    with patch("builtins.open", side_effect=Exception("Read Error")):
         # Should print warning and return empty list
         reqs = parse_requirements(f)
         assert reqs == []

def test_parse_requirements_happy_path(tmp_path):
    """Test parse_requirements reads file correctly."""
    f = tmp_path / "reqs.txt"
    f.write_text("numpy\npandas>=1.0\n# comment\n", encoding="utf-8")

    reqs = parse_requirements(f)
    assert "numpy" in reqs
    assert "pandas>=1.0" in reqs
    assert len(reqs) == 2

def test_parse_requirements_missing_file():
    """Test parse_requirements returns empty list if file does not exist."""
    reqs = parse_requirements("non_existent_requirements.txt")
    assert reqs == []

def test_load_text_from_file_error(tmp_path):
    """Test load_text_from_file raises RuntimeError on read error."""
    f = tmp_path / "text.txt"
    f.touch()

    with patch("builtins.open", side_effect=Exception("Read Error")):
        with pytest.raises(RuntimeError, match="Failed to read text"):
            load_text_from_file(f)

def test_create_directory_error():
    """Test create_directory handles OSError."""
    with patch("os.makedirs", side_effect=OSError("Permission denied")):
        assert create_directory("some/path") is False

def test_copy_file_from_subfolder_errors():
    """Test copy_file_from_subfolder error paths."""

    # Source file not found
    with patch("os.path.isfile", return_value=False):
        assert copy_file_from_subfolder("sub", "file", "dest") is False

    # Destination dir not exists
    # We need isfile to be true for source file, but folder_exists to be false for dest
    with patch("os.path.isfile", return_value=True), \
         patch("script2stlite.functions.folder_exists", return_value=False):
        assert copy_file_from_subfolder("sub", "file", "dest") is False

    # Generic exception
    with patch("os.path.isfile", side_effect=Exception("Boom")):
        assert copy_file_from_subfolder("sub", "file", "dest") is False

def test_load_text_from_subfolder_error():
    """Test load_text_from_subfolder raises FileNotFoundError."""
    with patch("os.path.isfile", return_value=False):
        with pytest.raises(FileNotFoundError, match="Text file not found"):
            load_text_from_subfolder("sub", "missing.txt")

def test_create_html_errors(tmp_path):
    """Test create_html error handling."""
    directory = str(tmp_path)

    # Missing CSS
    with pytest.raises(ValueError, match="No stlite css version defined"):
        create_html(directory, {})

    # Missing JS
    with pytest.raises(ValueError, match="No stlite JS version defined"):
        create_html(directory, {'|STLITE_CSS|': 'css'})

    # Missing Pyodide
    with pytest.raises(ValueError, match="No stlite Pyodide version defined"):
        create_html(directory, {'|STLITE_CSS|': 'css', '|STLITE_JS|': 'js'})

    # Entrypoint not .py
    settings = {
        '|STLITE_CSS|': 'css', '|STLITE_JS|': 'js', '|PYODIDE_VERSION|': 'pyodide',
        'APP_ENTRYPOINT': 'app.txt'
    }
    with pytest.raises(ValueError, match="APP ENTRYPOINT must be a .py file"):
        create_html(directory, settings)

    # Config not .toml
    settings['APP_ENTRYPOINT'] = 'app.py'
    settings['CONFIG'] = 'config.json'
    (tmp_path / "config.json").touch()

    # We need app.py to exist for create_html to proceed to config check?
    # Actually create_html reads app.py content. So we need to mock load_text_from_file or create the file.
    (tmp_path / "app.py").touch()

    # We also need html_template.txt to be loadable via load_text_from_subfolder
    with patch("script2stlite.functions.load_text_from_subfolder", return_value="TEMPLATE"):
         with pytest.raises(ValueError, match="APP CONFIG must be a .toml file"):
             create_html(directory, settings)

def test_get_current_directory():
    """Test get_current_directory returns current directory."""
    assert get_current_directory() == os.getcwd()

def test_write_text_file_error(tmp_path):
    """Test write_text_file handles IOError."""
    # We can mock open to raise IOError
    with patch("builtins.open", side_effect=IOError("Write error")):
        # Should catch and print error
        write_text_file("some_file.txt", "content")

def test_create_html_with_valid_config(tmp_path):
    """Test create_html correctly processes a valid toml config."""
    directory = str(tmp_path)
    (tmp_path / "app.py").write_text("print('hello')", encoding="utf-8")
    (tmp_path / "config.toml").write_text('[theme]\nprimaryColor="#F63366"', encoding="utf-8")

    settings = {
        '|STLITE_CSS|': 'css',
        '|STLITE_JS|': 'js',
        '|PYODIDE_VERSION|': 'pyodide',
        'APP_ENTRYPOINT': 'app.py',
        'CONFIG': 'config.toml',
        'APP_NAME': 'TestApp'
    }

    with patch("script2stlite.functions.load_text_from_subfolder", return_value="|CONFIG|"):
        html = create_html(directory, settings)
        # Check if config was processed and flattened
        assert "primaryColor" in html
        assert "#F63366" in html
