import requests
import yaml
import os
import shutil
from typing import Any, Dict, Tuple, Union
from pathlib import Path

stylesheet_url = r'https://raw.githubusercontent.com/LukeAFullard/script2stlite/refs/heads/main/stlite_versions/stylesheet.yaml'
js_url = r'https://raw.githubusercontent.com/LukeAFullard/script2stlite/refs/heads/main/stlite_versions/js.yaml'


def get_value_of_max_key(data: Dict[Any, Any]) -> Any:
    """
    Return the value corresponding to the maximum key in the dictionary.

    Parameters
    ----------
    data : Dict[Any, Any]
        A dictionary with comparable keys (e.g., int, float, str).

    Returns
    -------
    Any
        The value associated with the maximum key.

    Raises
    ------
    ValueError
        If the dictionary is empty.
    TypeError
        If the keys are not comparable.
    """
    if not data:
        raise ValueError("Cannot get max key from an empty dictionary.")

    try:
        max_key = max(data)
    except TypeError as e:
        raise TypeError("Dictionary keys are not comparable.") from e

    return data[max_key]

def load_yaml_from_url(url: str, timeout: int = 10) -> Dict[str, Any]:
    """
    Load a YAML file from a remote URL and return its contents as a Python dictionary.

    Parameters
    ----------
    url : str
        The URL pointing to the raw YAML file (e.g., a GitHub raw content link).
    timeout : int, optional
        Timeout in seconds for the HTTP request (default is 10).

    Returns
    -------
    Dict[str, Any]
        The parsed contents of the YAML file.

    Raises
    ------
    RuntimeError
        If there is a network-related error or YAML parsing failure.
    ValueError
        If the YAML content is empty or not a dictionary.
    """
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to fetch YAML file from {url}: {e}") from e

    try:
        data: Any = yaml.safe_load(response.text)
    except yaml.YAMLError as e:
        raise RuntimeError(f"Failed to parse YAML content from {url}: {e}") from e

    if not isinstance(data, dict):
        raise ValueError("YAML content is not a dictionary (mapping type)")

    return data


def load_stylesheet(url: str = stylesheet_url, timeout: int = 10) -> Tuple[Dict[str, Any], Any]:
    """
    Load the stylesheet version dictionary from a YAML file at the specified URL,
    and return both the full dictionary and the value corresponding to the maximum version key.

    Parameters
    ----------
    url : str
        The URL pointing to the raw YAML stylesheet version file.
    timeout : int
        Timeout in seconds for the HTTP request.

    Returns
    -------
    Tuple[Dict[str, Any], Any]
        A tuple containing:
        - The full stylesheet version dictionary
        - The value corresponding to the maximum key
    """
    stylesheet_versions: Dict[str, Any] = load_yaml_from_url(url=url, timeout=timeout)
    stylesheet_top_version: Any = get_value_of_max_key(stylesheet_versions)
    return stylesheet_versions, stylesheet_top_version


def load_js(url: str = js_url, timeout: int = 10) -> Tuple[Dict[str, Any], Any]:
    """
    Load the JavaScript version dictionary from a YAML file at the specified URL,
    and return both the full dictionary and the value corresponding to the maximum version key.

    Parameters
    ----------
    url : str
        The URL pointing to the raw YAML JavaScript version file.
    timeout : int
        Timeout in seconds for the HTTP request.

    Returns
    -------
    Tuple[Dict[str, Any], Any]
        A tuple containing:
        - The full JavaScript version dictionary
        - The value corresponding to the maximum key
    """
    js_versions: Dict[str, Any] = load_yaml_from_url(url=url, timeout=timeout)
    js_top_version: Any = get_value_of_max_key(js_versions)
    return js_versions, js_top_version

def load_all_versions(stylesheet_url: str = stylesheet_url, js_url: str = js_url, timeout: int = 10
                      ) -> Tuple[Dict[str, Any], Any, Dict[str, Any], Any]:
    """
    Load both stylesheet and JavaScript version dictionaries from their respective YAML files,
    and return both dictionaries and their top-version values.

    Parameters
    ----------
    stylesheet_url : str
        The URL pointing to the raw YAML stylesheet version file.
    js_url : str
        The URL pointing to the raw YAML JavaScript version file.
    timeout : int
        Timeout in seconds for the HTTP requests.

    Returns
    -------
    Tuple[Dict[str, Any], Any, Dict[str, Any], Any]
        A tuple containing:
        - Stylesheet version dictionary
        - Stylesheet top version value
        - JavaScript version dictionary
        - JavaScript top version value
    """
    stylesheet_versions, stylesheet_top_version = load_stylesheet(url=stylesheet_url, timeout=timeout)
    js_versions, js_top_version = load_js(url=js_url, timeout=timeout)
    return stylesheet_versions, stylesheet_top_version, js_versions, js_top_version

###############################################################################
def folder_exists(path: Union[str, bytes, os.PathLike]) -> bool:
    """
    Check if a folder (directory) exists at the specified path.

    Parameters
    ----------
    path : Union[str, bytes, os.PathLike]
        The path to the folder to check.

    Returns
    -------
    bool
        True if the folder exists and is a directory, False otherwise.
    """
    return os.path.isdir(path)


def file_exists(path: Union[str, bytes, os.PathLike]) -> bool:
    """
    Check if a file exists at the specified path.

    Parameters
    ----------
    path : Union[str, bytes, os.PathLike]
        The path to the file to check.

    Returns
    -------
    bool
        True if the file exists and is a file, False otherwise.
    """
    return os.path.isfile(path)
###############################################################################
def get_current_directory() -> str:
    """
    Return the current working directory.

    Returns
    -------
    str
        The absolute path to the current working directory.
    """
    return os.getcwd()

def create_directory(path: Union[str, bytes, os.PathLike], exist_ok: bool = True) -> bool:
    """
    Create a directory at the specified path, including any necessary parent directories.

    Parameters
    ----------
    path : Union[str, bytes, os.PathLike]
        The path of the directory to create.
    exist_ok : bool, optional
        If True, do not raise an error if the directory already exists (default is True).

    Returns
    -------
    bool
        True if the directory exists or was created successfully.
        False if directory creation failed.
    """
    try:
        os.makedirs(path, exist_ok=exist_ok)
        return True
    except OSError as e:
        print(f"Error creating directory '{path}': {e}")
        return False
###############################################################################    
def copy_file_from_subfolder(
    subfolder: Union[str, os.PathLike],
    filename: str,
    destination_dir: Union[str, os.PathLike]
) -> bool:
    """
    Copy a file from a subfolder (relative to this script) to a user-defined directory.

    Parameters
    ----------
    subfolder : Union[str, os.PathLike]
        The name or path of the subfolder relative to the script.
    filename : str
        The name of the file to copy (e.g., 'asettings.yaml').
    destination_dir : Union[str, os.PathLike]
        The directory where the file should be copied to.

    Returns
    -------
    bool
        True if the file was copied successfully, False if an error occurred.
    """
    try:
        # Resolve the absolute path to the source file
        script_dir = os.path.dirname(os.path.abspath(__file__))
        source_file = os.path.join(script_dir, subfolder, filename)

        if not os.path.isfile(source_file):
            raise FileNotFoundError(f"Source file not found: {source_file}")

        # Ensure destination directory exists
        path_exists = folder_exists(destination_dir)
        
        if path_exists:
            # Define the destination path
            destination_file = os.path.join(destination_dir, filename)
    
            # Copy the file
            shutil.copy2(source_file, destination_file)
        else:
            print(f"Destination folder, {destination_dir} does not exist.")
            return False

        return True
    except Exception as e:
        print(f"Error copying file: {e}")
        return False
    
def load_text_from_subfolder(
    subfolder: Union[str, os.PathLike],
    filename: str,
    encoding: str = "utf-8"
) -> str:
    """
    Load a text file from a subfolder (relative to this script) and return its contents as a string.

    Parameters
    ----------
    subfolder : Union[str, os.PathLike]
        The name or relative path of the subfolder where the file is located.
    filename : str
        The name of the text file to load.
    encoding : str, optional
        The file encoding to use (default is 'utf-8').

    Returns
    -------
    str
        The contents of the text file.

    Raises
    ------
    FileNotFoundError
        If the text file does not exist.
    IOError
        If there is an error reading the file.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, subfolder, filename)

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Text file not found: {file_path}")

    with open(file_path, "r", encoding=encoding) as f:
        content = f.read()

    return content    
###############################################################################        