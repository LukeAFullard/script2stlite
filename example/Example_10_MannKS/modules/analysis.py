import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import tempfile
import os

# Import MannKenSen functions
from MannKS.trend_test import trend_test
from MannKS.seasonal_trend_test import seasonal_trend_test
from MannKS.check_seasonality import check_seasonality
from MannKS.plotting import plot_seasonal_distribution

def get_plot_as_image(fig):
    """
    Converts a matplotlib figure to a PIL Image or Base64 string.
    Here we return BytesIO to display in st.image or save later.
    """
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight')
    buf.seek(0)
    return buf

def run_analysis(data_df, test_type, settings):
    """
    Runs the specified test on the data using the provided settings.
    Returns a result dictionary containing the test output and plot.
    """
    # Prepare inputs from data_df
    # MannKS expects x (value vector or DF with censored cols) and t (time vector)
    # Our data_df is standardized: ['t_original', 'value', 'censored', 'cen_type']

    if data_df is None or len(data_df) == 0:
        return {"error": "No data available."}

    x_input = data_df[['value', 'censored', 'cen_type']]
    t_input = data_df['t_original'].values

    results = {}
    results['test_type'] = test_type
    results['timestamp'] = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    results['settings'] = settings

    # Secure temporary file creation helper
    def create_temp_plot_file():
        tf = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        tf.close()
        return tf.name

    try:
        if test_type == "Trend Test":
            plot_filename = create_temp_plot_file()

            # Run Test
            params = settings.copy()
            test_res = trend_test(x_input, t_input, plot_path=plot_filename, **params)

            results['output'] = test_res
            results['plot_path'] = plot_filename

            # Read plot back into memory
            if os.path.exists(plot_filename):
                with open(plot_filename, "rb") as f:
                    results['plot_bytes'] = f.read()
                os.remove(plot_filename)
            else:
                results['plot_bytes'] = None

        elif test_type == "Seasonal Trend Test":
            plot_filename = create_temp_plot_file()

            params = settings.copy()
            test_res = seasonal_trend_test(x_input, t_input, plot_path=plot_filename, **params)

            results['output'] = test_res
            results['plot_path'] = plot_filename

            if os.path.exists(plot_filename):
                with open(plot_filename, "rb") as f:
                    results['plot_bytes'] = f.read()
                os.remove(plot_filename)
            else:
                results['plot_bytes'] = None

        elif test_type == "Seasonality Check":
            params = settings.copy()
            test_res = check_seasonality(x_input, t_input, **params)
            results['output'] = test_res

            # Generate Plot manually
            plot_filename = create_temp_plot_file()

            plot_kwargs = {
                'x': x_input,
                't': t_input,
                'period': params.get('period', 12),
                'season_type': params.get('season_type', 'month'),
                'plot_path': plot_filename,
                'agg_method': params.get('agg_method', 'none')
            }
            # Only add agg_period if it exists in settings
            if 'agg_period' in params:
                 plot_kwargs['agg_period'] = params['agg_period']

            plot_seasonal_distribution(**plot_kwargs)

            if os.path.exists(plot_filename):
                with open(plot_filename, "rb") as f:
                    results['plot_bytes'] = f.read()
                os.remove(plot_filename)
            else:
                results['plot_bytes'] = None

    except Exception as e:
        results['error'] = str(e)
        import traceback
        results['traceback'] = traceback.format_exc()

    return results
