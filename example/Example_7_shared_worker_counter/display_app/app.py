import streamlit as st
from shared_state import st
import time

st.title("Display App")

st.write("This app displays the counter value from the Control App.")

placeholder = st.empty()

while True:
    with placeholder.container():
        st.write(f"Current counter value: {st.session_state.counter}")
    time.sleep(1)
