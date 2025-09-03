import streamlit as st
import shared_state
import asyncio

st.title("Display App")

st.write("This app displays the counter value from the Control App.")

placeholder = st.empty()

async def watch_counter():
    while True:
        with placeholder.container():
            st.write(f"Current counter value: {st.session_state.counter}")
        await asyncio.sleep(1)

# stlite supports top-level await
await watch_counter()
