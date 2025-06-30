# PixelHue: Image Color Palette Generator - `script2stlite` Example

This directory contains Juncel Datinggaling's PixelHue Streamlit application, which has been converted into a self-contained static web application using the `script2stlite` package. PixelHue analyzes an image and extracts its dominant colors to generate a palette.

## `script2stlite`

The `script2stlite` package is a tool for converting Streamlit Python scripts into static HTML files that run entirely in the browser, powered by Pyodide. This is particularly useful as it allows complex Streamlit apps, even those with machine learning dependencies like scikit-learn, to run client-side without a Python backend.

This conversion simplifies deployment, allowing the application to be hosted on static web services like GitHub Pages or shared as a single HTML file.

## Original Application Credit

The PixelHue application was originally created by **Juncel Datinggaling**. We appreciate their work in developing this tool.

*   **Original Creator:** Juncel Datinggaling
*   **Original GitHub Repository:** [j-ncel/PixelHue](https://github.com/j-ncel/PixelHue)
*   **Original Live Streamlit App (requires Python backend):** [pixelhue.streamlit.app](https://pixelhue.streamlit.app/)

## Hosted `script2stlite` Version

This `script2stlite`-converted version of PixelHue can be accessed here:
[https://lukeafullard.github.io/script2stlite/example/Example_5_PixelHue/PixelHue.html](https://lukeafullard.github.io/script2stlite/example/Example_5_PixelHue/PixelHue.html)

## Functionality

The application allows users to:
1.  Upload an image (JPG, PNG, etc.).
2.  Specify the number of dominant colors to extract.
3.  View the uploaded image alongside the generated color palette (with HEX codes).

`script2stlite` turns the streamlit app to an stlite app to allow the app to run in the browser via Pyodide. The source Python script for this application is [main.py](./main.py) (which uses [palette_extractor.py](./palette_extractor.py)).
