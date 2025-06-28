import streamlit as st
from functions import random_pandas_dataframe

#say something
st.write("This text is from home.py")

#get a dataframe
st.write("The dataframe below is from functions.py")
df = random_pandas_dataframe()
st.write(df)

#show an image
st.write("The image below in in the assets folder, but is embeded into the html file.")
st.image("assets/image.jpg")

