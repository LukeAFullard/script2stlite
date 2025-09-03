import streamlit as st
import shared_state

st.title("Control App")

if st.button("Increment Counter"):
    st.session_state.counter += 1

st.write(f"Current counter value: {st.session_state.counter}")
