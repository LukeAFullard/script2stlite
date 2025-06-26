from functions import load_all_versions

def s2s_prepare_folder():
    #destination 
    pass



def s2s_convert(stlite_version = None, pyodide_version = None):
    #load settings
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