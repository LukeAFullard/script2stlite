from .functions import load_all_versions,folder_exists,get_current_directory,create_directory,copy_file_from_subfolder,file_exists, load_yaml_from_file,create_html,write_text_file, parse_requirements
from .discovery import discover_all_files
import os
from pathlib import Path
from typing import Union, Optional, Dict, Any

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


def _s2s_convert_core(
    settings: Dict[str, Any],
    directory: str,
    stlite_version: Optional[str] = None,
    pyodide_version: Optional[str] = None,
    packages: Optional[Dict[str, str]] = None,
    ignore_dirs: Optional[list] = None,
    ignore_files: Optional[list] = None
) -> None:
    """
    Core logic for converting a Streamlit application to stlite HTML.

    Parameters
    ----------
    settings : Dict[str, Any]
        The application settings.
    directory : str
        The root directory of the application.
    stlite_version : Optional[str]
        Specific stlite version to use.
    pyodide_version : Optional[str]
        Specific Pyodide version to use.
    packages : Optional[Dict[str, str]]
        Package version overrides.
    ignore_dirs : Optional[list]
        List of directory names to ignore during auto-discovery.
    ignore_files : Optional[list]
        List of file names to ignore during auto-discovery.
    """
    #1. load versions
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
    
    #Update css, js, pyodide versions into settings
    settings.update({"|STLITE_CSS|":stylesheet})
    settings.update({"|STLITE_JS|":js})
    settings.update({"|PYODIDE_VERSION|":pyodide})

    # --- Auto Discovery: requirements.txt ---
    req_file = os.path.join(directory, 'requirements.txt')
    if os.path.isfile(req_file):
        print(f"* Found requirements.txt in {directory}. Parsing...")
        file_reqs = parse_requirements(req_file)

        current_reqs = settings.get('APP_REQUIREMENTS')
        if current_reqs is None:
            current_reqs = []

        # Merge requirements, avoiding exact duplicates
        for r in file_reqs:
            if r not in current_reqs:
                current_reqs.append(r)
                print(f"  - Added requirement from file: {r}")

        settings['APP_REQUIREMENTS'] = current_reqs
    
    #if app entrypoint in app files, remove it! It will be used to replace |APP_HOME| in the html template.
    app_files = settings.get('APP_FILES', [])
    if app_files is None:
        app_files = []

    # --- Auto Discovery ---
    # We now discover ALL files in the directory (respecting default ignores)
    print(f"* Starting discovery of all files in {directory}...")

    # Convert lists to sets for discovery.py
    ignore_dirs_set = set(ignore_dirs) if ignore_dirs else None
    ignore_files_set = set(ignore_files) if ignore_files else None

    discovered_files = discover_all_files(directory, ignore_dirs=ignore_dirs_set, ignore_files=ignore_files_set)

    for f in discovered_files:
        if f not in app_files:
            app_files.append(f)
            # print(f"  - Discovered file: {f}") # Can be verbose

    # Update settings with discovered files so create_html uses them
    settings['APP_FILES'] = app_files

    if settings.get('APP_ENTRYPOINT') in app_files:
        app_files.remove(settings.get('APP_ENTRYPOINT'))
    
    # 3. Check that all files exist.
    for file_j in app_files:
        if not file_exists(os.path.join(directory,file_j)): raise ValueError(f"* File {file_j} not found in {directory}.")
        
    # 4. generate html
    html = create_html(directory,settings,packages=packages)
    write_text_file(os.path.join(directory,f'{settings.get("APP_NAME").replace(" ","_")}.html'), html)


def s2s_convert(
    stlite_version: Optional[str] = None,
    pyodide_version: Optional[str] = None,
    directory: Optional[str] = None,
    packages: Optional[Dict[str, str]] = None
) -> None:
    """
    Converts a Streamlit application project into a single HTML file using stlite.

    See `_s2s_convert_core` for details on the conversion process.
    This function primarily handles loading settings from `settings.yaml`.
    """
    #0. read/set directory
    if directory is not None: #directory is provided
        #check provided directory is valid
        if not folder_exists(directory): raise ValueError(f'''* {directory} does not exist on this system.''')
    else:  #nodirectory provided, use cd
        directory = get_current_directory()
        print(f"* No user directory provided. Creating new s2stlite project in current directory ({directory}). \n")

    #1. read settings yaml
    if not file_exists(os.path.join(directory,'settings.yaml')): raise ValueError(f"* No settings file found in {directory}. Please run s2s_prepare_folder().")
    settings = load_yaml_from_file(os.path.join(directory,'settings.yaml'))

    #2. Call core conversion
    _s2s_convert_core(
        settings=settings,
        directory=directory,
        stlite_version=stlite_version,
        pyodide_version=pyodide_version,
        packages=packages,
        ignore_dirs=settings.get('IGNORE_DIRS'),
        ignore_files=settings.get('IGNORE_FILES')
    )


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
        packages : Optional[Dict[str, str]], optional
            A dictionary to override package versions.
        """
        s2s_convert(
            stlite_version=stlite_version,
            pyodide_version=pyodide_version,
            directory=self.directory,
            packages=packages
        )

    def convert_from_entrypoint(
        self,
        app_name: str,
        entrypoint: str,
        config: Optional[str] = None,
        shared_worker: bool = False,
        idbfs_mountpoints: Optional[list] = None,
        extra_files: Optional[list] = None,
        stlite_version: Optional[str] = None,
        pyodide_version: Optional[str] = None,
        packages: Optional[Dict[str, str]] = None,
        ignore_dirs: Optional[list] = None,
        ignore_files: Optional[list] = None
    ) -> None:
        """
        Converts a Streamlit application using parameters directly, skipping settings.yaml.

        Parameters
        ----------
        app_name : str
            The name of the application.
        entrypoint : str
            The entrypoint script filename (must be in the project directory).
        config : Optional[str], optional
            Path to streamlit config file (relative to project directory). Default None.
        shared_worker : bool, optional
            Whether to use SharedWorker mode. Default False.
        idbfs_mountpoints : Optional[list], optional
            List of mountpoints for IDBFS. Default None.
        extra_files : Optional[list], optional
            List of extra files to include manually. Default None.
        stlite_version : Optional[str], optional
            The specific version of stlite to use.
        pyodide_version : Optional[str], optional
            The specific version of Pyodide to use.
        packages : Optional[Dict[str, str]], optional
            Package version overrides.
        ignore_dirs : Optional[list], optional
            List of directory names to ignore during auto-discovery.
        ignore_files : Optional[list], optional
            List of file names to ignore during auto-discovery.
        """
        if idbfs_mountpoints is None:
            idbfs_mountpoints = ['/mnt']

        if extra_files is None:
            extra_files = []

        # Construct settings dictionary
        settings = {
            'APP_NAME': app_name,
            'APP_ENTRYPOINT': entrypoint,
            'CONFIG': config,
            'SHARED_WORKER': shared_worker,
            'IDBFS_MOUNTPOINTS': idbfs_mountpoints,
            'APP_FILES': extra_files,
            'APP_REQUIREMENTS': [] # Will be populated by requirements.txt scan in core
        }

        # Check entrypoint existence here to fail fast?
        # _s2s_convert_core checks discovery, but checking here is good practice.
        if not os.path.isfile(os.path.join(self.directory, entrypoint)):
            raise ValueError(f"Entrypoint file '{entrypoint}' not found in {self.directory}")

        print(f"* Converting from entrypoint '{entrypoint}' in {self.directory}...")

        _s2s_convert_core(
            settings=settings,
            directory=self.directory,
            stlite_version=stlite_version,
            pyodide_version=pyodide_version,
            packages=packages,
            ignore_dirs=ignore_dirs,
            ignore_files=ignore_files
        )

def convert_app(
    directory: str,
    app_name: str,
    entrypoint: str,
    config: Optional[str] = None,
    shared_worker: bool = False,
    idbfs_mountpoints: Optional[list] = None,
    extra_files: Optional[list] = None,
    stlite_version: Optional[str] = None,
    pyodide_version: Optional[str] = None,
    packages: Optional[Dict[str, str]] = None,
    ignore_dirs: Optional[list] = None,
    ignore_files: Optional[list] = None
) -> None:
    """
    Shortcut function to convert a Streamlit app in one step.

    Parameters
    ----------
    directory : str
        The root directory of the Streamlit application.
    app_name : str
        The name of the application.
    entrypoint : str
        The entrypoint script filename (must be in the directory).
    config : Optional[str], optional
        Path to streamlit config file (relative to directory). Default None.
    shared_worker : bool, optional
        Whether to use SharedWorker mode. Default False.
    idbfs_mountpoints : Optional[list], optional
        List of mountpoints for IDBFS. Default None.
    extra_files : Optional[list], optional
        List of extra files to include manually. Default None.
    stlite_version : Optional[str], optional
        The specific version of stlite to use.
    pyodide_version : Optional[str], optional
        The specific version of Pyodide to use.
    packages : Optional[Dict[str, str]], optional
        Package version overrides.
    ignore_dirs : Optional[list], optional
        List of directory names to ignore during auto-discovery.
    ignore_files : Optional[list], optional
        List of file names to ignore during auto-discovery.
    """
    converter = Script2StliteConverter(directory=directory)
    converter.convert_from_entrypoint(
        app_name=app_name,
        entrypoint=entrypoint,
        config=config,
        shared_worker=shared_worker,
        idbfs_mountpoints=idbfs_mountpoints,
        extra_files=extra_files,
        stlite_version=stlite_version,
        pyodide_version=pyodide_version,
        packages=packages,
        ignore_dirs=ignore_dirs,
        ignore_files=ignore_files
    )