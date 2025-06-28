import streamlit as st
from functions import random_pandas_dataframe

#say something
st.write("This is from home.py")

#get a dataframe
df = random_pandas_dataframe()
st.write(df)

#show an image
st.image("/assets/image.jpg")

