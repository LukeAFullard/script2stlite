import streamlit as st
import micropip

st.title("Installer App")
st.write("This app installs the `tiny-math` package.")

async def install_package():
    st.write("Installing `tiny-math`...")
    await micropip.install('tiny-math')
    st.write("`tiny-math` installed successfully!")
    st.write("Now you can use it in the User App.")

# Using a button to trigger the installation
if st.button("Install `tiny-math` package"):
    await install_package()

st.info("After clicking the install button, go to the User App to see the effect.")
