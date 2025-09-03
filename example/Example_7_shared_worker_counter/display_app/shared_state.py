import streamlit as st

# This is a basic way to share state.
# For more complex apps, you might want to use a more robust solution.
if 'counter' not in st.session_state:
    st.session_state.counter = 0
