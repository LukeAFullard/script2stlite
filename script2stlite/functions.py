import requests
import yaml
import os
from typing import Any, Dict, Tuple, Union
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
