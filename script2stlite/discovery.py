import os
from typing import Set

DEFAULT_IGNORE_DIRS = {
    '.git',
    '__pycache__',
    'venv',
    '.venv',
    'env',
    '.mypy_cache',
    '.pytest_cache',
    'dist',
    'build',
    '.idea',
    '.vscode',
    'node_modules'
}

DEFAULT_IGNORE_FILES = {
    '.DS_Store',
    '.gitignore',
    '.env'
}

def discover_all_files(root_dir: str, ignore_dirs: Set[str] = None, ignore_files: Set[str] = None) -> Set[str]:
    """
    Recursively find all files in the root_dir, excluding those in the ignore lists.

    Parameters
    ----------
    root_dir : str
        The root directory of the application.
    ignore_dirs : Set[str]
        Set of directory names to ignore.
    ignore_files : Set[str]
        Set of file names to ignore.

    Returns
    -------
    Set[str]
        A set of relative file paths (relative to root_dir).
    """
    if ignore_dirs is None:
        ignore_dirs = DEFAULT_IGNORE_DIRS
    if ignore_files is None:
        ignore_files = DEFAULT_IGNORE_FILES

    discovered_files = set()

    for root, dirs, files in os.walk(root_dir):
        # Modify dirs in-place to skip ignored directories
        dirs[:] = [d for d in dirs if d not in ignore_dirs]

        for file in files:
            if file in ignore_files:
                continue

            # Construct full path and relative path
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, root_dir)

            discovered_files.add(rel_path)

    return discovered_files
