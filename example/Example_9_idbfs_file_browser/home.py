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

if not file_list:
    st.code(f"The `{mount_point}` directory is empty.", language="text")
else:
    st.write("Files in the persistent directory are listed below. You can delete files, but not directories with this tool.")
    for file_path in sorted(file_list):
        # We can only delete files, not directories, with this simple implementation.
        is_file = not file_path.endswith('/')

        col1, col2 = st.columns([0.8, 0.2])

        with col1:
            st.code(file_path, language="text")

        if is_file:
            with col2:
                if st.button("Delete", key=f"delete_{file_path}", use_container_width=True):
                    try:
                        full_path = os.path.join(mount_point, file_path)
                        os.remove(full_path)
                        st.success(f"Deleted `{file_path}`")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error deleting `{file_path}`: {e}")
