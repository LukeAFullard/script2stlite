from functions import load_all_versions,folder_exists,get_current_directory,create_directory,copy_file_from_subfolder,file_exists
import os

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

        



def s2s_convert(stlite_version = None, pyodide_version = None):
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