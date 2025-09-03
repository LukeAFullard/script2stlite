# Example 7: Shared Worker Counter

This example demonstrates the `SHARED_WORKER` mode of `script2stlite`. It consists of two separate Streamlit applications that share the same state using a single worker.

- **Control App**: A simple app with a button to increment a counter.
- **Display App**: An app that continuously displays the current value of the counter from the shared state.

This setup showcases how multiple `stlite` apps can communicate and share data when running in SharedWorker mode.

## How to Run

1.  **Convert the apps**:
    -   The `control_app` and `display_app` directories each contain a `settings.yaml` file with `SHARED_WORKER: true`.
    -   Run the `script2stlite.convert()` function on each of these directories to generate the `Control_App.html` and `Display_App.html` files.

2.  **Open `index.html`**:
    -   Open the `index.html` file in this directory in a web browser. This file displays both apps side-by-side in iframes.

When you click the button in the "Control App", you will see the counter value update in real-time in the "Display App".
