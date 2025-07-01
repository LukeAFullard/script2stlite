import requests
import yaml
import tomli
import os
import shutil
from typing import Any, Dict, Tuple, Union
from pathlib import Path
import base64

stylesheet_url = r'https://raw.githubusercontent.com/LukeAFullard/script2stlite/refs/heads/main/stlite_versions/stylesheet.yaml'
js_url         = r'https://raw.githubusercontent.com/LukeAFullard/script2stlite/refs/heads/main/stlite_versions/js.yaml'
pyodide_url    = r'https://raw.githubusercontent.com/LukeAFullard/script2stlite/refs/heads/main/stlite_versions/pyodide.yaml'

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

def load_yaml_from_file(path: Union[str, os.PathLike]) -> Dict[str, Any]:
    """
    Load a YAML file from the local file system and return its contents as a Python dictionary.

    Parameters
    ----------
    path : Union[str, os.PathLike]
        The path to the local YAML file.

    Returns
    -------
    Dict[str, Any]
        The parsed contents of the YAML file.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    RuntimeError
        If the YAML content cannot be parsed.
    ValueError
        If the content is not a dictionary (mapping type).
    """
    if not os.path.isfile(path):
        raise FileNotFoundError(f"YAML file not found: {path}")

    try:
        with open(path, "r", encoding="utf-8") as f:
            data: Any = yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise RuntimeError(f"Failed to parse YAML content from {path}: {e}") from e

    if not isinstance(data, dict):
        raise ValueError("YAML content is not a dictionary (mapping type)")

    return data

def load_toml_from_file(path: Union[str, os.PathLike]) -> Dict[str, Any]:
    """
    Load a TOML file from the local file system and return its contents as a Python dictionary.

    Parameters
    ----------
    path : Union[str, os.PathLike]
        The path to the local TOML file.

    Returns
    -------
    Dict[str, Any]
        The parsed contents of the TOML file.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    RuntimeError
        If the TOML content cannot be parsed.
    ValueError
        If the content is not a dictionary (mapping type).
    """
    if not os.path.isfile(path):
        raise FileNotFoundError(f"TOML file not found: {path}")

    try:
        with open(path, "rb") as f:
            data: Any = tomli.load(f)
    except tomli.TOMLDecodeError as e:
        raise RuntimeError(f"Failed to parse TOML content from {path}: {e}") from e

    if not isinstance(data, dict):
        raise ValueError("TOML content is not a dictionary (mapping type)")

    return data

def flatten_dict(d: Dict[str, Any], parent_key: str = "", sep: str = ".") -> Dict[str, Any]:
    """
    Flatten a nested dictionary by joining keys with a separator.

    Parameters
    ----------
    d : Dict[str, Any]
        The nested dictionary to flatten.
    parent_key : str, optional
        The base key to prepend to each flattened key (used for recursion).
    sep : str, optional
        The separator to use when joining keys (default is ".").

    Returns
    -------
    Dict[str, Any]
        A flattened dictionary with dot-separated keys.
    """
    items: Dict[str, Any] = {}
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.update(flatten_dict(v, new_key, sep=sep))
        else:
            items[new_key] = v
    return items

def load_text_from_file(
    path: Union[str, os.PathLike],
    escape_text: bool = True,
    escape_string_map: Dict[str, str] = {
        "\\": "\\\\",
        "`": "\\`",
        "${": "\\${"
    }
    ) -> str:
    """
    Load a plain text file from the local file system and return its contents as a string.
    Optionally escape specified substrings in the text.

    Parameters
    ----------
    path : Union[str, os.PathLike]
        The path to the local text file.
    escape_text : bool, optional
        Whether to apply escaping to the text content (default is True).
    escape_string_map : Dict[str, str], optional
        A dictionary of substrings to escape and their replacements 
        (default is escaping for "\", "`", and "${").

    Returns
    -------
    str
        The contents of the text file as a string (escaped if specified).

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    RuntimeError
        If the file cannot be read.
    """
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Text file not found: {path}")

    try:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
    except Exception as e:
        raise RuntimeError(f"Failed to read text from {path}: {e}") from e

    if escape_text:
        for target, replacement in escape_string_map.items():
            text = text.replace(target, replacement)

    return text

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

def load_pyodide(url: str = pyodide_url, timeout: int = 10) -> Tuple[Dict[str, Any], Any]:
    """
    Load the Pyodide version dictionary from a YAML file at the specified URL,
    and return both the full dictionary and the value corresponding to the maximum version key.

    Parameters
    ----------
    url : str
        The URL pointing to the raw YAML Pyodide version file.
    timeout : int
        Timeout in seconds for the HTTP request.

    Returns
    -------
    Tuple[Dict[str, Any], Any]
        A tuple containing:
        - The full Pyodide version dictionary
        - The value corresponding to the maximum key
    """
    pyodide_versions: Dict[str, Any] = load_yaml_from_url(url=url, timeout=timeout)
    pyodide_top_version: Any = get_value_of_max_key(pyodide_versions)
    return pyodide_versions, pyodide_top_version

def load_all_versions(stylesheet_url: str = stylesheet_url, js_url: str = js_url, pyd_url: str = pyodide_url, timeout: int = 10
                      ) -> Tuple[Dict[str, Any], Any, Dict[str, Any], Any]:
    """
    Load stylesheet, Pyodide and JavaScript version dictionaries from their respective YAML files,
    and return dictionaries and their top-version values.

    Parameters
    ----------
    stylesheet_url : str
        The URL pointing to the raw YAML stylesheet version file.
    js_url : str
        The URL pointing to the raw YAML JavaScript version file.
    pyd_url : str
        The URL pointing to the raw YAML Pyodide version file.
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
        - Pyodide version dictionary
        - Pyodide top version value
    """
    stylesheet_versions, stylesheet_top_version = load_stylesheet(url=stylesheet_url, timeout=timeout)
    js_versions, js_top_version = load_js(url=js_url, timeout=timeout)
    pyodide_versions, pyodide_top_version = load_pyodide(url = pyd_url, timeout=timeout)
    return stylesheet_versions, stylesheet_top_version, js_versions, js_top_version, pyodide_versions, pyodide_top_version

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


def file_to_ou_base64_string(file_path: str) -> str:
    """
    Convert a binary file into a base64-encoded string suitable for use inside Ou("...").

    This is used to embed binary assets (e.g. images, PDFs, models) into stlite apps
    by including them as virtual filesystem files preloaded via stlite.embed().

    Parameters
    ----------
    file_path : str
        Path to the binary file.

    Returns
    -------
    str
        A base64-encoded string ready to be inserted inside Ou("...").
    """
    with open(file_path, "rb") as f:
        encoded: bytes = base64.b64encode(f.read())
        return encoded.decode("utf-8")
############################################################################### 
def write_text_file(filename: str, content: str) -> None:
    """
    Write text content to a file.

    Parameters
    ----------
    filename : str
        The name of the file to write to.
    content : str
        The text content to write to the file.

    Returns
    -------
    None
    """
    try:
        with open(filename, 'w') as f:
            f.write(content)
        print(f"Content successfully written to {filename}")
    except IOError:
        print(f"Error writing to {filename}")

def replace_text(input_text: str, replace_flag: str, replacement_text: str, add_stlite_punctuation: bool = True) -> str:
    """
    Replace a specific flag in the input text with replacement text.

    Optionally adds stlite-specific backticks and commas around the replacement text.

    Parameters
    ----------
    input_text : str
        The original text.
    replace_flag : str
        The substring to be replaced.
    replacement_text : str
        The text to insert in place of the replace_flag.
    add_stlite_punctuation : bool, optional
        If True (default), encloses the replacement_text with backticks and a trailing comma
        (e.g., "`replacement_text`,"). Otherwise, inserts replacement_text as is.

    Returns
    -------
    str
        The text with replacements made.
    """
    if add_stlite_punctuation:
        return input_text.replace(replace_flag, f"`{replacement_text}`,")
    else:
        return input_text.replace(replace_flag, replacement_text)

def create_html(directory: str, app_settings: Dict[str, Any], packages: Union[Dict[str, str], None] = None) -> str:
    """
    Generates an HTML file content for an stlite application.

    This function takes directory, application settings, and optional package information
    to populate an HTML template. It replaces placeholders in the template with
    actual values like CSS links, JS links, Pyodide version, application name,
    requirements, entrypoint, main application script content, and other files.

    Parameters
    ----------
    directory : str
        The root directory of the application where 'settings.yaml' and other app files are located.
    app_settings : Dict[str, Any]
        A dictionary containing application settings, typically loaded from 'settings.yaml'.
        Expected keys include:
        - '|STLITE_CSS|': URL for the stlite CSS file.
        - '|STLITE_JS|': URL for the stlite JavaScript file.
        - '|PYODIDE_VERSION|': Version of Pyodide to use.
        - '|APP_NAME|': Name of the application.
        - '|APP_REQUIREMENTS|': A list of Python package requirements.
        - '|APP_ENTRYPOINT|': The main Python script for the application (e.g., 'streamlit_app.py').
        - '|APP_FILES|': A list of other files to include in the stlite bundle.
    packages : Union[Dict[str, str], None], optional
        A dictionary mapping package names to specific versions. If None (default),
        the latest versions specified in requirements are used. This allows for
        pinning package versions if needed.

    Returns
    -------
    str
        The generated HTML content as a string.

    Raises
    ------
    ValueError
        If essential settings like CSS, JS, Pyodide version, or app entrypoint are missing,
        or if the app entrypoint is not a '.py' file.
    FileNotFoundError
        If the HTML template or specified application files are not found.
    """
    if packages is None:
        packages = {}
    #1 load html file
    html = load_text_from_subfolder(subfolder='templates', filename='html_template.txt')
    
    #2) replace css
    if app_settings.get('|STLITE_CSS|') is not None:
        html = replace_text(html, '|STLITE_CSS|', app_settings.get('|STLITE_CSS|'), add_stlite_punctuation = False)
    else: raise ValueError("No stlite css version defined.")
        
    
    #3) replace JS
    if app_settings.get('|STLITE_JS|') is not None:
        html = replace_text(html, '|STLITE_JS|', app_settings.get('|STLITE_JS|'), add_stlite_punctuation = False)
    else: raise ValueError("No stlite JS version defined.")
    
    #4) replace Pyodide
    if app_settings.get('|PYODIDE_VERSION|') is not None:
        html = replace_text(html, '|PYODIDE_VERSION|', app_settings.get('|PYODIDE_VERSION|'), add_stlite_punctuation = False)
    else: raise ValueError("No stlite Pyodide version defined.")
    
    #5) replace '|APP_NAME|'
    if app_settings.get('APP_NAME') is not None:
        html = replace_text(html, '|APP_NAME|', app_settings.get('APP_NAME'), add_stlite_punctuation = False)
    else:
        html = replace_text(html, '|APP_NAME|', '', add_stlite_punctuation = False)
        
    #6) replace '|APP_REQUIREMENTS|'
    if app_settings.get('APP_REQUIREMENTS') is not None:
        package_requirements = [packages.get(x,x) for x in app_settings.get('APP_REQUIREMENTS')] # note, the dictionary packages allows us to define specific package versions. Not necessary, but may be useful one day.
        package_requirements = str(package_requirements)
        html = replace_text(html, '|APP_REQUIREMENTS|', package_requirements, add_stlite_punctuation = False)
    else:
        html = replace_text(html, '|APP_REQUIREMENTS|', '[]', add_stlite_punctuation = False)    
        
    #7) replace '|APP_ENTRYPOINT|' 
    if app_settings.get('APP_ENTRYPOINT') is not None:
        html = replace_text(html, '|APP_ENTRYPOINT|', app_settings.get('APP_ENTRYPOINT'), add_stlite_punctuation = False)
    else:
        html = replace_text(html, '|APP_ENTRYPOINT|', '', add_stlite_punctuation = False)
    
    #8) replace '|APP_HOME|'
    #check is a py file
    if not Path(os.path.join(directory,app_settings.get('APP_ENTRYPOINT'))).suffix == '.py': raise ValueError(f"APP ENTRYPOINT must be a .py file: {os.path.join(directory,app_settings.get('APP_ENTRYPOINT'))}")
    html = replace_text(html, '|APP_HOME|', load_text_from_file(os.path.join(directory,app_settings.get('APP_ENTRYPOINT'))), add_stlite_punctuation = False)   
    
    #9) replace |CONFIG|
    #check if it exists
    if not file_exists(os.path.join(directory,app_settings.get('CONFIG'))): 
        print(f"** No config file found - setting config blank")
        config = "{}"
    else:
        #ensure is a toml file
        if not Path(os.path.join(directory,app_settings.get('CONFIG'))).suffix == '.toml': raise ValueError(f"APP CONFIG must be a .toml file: {os.path.join(directory,app_settings.get('CONFIG'))}")
        else:
            config = flatten_dict(load_toml_from_file(os.path.join(directory,app_settings.get('CONFIG'))))
    config = str(config).replace('False','false').replace('True','true')        
    html = replace_text(html, '|CONFIG|', config, add_stlite_punctuation = False)           
    
    
    #10) replace '|APP_FILES|' 
    app_files = ''
    if app_settings.get('APP_FILES') is not None:
        for file_j in app_settings.get('APP_FILES'):
            if not Path(os.path.join(directory,file_j)).suffix == '.py': 
                binary_text = file_to_ou_base64_string(os.path.join(directory,file_j))
                app_files += f'"{file_j}":' + ' Ou("' + binary_text + '"),'
            else:
                app_files += f'"{file_j}":' + '`' + load_text_from_file(os.path.join(directory,file_j)) + '`,'
    html = replace_text(html, '|APP_FILES|', app_files, add_stlite_punctuation = False)   
    
    #10) return html
    return html
        
    
    
