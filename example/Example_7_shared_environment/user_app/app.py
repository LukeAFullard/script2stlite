import streamlit as st
import asyncio

st.title("User App")

st.write(
    "This app can use the `mpmath` package because the 'Installer App' includes it "
    "in its requirements, and both apps are running in a shared environment."
)

st.write(
    "However, due to a potential race condition where this app may start before the "
    "other app has finished installing the package, a retry mechanism has been added."
)

st.write("Click the button below to test the import and usage.")

if st.button("Use `mpmath` package"):
    package_name = "mpmath"
    max_retries = 5
    retry_delay = 2  # seconds

    for attempt in range(max_retries):
        try:
            # Try to import the package
            __import__(package_name)

            # If successful, import it properly and use it
            import mpmath
            st.success(f"Successfully imported `{package_name}` on attempt {attempt + 1}!")
            result = mpmath.fadd(5, 3)
            st.write(f"The result of `mpmath.fadd(5, 3)` is: **{result}**")

            # Exit the loop on success
            break

        except ImportError:
            if attempt < max_retries - 1:
                st.info(f"Attempt {attempt + 1}: Failed to import `{package_name}`. Retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
            else:
                st.error(
                    f"Failed to import `{package_name}` after {max_retries} attempts. "
                    "Please ensure the 'Installer App' is running and has `mpmath` "
                    "in its `settings.yaml` requirements."
                )
