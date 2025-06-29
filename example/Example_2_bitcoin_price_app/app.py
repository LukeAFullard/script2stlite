import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

# Define the API URL
API_URL = "https://min-api.cryptocompare.com/data/v2/histoday?fsym=BTC&tsym=USD&limit=30"

st.title("Bitcoin Price Viewer")

st.image("assets/image.png")

if st.button("Get Latest Bitcoin Price"):
    try:
        response = requests.get(API_URL)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()

        if data["Response"] == "Success":
            btc_data = data["Data"]["Data"]

            # Convert to DataFrame for easier manipulation and plotting
            df = pd.DataFrame(btc_data)

            # Convert UNIX timestamp to datetime
            df["time"] = pd.to_datetime(df["time"], unit="s")

            st.subheader("Bitcoin Price Data (Last 30 Days)")
            st.dataframe(df[["time", "open", "high", "low", "close", "volumefrom", "volumeto"]])

            # Create the plot
            fig = px.line(df, x="time", y="close", title="Bitcoin Closing Price (USD)")
            fig.update_xaxes(title_text='Date')
            fig.update_yaxes(title_text='Price (USD)')
            st.plotly_chart(fig)

        else:
            st.error(f"Error fetching data: {data.get('Message', 'Unknown error')}")

    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {e}")
    except KeyError as e:
        st.error(f"Unexpected data format from API: Missing key {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
