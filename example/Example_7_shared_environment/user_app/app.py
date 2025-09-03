import streamlit as st
import asyncio
import os

st.title("User App (File Reader)")

st.write(
    "This app is part of a diagnostic test. Its purpose is to read a file "
    "that should have been created by the 'Installer App'."
)

if st.button("Read the test file"):
    file_path = "/mnt/test.txt"
    max_retries = 5
    retry_delay = 2  # seconds

    for attempt in range(max_retries):
        st.info(f"Attempt {attempt + 1}: Checking for file `{file_path}`...")
        if os.path.exists(file_path):
            try:
                with open(file_path, "r") as f:
                    content = f.read()
                st.success(f"Successfully read the file on attempt {attempt + 1}!")
                st.text_area("File Content", content, height=150)
                # Exit the loop on success
                break
            except Exception as e:
                st.error(f"File exists, but failed to read it: {e}")
                break # Exit loop if reading fails
        else:
            if attempt < max_retries - 1:
                st.write(f"File not found. Retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
            else:
                st.error(
                    f"Failed to find file `{file_path}` after {max_retries} attempts. "
                    "This suggests the file system is not shared as expected."
                )
