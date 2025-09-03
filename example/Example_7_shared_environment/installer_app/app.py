import streamlit as st
import os

st.title("Installer App (File Writer)")

st.write(
    "This app is part of a diagnostic test. Its purpose is to write a file "
    "to a shared location (`/mnt/test.txt`) in the virtual file system."
)

if st.button("Write the test file"):
    file_path = "/mnt/test.txt"
    dir_name = os.path.dirname(file_path)

    try:
        # Create the directory if it doesn't exist
        if not os.path.exists(dir_name):
            st.write(f"Directory `{dir_name}` does not exist. Creating it...")
            os.makedirs(dir_name)
            st.write(f"Directory `{dir_name}` created.")

        # Write the file
        content = "Hello from the Installer App! The file was written successfully."
        with open(file_path, "w") as f:
            f.write(content)

        st.success(f"Successfully wrote file to `{file_path}`.")
        st.info("You can now go to the 'User App (File Reader)' to see if it can read this file.")

    except Exception as e:
        st.error(f"An error occurred: {e}")
