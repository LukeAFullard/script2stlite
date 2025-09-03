# Example 7: Shared Environment

This example demonstrates the `SHARED_WORKER` mode of `script2stlite`. It consists of two separate Streamlit applications that share the same Python environment.

- **Installer App**: This app uses `micropip` to install the `tiny-math` package.
- **User App**: This app imports and uses the `tiny-math` package, even though it is not listed in its own requirements.

This setup showcases how modifications to the Python environment (like installing packages) are shared across all apps running in the same shared worker.

## How to Run

1.  **Convert the apps**:
    -   The `installer_app` and `user_app` directories each contain a `settings.yaml` file with `SHARED_WORKER: true`.
    -   Run the `script2stlite.convert()` function on each of these directories to generate the `Installer_App.html` and `User_App.html` files.

2.  **Open `index.html`**:
    -   Open the `index.html` file in this directory in a web browser. This file displays both apps side-by-side in iframes.

First, click the "Install `tiny-math` package" button in the "Installer App". Once it's installed, click the "Try to use `tiny-math`" button in the "User App". You should see a success message and the result of the `tiny_math.add()` function.
