import streamlit as st
from PIL import Image
import io

# Page config is in main app.py
# st.set_page_config(page_title="Upload Image", page_icon="⬆️")

st.markdown("# ⬆️ Upload Image")
st.sidebar.header("Image Uploader") # Updates sidebar header for this page

st.write(
    """
    Upload an image to start editing. Supported formats: JPG, JPEG, PNG.
    """
)

# Allowed file types
ALLOWED_TYPES = ['jpg', 'jpeg', 'png']
TEST_IMAGE_PATH = "assets/image.png" # Path relative to app root (app.py)

# --- Test Image Loading Function ---
def load_and_store_image(image_path, default_name="test_image.png"):
    try:
        with open(image_path, "rb") as f:
            img_bytes = f.read()

        image = Image.open(io.BytesIO(img_bytes))

        # Store essential info in session state
        st.session_state['uploaded_image_bytes'] = img_bytes
        st.session_state['uploaded_image_name'] = default_name
        st.session_state['uploaded_image_format'] = image.format # PIL format

        # Clear any previous adjustment states
        if 'adjusted_image_bytes' in st.session_state:
            del st.session_state['adjusted_image_bytes']
        if 'adjustment_params' in st.session_state:
            del st.session_state['adjustment_params']

        st.success(f"'{default_name}' loaded successfully! Format: {image.format}. You can now go to the 'Adjust Image' page.")
        st.image(image, caption=f"Loaded: {default_name}", use_container_width=True)
        # It might be good to clear uploaded_file if it was set by st.file_uploader
        # However, st.rerun() might be needed, or careful state management.
        # For now, loading test image will overwrite previous upload.
        if "image_uploader" in st.session_state and st.session_state.image_uploader is not None:
            st.session_state.image_uploader = None # Attempt to reset file uploader
            # This reset is not always reliable with st.file_uploader's internal state.
            # A full st.rerun() might be more robust if issues arise.

    except FileNotFoundError:
        st.error(f"Test image not found at '{image_path}'. Please ensure the file exists.")
    except IOError:
        st.error(f"The test image at '{image_path}' is not a valid image or is corrupted.")
    except Exception as e:
        st.error(f"An unexpected error occurred while loading the test image: {e}")

# --- UI Elements ---
col1, col2 = st.columns([0.7, 0.3])

with col1:
    uploaded_file = st.file_uploader(
        "Choose an image file",
        type=ALLOWED_TYPES,
        accept_multiple_files=False,
        key="image_uploader" # Unique key for the widget
    )
with col2:
    st.write("") # Spacer
    st.write("") # Spacer
    if st.button("Load Test Image", key="load_test_image"):
        load_and_store_image(TEST_IMAGE_PATH)
        # If button is clicked, we don't want to process uploaded_file in the same run
        # Setting uploaded_file to None if test image is loaded, or use st.rerun()
        uploaded_file = None # Ensure uploaded_file logic isn't triggered if test image is loaded
        st.rerun() # Rerun to ensure state consistency after loading test image

if uploaded_file is not None:
    # This block will now only execute if a file was uploaded AND test image button wasn't just pressed
    img_bytes = uploaded_file.getvalue()
    file_name = uploaded_file.name

    try:
        image = Image.open(io.BytesIO(img_bytes))
        # Store essential info in session state
        st.session_state['uploaded_image_bytes'] = img_bytes
        st.session_state['uploaded_image_name'] = file_name
        st.session_state['uploaded_image_format'] = image.format

        # Clear any previous adjustment states if a new image is uploaded
        if 'adjusted_image_bytes' in st.session_state:
            del st.session_state['adjusted_image_bytes']
        if 'adjustment_params' in st.session_state:
            del st.session_state['adjustment_params']

        st.success(f"'{file_name}' uploaded successfully! Format: {image.format}. You can now go to the 'Adjust Image' page.")
        st.image(image, caption=f"Uploaded: {file_name}", use_container_width=True)

    except IOError:
        st.error("The uploaded file is not a valid image or is corrupted. Please try another file.")
        keys_to_delete = ['uploaded_image_bytes', 'uploaded_image_name', 'uploaded_image_format', 'adjusted_image_bytes']
        for key in keys_to_delete:
            if key in st.session_state: del st.session_state[key]
    except Exception as e:
        st.error(f"An unexpected error occurred while processing the uploaded image: {e}")
        keys_to_delete = ['uploaded_image_bytes', 'uploaded_image_name', 'uploaded_image_format', 'adjusted_image_bytes']
        for key in keys_to_delete:
            if key in st.session_state: del st.session_state[key]


# Display current image in session state if any
# This logic needs to be aware that uploaded_file might be None either initially,
# or after the test image button was pressed and caused a rerun.
if 'uploaded_image_bytes' in st.session_state and uploaded_file is None:
    # Check if the uploader is also clear or if its state needs managing
    # This part shows the image if one is in session AND the uploader is not currently holding a new file
    # (e.g., page just loaded, or test image was loaded, or user cleared uploader)
    st.write("---")
    st.write("Current image in session:")
    try:
        current_img_preview = Image.open(io.BytesIO(st.session_state['uploaded_image_bytes']))
        st.image(current_img_preview, caption=f"Current: {st.session_state.get('uploaded_image_name', 'N/A')}", use_container_width=True)

        col1, col2 = st.columns([0.7, 0.3])
        with col1:
            st.write("To change the image, use the uploader above.")
        with col2:
            if st.button("Clear Session Image", key="clear_session_image"):
                keys_to_delete = ['uploaded_image_bytes', 'uploaded_image_name', 'uploaded_image_format', 'adjusted_image_bytes', 'adjustment_params']
                for key in keys_to_delete:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()

    except Exception as e:
        st.error(f"Could not display current image from session: {e}")
        # Aggressively clear session state if it seems corrupted
        keys_to_delete = ['uploaded_image_bytes', 'uploaded_image_name', 'uploaded_image_format', 'adjusted_image_bytes', 'adjustment_params']
        for key in keys_to_delete:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun() # Rerun to reflect cleared state
elif uploaded_file is None:
    pass # Message "Please upload an image file to proceed." is already shown by uploader logic
