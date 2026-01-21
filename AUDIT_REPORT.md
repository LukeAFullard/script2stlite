# Audit Report: Auto Discovery Features

This report outlines the caveats, issues, and security implications of the new auto-discovery features in `script2stlite`.

## Overview

The auto-discovery mechanism (`script2stlite/discovery.py`) has been simplified to:
**Bundle all files in the provided directory**, excluding standard system/IDE directories (e.g., `.git`, `__pycache__`, `venv`, `node_modules`).

This replaces the previous AST-based static analysis, ensuring that all functional dependencies (dynamic imports, f-string assets, etc.) are included, provided they exist in the directory.

## Caveats and Issues

### 1. Responsibility for "Clean Directory"
**Issue**: Since all files in the directory are bundled, any sensitive file present (e.g., `.env`, `secrets.txt`, `keys/`) will be included in the public HTML bundle.
**Mitigation**: Users **must** adhere to the **Clean Directory Principle**:
- The directory provided to `script2stlite` should contain **only** the application files intended for distribution.
- **Environment files** (like `.env`) should generally be kept out of the target directory or added to a manual exclusion list if implemented in the future. (Note: `.env` is currently in the default ignore list).

### 2. Standard Library Shadowing
**Issue**: Local files with names matching standard library modules (e.g., `json.py`, `html.py`) will be bundled.
**Impact**:
- In the Pyodide environment, `import json` will import the local `json.py` instead of the standard library `json` module, potentially breaking the application.
- This is standard Python behavior, but more likely to occur if users include random scripts in the directory.

## Solved Issues (vs Previous AST Approach)

The following issues identified in previous audits are **resolved** by the "include all" strategy:

*   **Dynamic Imports**: `importlib.import_module("foo")` now works because `foo.py` is included if present.
*   **Constructed File Paths**: `f"data/{name}.csv"` now works because all files in `data/` are included.
*   **Wildcard Imports**: `from pkg import *` now works because the entire package directory is included.
*   **False Negatives**: No more missing files due to parser limitations.

## Default Ignore List

The following files and directories are excluded by default to keep bundles clean:

**Directories:**
- `.git`
- `__pycache__`
- `venv`, `.venv`, `env`
- `.mypy_cache`, `.pytest_cache`
- `dist`, `build`
- `.idea`, `.vscode`
- `node_modules`

**Files:**
- `.DS_Store`
- `.gitignore`
- `.env`

## Summary of Verified Behaviors

A test suite `tests/test_audit_scenarios.py` verifies these behaviors.

| Scenario | Behavior | Status |
| :--- | :--- | :--- |
| **Static Import** | `import foo` -> bundles `foo.py` | ✅ Working |
| **Dynamic Import** | `importlib.import_module('foo')` -> bundles `foo.py` | ✅ Working |
| **Dynamic Asset** | `open(f"{file}.csv")` -> bundles `data.csv` | ✅ Working |
| **Unused Files** | `unused.txt` -> bundles `unused.txt` | ✅ Working (Intended) |
| **Secrets** | `.env` present in dir -> ignored by default | ✅ Working |
| **Ignored Dirs** | `.git` folder -> ignored | ✅ Working |
