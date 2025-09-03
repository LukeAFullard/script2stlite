import streamlit as st
import os

st.title("IDBFS File Browser")

st.info(
    "This app lists all files and directories in the persistent `/mnt` directory, "
    "which is stored in your browser's IndexedDB. \n\n"
    "Run the **File Persistence Demo (Example 8)** first to create a log file. "
    "You should see that `log.txt` file listed here after running it."
)

mount_point = "/mnt"
file_list = []

if not os.path.exists(mount_point):
    st.warning(f"The mount point `{mount_point}` does not exist. It will be created on the first file operation.")
else:
    for root, dirs, files in os.walk(mount_point):
        # To make the path relative to the mount point for cleaner display
        relative_root = os.path.relpath(root, mount_point)
        if relative_root == ".":
            relative_root = ""

        for name in files:
            file_list.append(os.path.join(relative_root, name))
        for name in dirs:
            # Adding a slash to indicate it's a directory
            file_list.append(os.path.join(relative_root, name) + "/")

st.subheader(f"Contents of `{mount_point}`:")

if file_list:
    st.code("\n".join(sorted(file_list)), language="text")
else:
    st.code(f"The `{mount_point}` directory is empty.", language="text")
