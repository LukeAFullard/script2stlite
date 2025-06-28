import streamlit as st
from PIL import Image, ImageEnhance, ImageOps
import io
import os

# Page config is in main app.py
# st.set_page_config(page_title="Adjust Image", page_icon="🛠️")

st.markdown("# 🛠️ Adjust Image")
st.sidebar.header("Image Adjustments")

# Function to apply adjustments
def apply_adjustments(image_bytes, brightness, contrast, rotation, grayscale):
    img = Image.open(io.BytesIO(image_bytes))
    original_format = img.format

    if grayscale:
        img = ImageOps.grayscale(img)
        # Grayscale might convert image to 'L' mode. If so, convert back to RGB for consistency with color operations.
        if img.mode == 'L':
            img = img.convert('RGB')

    if brightness != 1.0:
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(brightness)

    if contrast != 1.0:
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(contrast)

    if rotation != 0:
        img = img.rotate(-rotation, expand=True) # PIL rotates counter-clockwise

    # Save adjusted image to bytes buffer
    buffer = io.BytesIO()
    # Preserve original format if PNG, otherwise default to PNG for broader compatibility (handles transparency)
    save_format = 'PNG' # Default to PNG for download
    if original_format == 'JPEG' and not grayscale and rotation == 0 : # Only keep JPEG if no alpha channel introduced
         # If grayscale or rotation happened, PNG is safer.
         # JPEG doesn't support alpha. If rotation created transparent areas, it needs PNG.
         # Grayscale might be fine, but PNG is a safe bet.
         # For simplicity now, let's stick to PNG for adjusted images to handle all cases.
         pass # Keep save_format as PNG

    img.save(buffer, format=save_format)
    return buffer.getvalue(), save_format


# Check if an image is loaded in session state
if 'uploaded_image_bytes' not in st.session_state:
    st.warning("No image uploaded. Please go to the 'Upload Image' page first.")
    if st.button("Go to Upload Page"):
        st.switch_page("pages/02_Upload_Image.py")
    st.stop()

# Retrieve original image from session state
original_image_bytes = st.session_state['uploaded_image_bytes']
original_image_name = st.session_state.get('uploaded_image_name', 'image.png')
original_pil_image = Image.open(io.BytesIO(original_image_bytes))

# Initialize adjustment parameters in session state if not present
if 'adjustment_params' not in st.session_state:
    st.session_state.adjustment_params = {
        'brightness': 1.0,
        'contrast': 1.0,
        'rotation': 0,
        'grayscale': False
    }

# Sidebar for controls
with st.sidebar:
    st.subheader("Adjustment Controls")

    # Retrieve current params for widget defaults
    params = st.session_state.adjustment_params

    brightness = st.slider("Brightness", 0.5, 2.0, params['brightness'], 0.1, key="brightness_slider")
    contrast = st.slider("Contrast", 0.5, 2.0, params['contrast'], 0.1, key="contrast_slider")
    rotation = st.selectbox("Rotation (degrees)", [0, 90, 180, 270],
                            index=[0, 90, 180, 270].index(params['rotation']), key="rotation_select")
    grayscale = st.checkbox("Grayscale", value=params['grayscale'], key="grayscale_check")

    # Update session state if any parameter changed
    if (brightness != params['brightness'] or
        contrast != params['contrast'] or
        rotation != params['rotation'] or
        grayscale != params['grayscale']):

        st.session_state.adjustment_params = {
            'brightness': brightness,
            'contrast': contrast,
            'rotation': rotation,
            'grayscale': grayscale
        }
        # Clear previous adjusted image if params change
        if 'adjusted_image_bytes' in st.session_state:
            del st.session_state['adjusted_image_bytes']
        st.rerun() # Rerun to apply changes

# Apply adjustments if parameters are set
adjusted_image_bytes = None
adjusted_image_format = "PNG" # Default download format

# Use cached adjusted image if parameters haven't changed, otherwise recompute
if 'adjusted_image_bytes' in st.session_state and st.session_state.adjustment_params == {
        'brightness': brightness, 'contrast': contrast, 'rotation': rotation, 'grayscale': grayscale}:
    adjusted_image_bytes = st.session_state.adjusted_image_bytes
    adjusted_image_format = st.session_state.get('adjusted_image_format', 'PNG')
else:
    if original_image_bytes:
        current_params = st.session_state.adjustment_params
        adjusted_image_bytes, adjusted_image_format = apply_adjustments(
            original_image_bytes,
            current_params['brightness'],
            current_params['contrast'],
            current_params['rotation'],
            current_params['grayscale']
        )
        st.session_state.adjusted_image_bytes = adjusted_image_bytes
        st.session_state.adjusted_image_format = adjusted_image_format


# Display images
col1, col2 = st.columns(2)

with col1:
    st.subheader("Original Image")
    st.image(original_pil_image, caption=f"Original: {original_image_name}", use_column_width=True)

with col2:
    st.subheader("Adjusted Image")
    if adjusted_image_bytes:
        st.image(adjusted_image_bytes, caption="Adjusted Preview", use_column_width=True)

        # Prepare filename for download
        base, ext = os.path.splitext(original_image_name)
        # Use adjusted_image_format for the extension, which is PNG by default or after certain ops
        download_filename = f"{base}_adjusted.{adjusted_image_format.lower()}"

        st.download_button(
            label=f"Download Adjusted Image ({adjusted_image_format})",
            data=adjusted_image_bytes,
            file_name=download_filename,
            mime=f"image/{adjusted_image_format.lower()}",
            key="download_button"
        )
    else:
        st.info("Adjust parameters in the sidebar to see the modified image here.")

if st.sidebar.button("Reset Adjustments", key="reset_adjustments"):
    st.session_state.adjustment_params = {
        'brightness': 1.0,
        'contrast': 1.0,
        'rotation': 0,
        'grayscale': False
    }
    if 'adjusted_image_bytes' in st.session_state:
        del st.session_state['adjusted_image_bytes']
    if 'adjusted_image_format' in st.session_state:
        del st.session_state['adjusted_image_format']
    st.rerun()
