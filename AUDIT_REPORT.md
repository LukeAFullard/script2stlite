# Audit Report: Auto Discovery Features

This report outlines the caveats, issues, and security implications of the new auto-discovery features in `script2stlite`.

## Overview

The auto-discovery mechanism (`script2stlite/discovery.py`) scans the codebase to automatically identify and bundle:
1.  **Python Modules**: By parsing AST for `import` statements.
2.  **Assets**: By parsing AST for string literals that match local filenames.

## Caveats and Issues

### 1. Asset Over-Inclusion (Security Risk)
**Issue**: The asset discovery logic assumes that *any* string literal in the code that matches a relative path to an existing local file is an asset reference.
**Impact**:
- If a file is mentioned in a string (e.g., in a variable, a print statement, or an exclusion list), it will be bundled into the application.
- **Security**: "Secret" files (e.g., `.env`, `keys`, `passwords.txt`) could be inadvertently included if their names appear in the code (e.g., `ignore_files = ["secrets.txt"]`).
- **Path Traversal**: Strings containing `../` can resolve to files outside the project root (e.g., `../secrets.txt`), causing them to be bundled if they exist.
- **Mitigation**: Currently, there is no way to explicitly exclude files from being bundled if they are "discovered" this way.

### 2. Dynamic Imports are Ignored
**Issue**: The discovery relies on static AST parsing.
**Impact**:
- Imports using `importlib.import_module("module_name")` are not detected.
- `__import__("module_name")` is not detected.
- Code relying heavily on dynamic plugins will fail to bundle dependencies automatically.

### 3. Constructed File Paths are Ignored
**Issue**: Asset discovery only finds static string literals.
**Impact**:
- `f-strings` or concatenated strings (e.g., `f"data/{filename}.csv"`) are not detected.
- Users must manually add these files to `APP_FILES` in `settings.yaml`.

### 4. Wildcard Imports and `__all__`
**Issue**: `from package import *` imports are resolved to `package/__init__.py`.
**Impact**:
- The parser does not evaluate `__all__` in `__init__.py`.
- If `__init__.py` relies on `__all__` to export submodules without importing them explicitly, those submodules will *not* be bundled.

### 5. False Positives for Python Files
**Issue**: If a Python filename is mentioned in a string (e.g., `script_name = "app.py"`), it is added as an asset.
**Impact**:
- While usually harmless (files are deduped), it can lead to confusion or unintended bundling of scripts that were meant to be ignored.

### 6. Shadowing of Standard Library
**Issue**: Local files with names matching standard library modules (e.g., `json.py`, `html.py`) will be discovered and bundled.
**Impact**:
- In the Pyodide environment, `import json` will import the local `json.py` instead of the standard library `json` module, potentially breaking the application.

## Best Practice: Clean Directory Isolation

To mitigate security risks, users should strictly follow the **Clean Directory Principle**:

*   **Recommendation**: The directory provided to `script2stlite` should contain **only** the application files intended for distribution.
*   **Security Benefit**: If sensitive files (e.g., `.env`, `secrets.txt`) are **not present** in the directory (or its accessible parents), they cannot be bundled, even if the code references them (e.g., in an ignore list or via path traversal).
*   **Caveat**: While this prevents the *security risk* of leaking secrets, it does **not** solve the functionality issues (Issues 2, 3, 4, 6 above). Issues like missing dynamic imports or f-string assets will persist even in a clean directory and require the solutions proposed below.

## Suggested Fixes/Changes

### 1. Explicit Exclusion Mechanism (Zero-Config Friendly)
**Proposal**: Introduce a way to exclude files without requiring a `settings.yaml`.
**Options**:
1.  **Special Variable**: Support a `__stlite_ignore__` list in the Python script (detectable via AST).
2.  **Ignore File**: Support a simple `.stliteignore` file in the project root.
**Benefit**: Preserves the "zero-config" experience while allowing users to prevent sensitive files (like `.env`) from being bundled if they are referenced in the code (e.g., in an exclusion list).
**Context**: The current discovery system **already** ignores files that are unused. This mechanism is needed for files that **are** mentioned in the code (triggering discovery) but should not be bundled.

### 2. Context-Aware Discovery with Heuristics
**Proposal**: Move beyond simple string matching to a context-aware approach.
**Details**:
1.  **Function Call Analysis**: Prioritize string literals used as arguments to known I/O functions (e.g., `open()`, `st.image()`, `pandas.read_csv()`).
2.  **Constant Propagation**: Implement basic AST analysis to track variables holding filenames (e.g., `f = "data.csv"; st.image(f)`).
3.  **Extension Filtering**: For strings found outside of known functions, only auto-bundle "safe" asset types (e.g., images, data files) and ignore sensitive extensions (e.g., `.key`, `.env`, `.py`) unless explicitly used in an I/O context.
**Benefit**: Minimizes false positives (security risk) without sacrificing the convenience of auto-discovery for standard use cases. It bridges the gap between safety and ease of use.

### 3. Wildcard Import Handling
**Proposal**: When encountering `from package import *`, inspect the package's `__init__.py` for `__all__` definition.
**Details**: If `__all__` is present, resolve the listed submodules. If not, consider a "safe mode" that optionally includes all submodules in the package directory (or warn the user).

### 4. User Warnings
**Proposal**: Print a summary of discovered assets during the build process, highlighting potential security risks (e.g., files ending in `.key`, `.env`, `.pem`).
**Benefit**: Increases visibility of what is being bundled, allowing users to catch accidental inclusions before deployment.

### 5. Support for Dynamic/Constructed Cases
**Proposal**: Attempt to support common dynamic patterns instead of just documenting non-support.
**Details**:
1.  **Pattern Matching for F-Strings**: Analyze f-strings to identify file patterns. For example, if `f"data/{name}.csv"` is detected, the scanner could perform a wildcard expansion (glob) to bundle all `data/*.csv` files.
2.  **Literal Dynamic Imports**: Detect simple dynamic imports where the module name is a string literal (e.g., `importlib.import_module("my_plugin")`) and treat them as static imports.
**Benefit**: Significantly reduces the need for manual `settings.yaml` configuration, moving closer to a true "zero-config" experience even for complex apps.

## Summary of Verified Behaviors

A test suite `tests/test_audit_scenarios.py` has been added to the repository to document and verify these behaviors.

| Scenario | Behavior | Status |
| :--- | :--- | :--- |
| **Static Import** | `import foo` -> bundles `foo.py` | ✅ Working |
| **Relative Import** | `from . import bar` -> bundles `bar.py` | ✅ Working |
| **Dynamic Import** | `importlib.import_module('foo')` -> `foo.py` ignored | ⚠️ Caveat |
| **Static Asset** | `open("data.csv")` -> bundles `data.csv` | ✅ Working |
| **Dynamic Asset** | `open(f"{file}.csv")` -> `data.csv` ignored | ⚠️ Caveat |
| **String Match** | `x = "secret.key"` -> bundles `secret.key` | ❌ Security Issue |
| **Wildcard Import** | `from pkg import *` -> ignores `__all__` | ⚠️ Caveat |
