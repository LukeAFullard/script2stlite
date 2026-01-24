import pytest
import os
from unittest.mock import MagicMock, patch
from script2stlite.script2stlite import s2s_prepare_folder, s2s_convert, Script2StliteConverter, _s2s_convert_core

def test_s2s_prepare_folder_invalid_directory():
    """Test s2s_prepare_folder raises ValueError if directory does not exist."""
    with patch('script2stlite.script2stlite.folder_exists', return_value=False):
        with pytest.raises(ValueError, match="does not exist on this system"):
            s2s_prepare_folder(directory="nonexistent_dir")

def test_s2s_prepare_folder_copy_settings_fails():
    """Test s2s_prepare_folder raises ValueError if copying settings fails."""
    with patch('script2stlite.script2stlite.folder_exists', return_value=True), \
         patch('script2stlite.script2stlite.create_directory'), \
         patch('script2stlite.script2stlite.file_exists', return_value=False), \
         patch('script2stlite.script2stlite.copy_file_from_subfolder', return_value=False):

        with pytest.raises(ValueError, match="Issue copying settings template"):
            s2s_prepare_folder(directory="some_dir")

def test_s2s_prepare_folder_no_directory():
    """Test s2s_prepare_folder works when directory is None (uses current directory)."""
    with patch('script2stlite.script2stlite.get_current_directory', return_value='/tmp/current'), \
         patch('script2stlite.script2stlite.create_directory') as mock_create, \
         patch('script2stlite.script2stlite.file_exists', return_value=True):

         s2s_prepare_folder(directory=None)
         mock_create.assert_called_with('/tmp/current/pages')

def test_s2s_convert_core_invalid_stlite_version():
    """Test _s2s_convert_core raises ValueError if stlite_version is invalid."""
    settings = {}
    directory = "some_dir"

    # Mock load_all_versions to return specific versions
    # versions structure: stylesheet_versions, stylesheet_top_version, js_versions, js_top_version, pyodide_versions, pyodide_top_version
    with patch('script2stlite.script2stlite.load_all_versions') as mock_load:
        mock_load.return_value = ({'0.82.0': 'css_url'}, 'css_url', {'0.82.0': 'js_url'}, 'js_url', {'0.27.4': 'py_url'}, 'py_url')

        with pytest.raises(ValueError, match="stlite_version.*is not currently supported"):
            _s2s_convert_core(settings, directory, stlite_version="99.99.99")

def test_s2s_convert_core_no_app_files(tmp_path):
    """Test _s2s_convert_core works when APP_FILES is None in settings."""
    # This covers:
    # 1. settings.get('APP_FILES') is None -> app_files = []
    # 2. discover_all_files returns nothing -> app_files remains []
    # 3. settings.get('APP_ENTRYPOINT') not in app_files (if entrypoint is separate)

    directory = str(tmp_path)
    # Explicitly set APP_FILES to None to trigger "if app_files is None" branch
    settings = {'APP_NAME': 'Test', 'APP_ENTRYPOINT': 'app.py', 'APP_FILES': None}

    with patch('script2stlite.script2stlite.load_all_versions') as mock_load, \
         patch('script2stlite.script2stlite.discover_all_files', return_value=[]), \
         patch('script2stlite.script2stlite.file_exists', return_value=True), \
         patch('script2stlite.script2stlite.create_html', return_value="<html></html>"), \
         patch('script2stlite.script2stlite.write_text_file'):

        mock_load.return_value = ({'0.82.0': 'css_url'}, 'css_url', {'0.82.0': 'js_url'}, 'js_url', {'0.27.4': 'py_url'}, 'py_url')

        _s2s_convert_core(settings, directory)
        assert settings['APP_FILES'] == []

def test_s2s_convert_invalid_directory():
    """Test s2s_convert raises ValueError if directory does not exist."""
    with patch('script2stlite.script2stlite.folder_exists', return_value=False):
        with pytest.raises(ValueError, match="does not exist on this system"):
            s2s_convert(directory="nonexistent_dir")

def test_s2s_convert_no_directory():
    """Test s2s_convert uses current directory if none provided."""
    with patch('script2stlite.script2stlite.get_current_directory', return_value='/tmp/current'), \
         patch('script2stlite.script2stlite.file_exists', return_value=True), \
         patch('script2stlite.script2stlite.load_yaml_from_file', return_value={}), \
         patch('script2stlite.script2stlite._s2s_convert_core') as mock_core:

         s2s_convert(directory=None)
         mock_core.assert_called()
         assert mock_core.call_args[1]['directory'] == '/tmp/current'

def test_converter_init_create_directory_fails():
    """Test Script2StliteConverter raises ValueError if directory creation fails."""
    with patch('script2stlite.script2stlite.folder_exists', side_effect=[False, False]), \
         patch('script2stlite.script2stlite.create_directory', side_effect=OSError("Permission denied")):

         with pytest.raises(ValueError, match="Error with provided directory"):
             Script2StliteConverter(directory="protected_dir")

def test_converter_init_directory_creation_false_positive():
    """Test Script2StliteConverter raises ValueError if directory creation seems successful but folder still doesn't exist."""
    with patch('script2stlite.script2stlite.folder_exists', side_effect=[False, False]), \
         patch('script2stlite.script2stlite.create_directory'):

         with pytest.raises(ValueError, match="does not exist and could not be created"):
             Script2StliteConverter(directory="ghost_dir")

def test_converter_init_no_directory():
    """Test Script2StliteConverter uses current directory if none provided."""
    with patch('script2stlite.script2stlite.get_current_directory', return_value='/tmp/current'):
        converter = Script2StliteConverter(directory=None)
        assert converter.directory == '/tmp/current'

def test_converter_init_create_directory_success():
    """Test Script2StliteConverter creates directory if it doesn't exist."""
    with patch('script2stlite.script2stlite.folder_exists', side_effect=[False, True]), \
         patch('script2stlite.script2stlite.create_directory') as mock_create:

         converter = Script2StliteConverter(directory="new_dir")
         mock_create.assert_called_with("new_dir", exist_ok=True)
         assert converter.directory == "new_dir"

def test_converter_prepare_folder():
    """Test Script2StliteConverter.prepare_folder calls s2s_prepare_folder."""
    with patch('script2stlite.script2stlite.folder_exists', return_value=True), \
         patch('script2stlite.script2stlite.s2s_prepare_folder') as mock_prep:

         converter = Script2StliteConverter(directory="some_dir")
         converter.prepare_folder()
         mock_prep.assert_called_with(directory="some_dir")

def test_convert_from_entrypoint_missing_entrypoint(tmp_path):
    """Test convert_from_entrypoint raises ValueError if entrypoint file is missing."""
    converter = Script2StliteConverter(directory=str(tmp_path))

    with pytest.raises(ValueError, match="Entrypoint file.*not found"):
        converter.convert_from_entrypoint(app_name="Test App", entrypoint="missing.py")
