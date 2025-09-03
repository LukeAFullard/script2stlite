import streamlit as st

st.title("Installer App")

st.info(
    "This app's `settings.yaml` file includes the `mpmath` package in its requirements."
)

st.write(
    "Because this app and the 'User App' are running in a shared worker "
    "(`SHARED_WORKER: true`), the `mpmath` package is available in the "
    "environment for both apps."
)

st.write(
    "You can now go to the **User App** and use the `mpmath` package without "
    "any installation needed there."
)
