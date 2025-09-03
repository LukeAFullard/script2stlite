import streamlit as st

st.title("User App")
st.write("This app attempts to use the `tiny-math` package.")

st.info("First, go to the Installer App and click the install button. Then, come back here and click the button below.")

if st.button("Try to use `tiny-math`"):
    try:
        import tiny_math
        st.success("Successfully imported `tiny-math`!")
        result = tiny_math.add(5, 3)
        st.write(f"The result of `tiny_math.add(5, 3)` is: **{result}**")
    except ImportError:
        st.error("Failed to import `tiny-math`. Please make sure you have installed it in the Installer App.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
