from functions import load_all_versions,folder_exists,get_current_directory,create_directory,copy_file_from_subfolder,file_exists, load_yaml_from_file,file_to_ou_base64_string
import os
from pathlib import Path

def s2s_prepare_folder(directory = None):
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

        



def s2s_convert(stlite_version = None, pyodide_version = None, directory = None):
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
    
    #if app entrypoint not in app files, add it in
    if settings.get('APP_ENTRYPOINT') not in settings.get('APP_FILES'): settings.get('APP_FILES').append(settings.get('APP_ENTRYPOINT'))
    
    # 3. Check that all files exist.
    for file_j in settings.get('APP_FILES'):
        if not file_exists(os.path.join(directory,file_j)): raise ValueError(f"* File {file_j} not found in {directory}.")
        
        #add next line later when adding files into html
        #if not Path(file_j).suffix == '.py': file_to_ou_base64_string(os.path.join(directory,file_j))
    