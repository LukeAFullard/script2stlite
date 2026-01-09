import ast
import os
from typing import Set, List, Tuple

def find_imports(script_path: str, root_dir: str) -> Set[str]:
    """
    Recursively find all local Python modules imported by the script.

    Parameters
    ----------
    script_path : str
        The path to the Python script to parse.
    root_dir : str
        The root directory of the application.

    Returns
    -------
    Set[str]
        A set of relative file paths (relative to root_dir) of imported local modules.
    """
    discovered_files = set()
    visited_scripts = set()
    queue = [script_path]

    while queue:
        current_script = queue.pop(0)
        if current_script in visited_scripts:
            continue
        visited_scripts.add(current_script)

        # Read the script content
        try:
            with open(current_script, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            print(f"Warning: Could not read file {current_script}: {e}")
            continue

        # Parse AST
        try:
            tree = ast.parse(content)
        except Exception as e:
            print(f"Warning: Could not parse AST for {current_script}: {e}")
            continue

        # Walk AST to find imports
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    # Check if the imported module exists locally
                    local_files = resolve_module(alias.name, root_dir)
                    for f in local_files:
                        rel_path = os.path.relpath(f, root_dir)
                        if rel_path not in discovered_files:
                            discovered_files.add(rel_path)
                            queue.append(f)

            elif isinstance(node, ast.ImportFrom):
                level = node.level
                module_name = node.module

                if level == 0:
                    # Absolute import
                    if module_name:
                        local_files = resolve_module(module_name, root_dir)
                        for f in local_files:
                            rel_path = os.path.relpath(f, root_dir)
                            if rel_path not in discovered_files:
                                discovered_files.add(rel_path)
                                queue.append(f)

                        # Handle 'from package import submodule'
                        # e.g. from utils import formatting
                        # We resolved 'utils', now check if 'formatting' is a file inside utils package
                        package_dir = None
                        for f in local_files:
                            if f.endswith("__init__.py"):
                                package_dir = os.path.dirname(f)
                                break

                        if package_dir:
                            for alias in node.names:
                                sub_files = resolve_module(alias.name, package_dir)
                                for f in sub_files:
                                    rel_path = os.path.relpath(f, root_dir)
                                    if rel_path not in discovered_files:
                                        discovered_files.add(rel_path)
                                        queue.append(f)

                else:
                    # Relative import
                    script_dir = os.path.dirname(current_script)
                    base_dir = script_dir
                    # level 1 = current dir (no ascent), level 2 = parent (1 ascent), etc.
                    for _ in range(level - 1):
                        base_dir = os.path.dirname(base_dir)

                    if module_name:
                         # e.g. from .bar import ...
                         # First resolve the module itself (e.g. .bar -> .../bar.py or .../bar/__init__.py)
                         local_files = resolve_module(module_name, base_dir)
                         for f in local_files:
                            rel_path = os.path.relpath(f, root_dir)
                            if rel_path not in discovered_files:
                                discovered_files.add(rel_path)
                                queue.append(f)

                         # Then check if we are importing specific submodules from it
                         # e.g. from .bar import baz -> check .../bar/baz.py
                         package_dir = None
                         for f in local_files:
                             if f.endswith("__init__.py"):
                                 package_dir = os.path.dirname(f)
                                 break

                         if package_dir:
                             for alias in node.names:
                                 # alias.name might be a submodule file
                                 sub_files = resolve_module(alias.name, package_dir)
                                 for f in sub_files:
                                    rel_path = os.path.relpath(f, root_dir)
                                    if rel_path not in discovered_files:
                                        discovered_files.add(rel_path)
                                        queue.append(f)

                    else:
                        # e.g. from . import bar
                        for alias in node.names:
                            local_files = resolve_module(alias.name, base_dir)
                            for f in local_files:
                                rel_path = os.path.relpath(f, root_dir)
                                if rel_path not in discovered_files:
                                    discovered_files.add(rel_path)
                                    queue.append(f)

    # Remove the script itself if it was added (unlikely if resolve_module works correctly relative to root)
    return discovered_files

def find_pages(root_dir: str) -> Set[str]:
    """
    Find all python scripts in the 'pages' subdirectory, which Streamlit
    treats as multipage app pages.

    Parameters
    ----------
    root_dir : str
        The root directory of the application.

    Returns
    -------
    Set[str]
        A set of relative file paths for pages.
    """
    pages_dir = os.path.join(root_dir, 'pages')
    discovered_pages = set()

    if os.path.isdir(pages_dir):
        for root, dirs, files in os.walk(pages_dir):
            for file in files:
                if file.endswith('.py'):
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, root_dir)
                    discovered_pages.add(rel_path)

    return discovered_pages

def resolve_module(module_name: str, root_dir: str) -> List[str]:
    """
    Resolve a module name to a list of file paths.
    E.g. "helper" -> ["/path/to/helper.py"]
    "package.module" -> ["/path/to/package/module.py"]
    "package" -> ["/path/to/package/__init__.py"]
    """
    parts = module_name.split('.')
    path = os.path.join(root_dir, *parts)

    files = []

    # Check for module.py
    py_file = path + ".py"
    if os.path.isfile(py_file):
        files.append(py_file)

    # Check for package/__init__.py
    init_file = os.path.join(path, "__init__.py")
    if os.path.isfile(init_file):
        files.append(init_file)

    return files

def find_assets(script_path: str, root_dir: str, known_python_files: Set[str] = None) -> Set[str]:
    """
    Recursively find potential assets referenced in Python scripts.
    It scans for string literals that correspond to existing files in root_dir.

    Parameters
    ----------
    script_path : str
        The path to the entrypoint script.
    root_dir : str
        The root directory of the application.
    known_python_files : Set[str]
        A set of known Python files (relative to root_dir) to scan.
        If None, only scans script_path.

    Returns
    -------
    Set[str]
        A set of relative file paths of potential assets.
    """
    if known_python_files is None:
        files_to_scan = {script_path}
    else:
        files_to_scan = {os.path.join(root_dir, f) for f in known_python_files}
        files_to_scan.add(script_path)

    discovered_assets = set()

    for script in files_to_scan:
        if not os.path.exists(script):
            continue

        try:
            with open(script, "r", encoding="utf-8") as f:
                content = f.read()
            tree = ast.parse(content)
        except Exception as e:
            print(f"Warning: Could not parse {script} for assets: {e}")
            continue

        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                # Potential file path
                potential_path = node.value

                # Check if it exists relative to root_dir
                # Be careful with absolute paths or paths starting with /
                if os.path.isabs(potential_path):
                     # If absolute, check if it is within root_dir (rare for portable apps but possible)
                     # But usually user writes "data/file.csv".
                     # If user writes "/data/file.csv", likely means root?
                     continue

                # Check relative to root_dir
                full_path_root = os.path.join(root_dir, potential_path)
                if os.path.isfile(full_path_root):
                     # Ensure it's not the script itself or one of the known python files (optional, but good to avoid dupes)
                     # Although convert function handles duplicates, no harm adding here.
                     rel_path = os.path.relpath(full_path_root, root_dir)
                     # Exclude .py files that are already discovered via imports?
                     # Or just include everything found. The caller merges lists.
                     # But we generally don't want to include .py files as assets if they are code.
                     # However, if code reads a .py file as text (e.g. st.code), it should be an asset?
                     # In stlite, 'files' dict contains both code and assets.
                     if rel_path != os.path.relpath(script, root_dir):
                        discovered_assets.add(rel_path)

    return discovered_assets
