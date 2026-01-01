import streamlit as st

def render_settings_ui():
    """
    Renders the configuration tabs for the analysis tools and returns a dictionary
    containing the settings for each test.
    """
    st.markdown("### Analysis Configuration")
    st.markdown("Configure the parameters for the statistical tests.")

    # Initialize settings dictionary
    settings = {}

    # Create tabs for the three main tools
    tab1, tab2, tab3 = st.tabs(["Trend Test", "Seasonal Trend Test", "Seasonality Check"])

    # --- Tab 1: Trend Test ---
    with tab1:
        st.markdown("**Mann-Kendall Trend Test Settings**")

        # We need to namespace these keys so they don't conflict across tabs if we used same keys
        # But we can just build the dict directly.

        tt_alpha = st.number_input("Significance Level (alpha)", 0.001, 0.5, 0.05, key='tt_alpha',
                                   help="The probability of rejecting the null hypothesis when it is true.")

        col1, col2 = st.columns(2)
        with col1:
            tt_mk_method = st.selectbox("MK Test Method", ["robust", "lwp"], key='tt_mk_method',
                                        help="'robust' handles right-censored data without modification. 'lwp' uses a heuristic replacement.")
            tt_sens_method = st.selectbox("Sen's Slope Method", ["nan", "lwp", "ats"], key='tt_sens_method',
                                          help="Method for handling ambiguous slopes in censored data. 'ats' is most robust but slower.")

        with col2:
            tt_ci_method = st.selectbox("Confidence Interval Method", ["direct", "lwp"], key='tt_ci_method',
                                        help="'direct' uses rank rounding, 'lwp' uses interpolation.")
            tt_tau_method = st.selectbox("Kendall's Tau Method", ["b", "a"], key='tt_tau_method',
                                         help="'b' adjusts for ties (recommended).")

        st.markdown("---")
        st.markdown(" **Aggregation Settings** (Optional)")

        col3, col4 = st.columns(2)
        with col3:
            tt_agg_method = st.selectbox("Aggregation Method",
                                         ['none', 'median', 'robust_median', 'middle', 'middle_lwp', 'lwp', 'lwp_median', 'lwp_robust_median'],
                                         key='tt_agg_method',
                                         help="Method to aggregate data before analysis. 'none' is default.")
        with col4:
            tt_agg_period = st.text_input("Aggregation Period", value="", key='tt_agg_period',
                                          help="e.g. 'year', 'month'. Required if using LWP aggregation methods on datetime data.")
            if tt_agg_period.strip() == "":
                tt_agg_period = None

        st.markdown("---")
        st.markdown("**Scaling**")
        tt_slope_scaling = st.selectbox("Scale Slope To:", ["None", "year", "month", "day"], key='tt_slope_scaling',
                                        help="Convert the slope unit (e.g. per second) to a human readable unit.")
        if tt_slope_scaling == "None":
            tt_slope_scaling = None

        settings['trend_test'] = {
            'alpha': tt_alpha,
            'mk_test_method': tt_mk_method,
            'sens_slope_method': tt_sens_method,
            'ci_method': tt_ci_method,
            'tau_method': tt_tau_method,
            'agg_method': tt_agg_method,
            'agg_period': tt_agg_period,
            'slope_scaling': tt_slope_scaling
        }

    # --- Tab 2: Seasonal Trend Test ---
    with tab2:
        st.markdown("**Seasonal Mann-Kendall Test Settings**")

        st_alpha = st.number_input("Significance Level (alpha)", 0.001, 0.5, 0.05, key='st_alpha')
        st_period = st.number_input("Seasonal Period (Cycles)", min_value=2, value=12, key='st_period',
                                    help="Number of seasons in a full cycle (e.g., 12 for months).")

        col1, col2 = st.columns(2)
        with col1:
            st_season_type = st.selectbox("Season Type",
                                          ['month', 'quarter', 'day_of_week', 'week_of_year', 'day_of_year', 'hour', 'minute', 'second', 'year'],
                                          key='st_season_type')
            st_mk_method = st.selectbox("MK Test Method", ["robust", "lwp"], key='st_mk_method')

        with col2:
            st_sens_method = st.selectbox("Sen's Slope Method", ["nan", "lwp", "ats"], key='st_sens_method')
            st_ci_method = st.selectbox("Confidence Interval Method", ["direct", "lwp"], key='st_ci_method')

        st.markdown("---")
        st.markdown("**Aggregation Settings**")

        col3, col4 = st.columns(2)
        with col3:
            st_agg_method = st.selectbox("Aggregation Method",
                                         ['none', 'median', 'robust_median', 'middle', 'middle_lwp', 'lwp'],
                                         key='st_agg_method')
        with col4:
            # Added Aggregation Period for Seasonal Trend Test
            st_agg_period = st.text_input("Aggregation Period", value="", key='st_agg_period',
                                          help="Time unit to aggregate by (e.g. 'month') if using an aggregation method.")
            if st_agg_period.strip() == "":
                st_agg_period = None

        st.markdown("---")
        st.markdown("**Scaling**")
        st_slope_scaling = st.selectbox("Scale Slope To:", ["None", "year", "month", "day"], key='st_slope_scaling')
        if st_slope_scaling == "None":
            st_slope_scaling = None

        settings['seasonal_trend_test'] = {
            'alpha': st_alpha,
            'period': st_period,
            'season_type': st_season_type,
            'mk_test_method': st_mk_method,
            'sens_slope_method': st_sens_method,
            'ci_method': st_ci_method,
            'agg_method': st_agg_method,
            'agg_period': st_agg_period,
            'slope_scaling': st_slope_scaling,
            'tau_method': 'b' # Defaulting to b for simplicity in UI, could add if needed
        }

    # --- Tab 3: Seasonality Check ---
    with tab3:
        st.markdown("**Seasonality Check (Kruskal-Wallis) Settings**")

        sc_alpha = st.number_input("Significance Level (alpha)", 0.001, 0.5, 0.05, key='sc_alpha')
        sc_period = st.number_input("Seasonal Period (Cycles)", min_value=2, value=12, key='sc_period')
        sc_season_type = st.selectbox("Season Type",
                                      ['month', 'quarter', 'day_of_week', 'week_of_year', 'day_of_year', 'hour', 'minute', 'second'],
                                      key='sc_season_type')

        st.markdown("---")
        st.markdown("**Aggregation Settings**")
        st.info("It is recommended to use the same aggregation method here as in the Seasonal Trend Test.")

        sc_agg_method = st.selectbox("Aggregation Method",
                                     ['none', 'median', 'robust_median', 'middle', 'middle_lwp'],
                                     key='sc_agg_method')

        sc_agg_period = st.text_input("Aggregation Period", value="month", key='sc_agg_period',
                                      help="Time unit to aggregate by (e.g. 'month'). Required if agg_method is not 'none'.")
        if sc_agg_method != 'none' and sc_agg_period.strip() == "":
            st.warning("Aggregation Period is required when Aggregation Method is not 'none'.")
            sc_agg_period = None
        elif sc_agg_method == 'none':
            sc_agg_period = None

        settings['check_seasonality'] = {
            'alpha': sc_alpha,
            'period': sc_period,
            'season_type': sc_season_type,
            'agg_method': sc_agg_method,
            'agg_period': sc_agg_period
        }

    return settings
