from .functions import load_all_versions,folder_exists,get_current_directory,create_directory,copy_file_from_subfolder,file_exists, load_yaml_from_file,create_html,write_text_file
import os
from pathlib import Path
from typing import Union, Optional, Dict

def s2s_prepare_folder(directory: Optional[str] = None) -> None:
    """
    Prepares a folder for a script2stlite project.

    This function performs the following actions:
    1. Determines the target directory: Uses the provided `directory` or defaults
       to the current working directory if `directory` is None.
    2. Validates directory: If a directory is provided, it checks if it exists.
    3. Creates 'pages' subdirectory: Ensures a 'pages' subdirectory exists within
       the target directory, creating it if necessary.
    4. Copies 'settings.yaml': If 'settings.yaml' does not already exist in the
       target directory, it copies a template 'settings.yaml' file into it.
       If 'settings.yaml' already exists, it prints a message and does not overwrite.

    Parameters
    ----------
    directory : Optional[str], optional
        The path to the directory where the project folder structure should be
        prepared. If None (default), the current working directory is used.

    Returns
    -------
    None

    Raises
    ------
    ValueError
        If the provided `directory` does not exist or if there's an issue
        copying the 'settings.yaml' template file.
    """
    #1. check if user provided a directory (or we will use current dir)
    if directory is not None: #directory is provided
        #check provided directory is valid
        if not folder_exists(directory): raise ValueError(f'''* {directory} does not exist on this system.''')
    else:  #nodirectory provided, use cd
        directory = get_current_directory()  
        print(f"* No user directory provided. Creating new s2stlite project in current directory ({directory}). \n")
    #2. check if pages folder exists, if not, create it
    create_directory(os.path.join(directory,'pages'))
    #3. create settings fileif it doesn't exist.
    if not file_exists(os.path.join(directory,'settings.yaml')):
        if not copy_file_from_subfolder(subfolder='templates',filename='settings.yaml',destination_dir=directory):
            raise ValueError(f'''* Issue copying settings template.''')
    else: print(f"* settings.yaml already exists in {directory}. NO NEW FILE CREATED. \n")        
    print(f"* Folder structure successfully created: {directory}. \n")


def s2s_convert(
    stlite_version: Optional[str] = None,
    pyodide_version: Optional[str] = None,
    directory: Optional[str] = None,
    packages: Optional[Dict[str, str]] = None
) -> None:
    """
    Converts a Streamlit application project into a single HTML file using stlite.

    This function performs the following steps:
    1. Determines the target directory (current working directory if not specified).
    2. Loads stlite, JavaScript, and Pyodide versions (uses latest if not specified).
    3. Reads 'settings.yaml' from the target directory.
    4. Updates settings with the chosen stlite, JS, and Pyodide versions.
    5. Ensures the main app entrypoint is not duplicated in the app files list.
    6. Validates that all files listed in settings exist.
    7. Generates the HTML content using `create_html`.
    8. Writes the generated HTML to a file named after the app_name in `settings.yaml`.

    Parameters
    ----------
    stlite_version : Optional[str], optional
        The specific version of stlite to use (e.g., "0.46.0"). If None (default),
        the latest available version is used. This also determines the default
        JavaScript version.
    pyodide_version : Optional[str], optional
        The specific version of Pyodide to use. If None (default), the latest
        available version compatible with the chosen stlite_version is used.
    directory : Optional[str], optional
        The root directory of the Streamlit application project. If None (default),
        the current working directory is used. This directory must contain
        'settings.yaml' and all application files.
    packages : Optional[Dict[str, str]], optional
        A dictionary mapping package names to specific versions, which can be used
        to override versions specified in requirements. If None (default),
        versions from requirements or latest available are used.

    Returns
    -------
    None

    Raises
    ------
    ValueError
        - If the specified `directory` does not exist.
        - If `stlite_version` is provided but not supported.
        - If 'settings.yaml' is not found in the directory.
        - If any file listed in 'settings.yaml' under 'APP_FILES' is not found.
    """
    #0. read/set directory
    if directory is not None: #directory is provided
        #check provided directory is valid
        if not folder_exists(directory): raise ValueError(f'''* {directory} does not exist on this system.''')
    else:  #nodirectory provided, use cd
        directory = get_current_directory()  
        print(f"* No user directory provided. Creating new s2stlite project in current directory ({directory}). \n")
    #1. load settings
    stylesheet_versions, stylesheet_top_version, js_versions, js_top_version, pyodide_versions, pyodide_top_version = load_all_versions()
    
    if stlite_version is None:
        stylesheet = stylesheet_top_version
        js = js_top_version
        pyodide = pyodide_top_version
    else:
        stylesheet = stylesheet_versions.get(str(stlite_version))
        js = js_versions.get(str(stlite_version))
        pyodide = pyodide_versions.get(str(pyodide_version))
    if (stylesheet is None) or (js is None):
        raise ValueError(f'''stlite_version ({stlite_version}) is not currently supported by script2stlite.
Valid versions include: {list(stylesheet_versions.keys())}''')

    #2. read settings yaml
    if not file_exists(os.path.join(directory,'settings.yaml')): raise ValueError(f"* No settings file found in {directory}. Please run s2s_prepare_folder().")
    settings = load_yaml_from_file(os.path.join(directory,'settings.yaml'))
    
    #Update css, js, pyodide versions into settings
    settings.update({"|STLITE_CSS|":stylesheet})
    settings.update({"|STLITE_JS|":js})
    settings.update({"|PYODIDE_VERSION|":pyodide})
    
    #if app entrypoint in app files, remove it! It will be used to replace |APP_HOME| in the html template. 
    if settings.get('APP_ENTRYPOINT') in settings.get('APP_FILES'): settings.get('APP_FILES').remove(settings.get('APP_ENTRYPOINT'))
    
    # 3. Check that all files exist.
    for file_j in settings.get('APP_FILES'):
        if not file_exists(os.path.join(directory,file_j)): raise ValueError(f"* File {file_j} not found in {directory}.")
        
    # 4. generate html
    html = create_html(directory,settings,packages=packages)
    write_text_file(os.path.join(directory,f'{settings.get("APP_NAME").replace(" ","_")}.html'), html)


class Script2StliteConverter:
    """
    A class to prepare and convert Streamlit applications to stlite.
    """
    def __init__(self, directory: Optional[str] = None):
        """
        Initializes the Script2StliteConverter.

        Parameters
        ----------
        directory : Optional[str], optional
            The target directory for operations. If None, defaults to the
            current working directory.
        """
        if directory is None:
            self.directory = get_current_directory()
            print(f"* No directory provided. Using current directory ({self.directory}). \n")
        else:
            if not folder_exists(directory):
                # Attempt to create it if it doesn't exist, or let s2s_prepare_folder handle it.
                # For now, let's ensure it exists or raise an error early.
                try:
                    create_directory(directory, exist_ok=True) # exist_ok=True means it won't fail if it's already there.
                    if not folder_exists(directory): # Check again after attempting to create
                         raise ValueError(f"* Provided directory {directory} does not exist and could not be created.")
                    print(f"* Using directory: {directory} \n")
                except Exception as e:
                    raise ValueError(f"* Error with provided directory {directory}: {e}")
            self.directory = directory

    def prepare_folder(self) -> None:
        """
        Prepares a folder for a script2stlite project using the directory
        specified during class initialization.
        """
        s2s_prepare_folder(directory=self.directory)

    def convert(
        self,
        stlite_version: Optional[str] = None,
        pyodide_version: Optional[str] = None,
        packages: Optional[Dict[str, str]] = None
    ) -> None:
        """
        Converts a Streamlit application project into a single HTML file using stlite,
        operating on the directory specified during class initialization.

        Parameters
        ----------
        stlite_version : Optional[str], optional
            The specific version of stlite to use. If None, latest is used.
        pyodide_version : Optional[str], optional
            The specific version of Pyodide to use. If None, latest is used.
        directory : Optional[str], optional
            The root directory of the Streamlit application project.
            If None, current working directory is used.
        packages : Optional[Dict[str, str]], optional
            A dictionary to override package versions.
        """
        s2s_convert(
            stlite_version=stlite_version,
            pyodide_version=pyodide_version,
            directory=self.directory,
            packages=packages
        )