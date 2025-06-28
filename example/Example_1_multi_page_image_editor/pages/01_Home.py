import streamlit as st

# Page configuration is handled in the main app.py

st.title("🖼️ Welcome to Image Editor Pro!")

st.sidebar.success("Select a page above to get started.")

st.markdown(
    """
    This application allows you to upload an image and perform various adjustments.

    **👈 Select a page from the sidebar** to either upload a new image or
    start editing an existing one (if already uploaded).

    ### Features:
    - **Upload Image:** Securely upload your JPG, JPEG, or PNG images.
    - **Adjust Image:** Modify brightness, contrast, rotate, or convert to grayscale.
    - **Side-by-side View:** Compare the original and modified images in real-time.
    - **Download:** Save your masterpiece!

    We hope you enjoy using Image Editor Pro!
"""
)
