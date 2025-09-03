import streamlit as st

st.title("User App")

st.write(
    "This app can use the `mpmath` package because the 'Installer App' includes it "
    "in its requirements, and both apps are running in a shared environment."
)

st.write("Click the button below to test the import and usage.")

if st.button("Use `mpmath` package"):
    try:
        import mpmath
        st.success("Successfully imported `mpmath`!")
        result = mpmath.fadd(5, 3)
        st.write(f"The result of `mpmath.fadd(5, 3)` is: **{result}**")
    except ImportError:
        st.error(
            "Failed to import `mpmath`. Make sure the 'Installer App' has `mpmath` "
            "in its `settings.yaml` requirements."
        )
    except Exception as e:
        st.error(f"An error occurred: {e}")
