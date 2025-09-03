import streamlit as st
import datetime
import os

st.title("File Persistence Demo")
st.write(
    "This app demonstrates file persistence using the IDBFS (IndexedDB File System). "
    "Each time you reload this page, a new timestamp is appended to a log file "
    "stored in the browser's IndexedDB."
)

log_file = "/mnt/log.txt"

# Ensure the mount point directory exists within the virtual file system
if not os.path.exists("/mnt"):
    os.makedirs("/mnt")

# Append the current timestamp to the log file
with open(log_file, "a") as f:
    f.write(f"App opened at: {datetime.datetime.now()}\\n")

# Read and display the entire log file
st.subheader("Log File Content")
try:
    with open(log_file, "r") as f:
        log_content = f.read()
        st.code(log_content, language="text")
except FileNotFoundError:
    st.code("Log file not found. It will be created on the next run.", language="text")
