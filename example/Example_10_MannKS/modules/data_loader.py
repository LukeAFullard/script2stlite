import streamlit as st
import pandas as pd
import numpy as np
from io import StringIO
from MannKS.preprocessing import prepare_censored_data

def read_file(uploaded_file):
    """
    Reads an uploaded file (CSV or Excel) into a pandas DataFrame.
    """
    if uploaded_file.name.endswith('.csv'):
        return pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith(('.xls', '.xlsx')):
        return pd.read_excel(uploaded_file)
    else:
        st.error("Unsupported file format. Please upload a CSV or Excel file.")
        return None

def process_input_data(df, value_col, time_col, censored_col=None, censored_flag_col=None):
    """
    Normalizes the input DataFrame into the format required by MannKS.
    Returns a DataFrame with columns: ['t_original', 'value', 'censored', 'cen_type']
    """
    try:
        # 1. Handle Time
        # Try to convert to datetime first
        try:
            t_original = pd.to_datetime(df[time_col])
        except Exception:
            # If numeric, keep as is
            t_original = df[time_col]

        # 2. Handle Values and Censoring
        if censored_col:
            # Case A: Single column with combined strings (e.g., "<5", "10")
            # prepare_censored_data expects a 1D array/series
            processed_values = prepare_censored_data(df[censored_col].values)

            # If the user also selected a separate value column, we might want to warn or just use the processed one.
            # Assuming if they picked a censored_col (string), that's the source of truth.

        elif censored_flag_col:
            # Case B: Separate Value and Flag columns
            # We need to construct the censoring logic manually to match MannKS format
            vals = pd.to_numeric(df[value_col], errors='coerce')

            # Inspect flag column to guess format (True/False, 1/0, "Yes"/"No", "<")
            flags = df[censored_flag_col]

            # Simple heuristic: treat truthy values as censored
            # For robustness, we'll assume standard boolean-like or specific strings
            is_censored = flags.apply(lambda x: str(x).lower() in ['true', '1', 'yes', 'censored', '<', 'lt'])

            # Create cen_type (assuming left censoring by default for now, could be improved)
            cen_type = np.where(is_censored, 'lt', 'not')

            processed_values = pd.DataFrame({
                'value': vals,
                'censored': is_censored,
                'cen_type': cen_type
            })

        else:
            # Case C: Plain values, no censoring
            vals = pd.to_numeric(df[value_col], errors='coerce')
            processed_values = pd.DataFrame({
                'value': vals,
                'censored': np.zeros(len(vals), dtype=bool),
                'cen_type': np.full(len(vals), 'not')
            })

        # Combine
        final_df = processed_values.copy()
        final_df['t_original'] = t_original.values

        # Sort by time
        final_df = final_df.sort_values(by='t_original').reset_index(drop=True)

        return final_df

    except Exception as e:
        st.error(f"Error processing data: {str(e)}")
        return None

def load_data_ui():
    """
    Renders the File Upload UI and returns the processed DataFrame.
    """
    st.markdown("### Upload Data")
    st.markdown("Upload a CSV or Excel file. Your data should be in long format (one row per observation).")

    uploaded_file = st.file_uploader("Choose a file", type=['csv', 'xlsx', 'xls'])

    if uploaded_file is not None:
        df = read_file(uploaded_file)

        if df is not None:
            st.write("Preview of raw data:", df.head())

            st.markdown("#### Map Columns")
            cols = df.columns.tolist()

            col1, col2 = st.columns(2)
            with col1:
                time_col = st.selectbox("Select Time Column", options=cols)
            with col2:
                # User can either select a 'Value' column OR a 'Censored String' column
                # We'll offer a mode switch
                input_mode = st.radio("Data Format", ["Numeric Value Column", "Combined String Column (e.g. '<0.5')"], horizontal=True)

            censored_col = None
            censored_flag_col = None
            value_col = None

            if input_mode == "Combined String Column (e.g. '<0.5')":
                censored_col = st.selectbox("Select Column with Values (including censored strings)", options=cols)
                value_col = censored_col # Placeholder, logic uses censored_col
            else:
                value_col = st.selectbox("Select Value Column", options=cols)
                has_flag = st.checkbox("I have a separate Censored Flag column")
                if has_flag:
                    censored_flag_col = st.selectbox("Select Censored Flag Column", options=cols)

            if st.button("Process Data"):
                processed_df = process_input_data(df, value_col, time_col, censored_col, censored_flag_col)
                if processed_df is not None:
                    st.success("Data processed successfully!")
                    st.write("Preview of processed data for analysis:", processed_df.head())
                    # Return or Store in session state?
                    # Better to return, let main handle storage
                    return processed_df

    return None
