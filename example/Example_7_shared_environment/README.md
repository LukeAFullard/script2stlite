# Example 7: Shared Environment

This example demonstrates the `SHARED_WORKER` mode of `script2stlite`. It consists of two separate Streamlit applications that share the same Python environment.

- **Installer App**: This app's `settings.yaml` file lists `mpmath` as a requirement.
- **User App**: This app can import and use the `mpmath` package because it shares the same environment as the 'Installer App', even though `mpmath` is not listed in its own requirements.

This setup showcases how the Python environment (including packages specified in `settings.yaml`) is shared across all apps running in the same shared worker.

## How to Run

1.  **Convert the apps**:
    -   The `installer_app` and `user_app` directories each contain a `settings.yaml` file with `SHARED_WORKER: true`.
    -   Run the `script2stlite.convert()` function on each of these directories to generate the `Installer_App.html` and `User_App.html` files.

2.  **Open `index.html`**:
    -   Open the `index.html` file in this directory in a web browser. This file displays both apps side-by-side in iframes.

The 'Installer App' explains the setup. You can go directly to the 'User App' and click the "Use `mpmath` package" button to see that the package is available and works correctly.
