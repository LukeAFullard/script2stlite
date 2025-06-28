import streamlit as st

# This is the main application file.
# Streamlit automatically picks up other pages from the 'pages' directory.

st.set_page_config(
    page_title="Image Editor Pro",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="expanded" # Ensures sidebar is open by default
)

# Optional: Add a small note in the main app.py if desired, though most content will be in pages.
# st.sidebar.info("Navigate through the app using the sidebar.")

# When running `streamlit run app.py`, Streamlit will:
# 1. Execute this `app.py` file.
# 2. Scan the `pages/` subdirectory for any `.py` files.
# 3. Each file in `pages/` will be listed in the sidebar as a navigable page.
#    The filename (with number and emoji prefix removed, and underscores replaced by spaces) becomes the page title.
#    For example, `pages/01_Home.py` becomes "Home".
#    `pages/02_Upload_Image.py` becomes "Upload Image".

# No explicit routing or page definition is needed here beyond this structure.
# The `01_Home.py` will be treated as the default page to show if no specific page is selected,
# or often, Streamlit will show the first page in the `pages` directory alphabetically if app.py is minimal.
# By convention, the main app.py can also be a landing/welcome page if it has content.
# In our case, 01_Home.py in pages/ is the explicit welcome page.

# If st.set_page_config is called in one of the page files (e.g. pages/01_Home.py),
# Streamlit might throw an error or behave unpredictably because it should only be called once.
# I've ensured it's in `01_Home.py` and now also here. I should remove it from `01_Home.py`
# to avoid conflicts.

# For now, let's keep this app.py extremely minimal.
# The `st.set_page_config` is the most important part for the overall app configuration.
# The content for the "main" page of the application is now in `pages/01_Home.py`.
# Streamlit will automatically make `pages/01_Home.py` the first page in the navigation.

st.markdown("Redirecting to Home page...")
st.switch_page("pages/01_Home.py")
