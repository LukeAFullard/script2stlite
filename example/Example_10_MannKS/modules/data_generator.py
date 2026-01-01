import streamlit as st
import pandas as pd
import numpy as np
import datetime

def generate_synthetic_data(
    n_points,
    start_date,
    time_unit,
    slope,
    intercept,
    season_period,
    season_amplitude,
    noise_std,
    censor_threshold,
    censor_type,
    gap_fraction,
    seed
):
    """
    Generates synthetic time series data based on parameters.
    """
    np.random.seed(seed)

    # 1. Generate Time Vector
    # We'll create a base range and then maybe drop some
    # We use a base integer range first for calculation
    t_idx = np.arange(n_points)

    # 2. Calculate Trend Component
    # slope is "units per time_unit"
    # We need to map time_unit to our t_idx step
    # If we assume t_idx represents "1 unit of time_unit", it's simple:
    trend = intercept + (slope * t_idx)

    # 3. Calculate Seasonal Component
    # Simple Sinusoidal: A * sin(2 * pi * t / P)
    if season_amplitude > 0 and season_period > 0:
        seasonal = season_amplitude * np.sin(2 * np.pi * t_idx / season_period)
    else:
        seasonal = np.zeros(n_points)

    # 4. Noise
    noise = np.random.normal(0, noise_std, n_points)

    # 5. Combine
    y_raw = trend + seasonal + noise

    # 6. Apply Censoring
    # logic: if value < threshold, make it censored
    # We will construct the 'censored' and 'cen_type' columns directly
    censored = np.zeros(n_points, dtype=bool)
    cen_type = np.full(n_points, 'not', dtype=object)

    # We need to handle the values. For censored data, the value stored
    # is usually the detection limit.
    y_final = y_raw.copy()

    if censor_type == 'Left (<)':
        mask = y_raw < censor_threshold
        y_final[mask] = censor_threshold
        censored[mask] = True
        cen_type[mask] = 'lt'
    elif censor_type == 'Right (>)':
        mask = y_raw > censor_threshold
        y_final[mask] = censor_threshold
        censored[mask] = True
        cen_type[mask] = 'gt'

    # 7. Convert Time to Datetime or Numeric
    # If Start Date is provided, we create a DatetimeIndex
    if start_date is not None:
        # map unit string to pandas freq
        freq_map = {
            'Seconds': 's',
            'Minutes': 'min',
            'Hours': 'h',
            'Days': 'D',
            'Weeks': 'W',
            'Months': 'ME', # Month End
            'Years': 'YE'   # Year End
        }
        freq = freq_map.get(time_unit, 'D')
        t_final = pd.date_range(start=start_date, periods=n_points, freq=freq)
    else:
        t_final = t_idx

    # 8. Create DataFrame
    df = pd.DataFrame({
        't_original': t_final,
        'value': y_final,
        'censored': censored,
        'cen_type': cen_type,
        'true_value': y_raw # Keep true value for reference/debugging
    })

    # 9. Apply Gaps (Missing Data)
    if gap_fraction > 0:
        n_drop = int(n_points * gap_fraction)
        if n_drop > 0:
            drop_indices = np.random.choice(df.index, n_drop, replace=False)
            df = df.drop(drop_indices).sort_values(by='t_original').reset_index(drop=True)

    return df

def generate_data_ui():
    """
    Renders the Synthetic Data Generator UI and returns the generated DataFrame.
    """
    st.markdown("### Generate Synthetic Data")
    st.markdown("Create a custom dataset to test the analysis tools.")

    col1, col2, col3 = st.columns(3)

    with col1:
        n_points = st.number_input("Number of Points (N)", min_value=10, max_value=5000, value=100)
        time_unit = st.selectbox("Time Unit", ["Days", "Months", "Years", "Seconds", "Minutes", "Hours", "Weeks"])
        start_date = st.date_input("Start Date", value=datetime.date(2020, 1, 1))

    with col2:
        intercept = st.number_input("Base Value (Intercept)", value=10.0)
        slope = st.number_input("Trend Slope (units per time step)", value=0.1, format="%.4f")
        seed = st.number_input("Random Seed (Numpy)", value=42, step=1)

    with col3:
        noise_std = st.number_input("Noise (Std Dev)", value=1.0)
        gap_fraction = st.slider("Missing Data Fraction", 0.0, 0.9, 0.0)

    st.markdown("#### Seasonality")
    scol1, scol2 = st.columns(2)
    with scol1:
        season_period = st.number_input("Seasonal Period (steps)", min_value=0, value=12, help="0 to disable")
    with scol2:
        season_amplitude = st.number_input("Seasonal Amplitude", value=2.0)

    st.markdown("#### Censoring")
    ccol1, ccol2 = st.columns(2)
    with ccol1:
        censor_type = st.selectbox("Censoring Type", ["None", "Left (<)", "Right (>)"])
    with ccol2:
        censor_threshold = st.number_input("Detection Limit / Threshold", value=5.0)

    if st.button("Generate Data"):
        # Map "None" censor type to internal logic
        if censor_type == "None":
            # Pass a threshold that won't trigger (e.g., -inf for Left)
            # But simpler to just handle in logic.
            # We'll pass logic check inside the function, but for now lets just pass the input
            pass

        df = generate_synthetic_data(
            n_points, start_date, time_unit, slope, intercept,
            season_period, season_amplitude, noise_std,
            censor_threshold, censor_type, gap_fraction, seed
        )

        st.success("Data generated successfully!")
        st.write(f"Generated {len(df)} points.")
        st.dataframe(df.head())

        # Simple plot preview
        st.line_chart(df.set_index('t_original')['value'])

        return df

    return None
