import streamlit as st
import pandas as pd
from modules.data_loader import load_data_ui
from modules.data_generator import generate_data_ui
from modules.settings import render_settings_ui
from modules.analysis import run_analysis
from modules.reporting import generate_html_report

# Set page config
st.set_page_config(page_title="MannKenSen Analysis App", layout="wide", page_icon="📈")

def inject_custom_css():
    """Inject modern, sleek CSS into the Streamlit app"""
    st.markdown("""
    <style>
    /* ============================================
       GLOBAL STYLES
       ============================================ */

    /* Main app container */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%);
    }

    /* Headers */
    h1, h2, h3 {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        font-weight: 600;
        letter-spacing: -0.02em;
    }

    h1 {
        color: #1a1a1a;
        font-size: 2.5rem !important;
        margin-bottom: 1.5rem;
    }

    h2 {
        color: #2c3e50;
        font-size: 1.8rem !important;
        margin-top: 2rem;
    }

    h3 {
        color: #34495e;
        font-size: 1.4rem !important;
    }

    /* ============================================
       TAB STYLING - PROMINENT & MODERN
       ============================================ */

    /* Tab container */
    .stTabs {
        background: white;
        border-radius: 16px;
        padding: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        margin: 2rem 0;
    }

    /* Tab list (container for all tabs) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #f8f9fa;
        border-radius: 12px;
        padding: 6px;
    }

    /* Individual tab buttons */
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        padding: 0 32px;
        background: transparent;
        border: none;
        border-radius: 10px;
        font-size: 16px;
        font-weight: 600;
        color: #64748b;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        letter-spacing: 0.01em;
    }

    /* Tab hover effect */
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(59, 130, 246, 0.08);
        color: #3b82f6;
        transform: translateY(-2px);
    }

    /* Active tab */
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }

    /* Active tab hover (maintain style) */
    .stTabs [aria-selected="true"]:hover {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        transform: translateY(-2px);
    }

    /* Tab content panel */
    .stTabs [data-baseweb="tab-panel"] {
        padding: 2rem 1rem;
    }

    /* ============================================
       BUTTONS
       ============================================ */

    /* Primary buttons */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-size: 16px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }

    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }

    /* Secondary buttons */
    .stButton > button {
        background: white;
        color: #667eea;
        border: 2px solid #667eea;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-size: 16px;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        background: #667eea;
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
    }

    /* ============================================
       CARDS & CONTAINERS
       ============================================ */

    /* Info boxes */
    .stAlert {
        border-radius: 12px;
        border: none;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
    }

    /* Expander */
    .streamlit-expanderHeader {
        background: white;
        border-radius: 12px;
        border: 2px solid #e5e7eb;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .streamlit-expanderHeader:hover {
        border-color: #667eea;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.1);
    }

    /* ============================================
       INPUTS
       ============================================ */

    /* Text inputs, number inputs */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        border-radius: 8px;
        border: 2px solid #e5e7eb;
        transition: all 0.3s ease;
    }

    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }

    /* Select boxes */
    .stSelectbox > div > div {
        border-radius: 8px;
    }

    /* Radio buttons */
    .stRadio > div {
        background: white;
        padding: 1rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }

    /* ============================================
       DATAFRAMES
       ============================================ */

    .dataframe {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
    }

    /* ============================================
       SIDEBAR
       ============================================ */

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }

    [data-testid="stSidebar"] .element-container {
        color: white;
    }

    /* Sidebar text */
    [data-testid="stSidebar"] .stMarkdown {
        color: white;
    }

    /* ============================================
       METRICS
       ============================================ */

    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #1a1a1a;
    }

    [data-testid="stMetricLabel"] {
        font-size: 1rem;
        font-weight: 600;
        color: #64748b;
    }

    /* ============================================
       DOWNLOAD BUTTON
       ============================================ */

    .stDownloadButton > button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-size: 16px;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
        transition: all 0.3s ease;
    }

    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4);
    }

    /* ============================================
       ANIMATIONS
       ============================================ */

    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .element-container {
        animation: fadeIn 0.5s ease-out;
    }

    /* ============================================
       SPINNER
       ============================================ */

    .stSpinner > div {
        border-top-color: #667eea !important;
    }

    /* ============================================
       RESPONSIVE ADJUSTMENTS
       ============================================ */

    @media (max-width: 768px) {
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            padding: 0 20px;
            font-size: 14px;
        }

        h1 {
            font-size: 2rem !important;
        }
    }

    </style>
    """, unsafe_allow_html=True)

inject_custom_css()

LOGO_URL = "https://raw.githubusercontent.com/LukeAFullard/MannKS/main/assets/logo.png"

def main():
    # Sidebar Logo
    st.sidebar.image(LOGO_URL, use_container_width=True)
    st.sidebar.markdown("---")

    col1, col2 = st.columns([1, 5])
    with col1:
        st.image(LOGO_URL, width=100)
    with col2:
        st.title("MannKenSen Analysis Tool")
        st.markdown("""
        Perform robust non-parametric trend analysis on unequally spaced time series with censored data.
        """)

    # Initialize Session State
    if 'data' not in st.session_state:
        st.session_state.data = None
    if 'history' not in st.session_state:
        st.session_state.history = []

    # --- Tabs ---
    tab_data, tab_settings, tab_run, tab_results = st.tabs([
        "1. Data", "2. Configure Settings", "3. Run Analysis", "4. Results & Report"
    ])

    # --- 1. Data Tab ---
    with tab_data:
        data_source = st.radio("Choose Data Source", ["Upload File", "Generate Synthetic Data"], horizontal=True)

        if data_source == "Upload File":
            df = load_data_ui()
        else:
            df = generate_data_ui()

        if df is not None:
            st.session_state.data = df

        if st.session_state.data is not None:
            st.info(f"Current Data: {len(st.session_state.data)} observations loaded.")
            with st.expander("View Data"):
                st.dataframe(st.session_state.data)

    # --- 2. Settings Tab ---
    with tab_settings:
        # Returns a dict of settings for all tests
        all_settings = render_settings_ui()
        st.session_state.settings = all_settings

    # --- 3. Run Analysis Tab ---
    with tab_run:
        st.header("Execute Analysis")

        if st.session_state.data is None:
            st.warning("Please load or generate data in the 'Data' tab first.")
        else:
            test_type = st.radio("Select Test to Run", ["Trend Test", "Seasonal Trend Test", "Seasonality Check"])

            # Show preview of settings for selected test
            if 'settings' in st.session_state:
                current_settings = st.session_state.settings.get(test_type.lower().replace(" ", "_"), {})
                st.markdown(f"**Current Settings for {test_type}:**")
                st.json(current_settings)

            if st.button("Run Analysis", type="primary"):
                with st.spinner("Running analysis..."):
                    # Get settings for this specific test
                    # keys in settings.py were: 'trend_test', 'seasonal_trend_test', 'check_seasonality'
                    key_map = {
                        "Trend Test": "trend_test",
                        "Seasonal Trend Test": "seasonal_trend_test",
                        "Seasonality Check": "check_seasonality"
                    }
                    settings_key = key_map[test_type]
                    params = st.session_state.settings.get(settings_key, {})

                    # Run
                    result = run_analysis(st.session_state.data, test_type, params)

                    # Store in history
                    st.session_state.history.append(result)

                    st.success("Analysis complete! Go to the 'Results & Report' tab to view details.")

    # --- 4. Results & Report Tab ---
    with tab_results:
        st.header("Analysis History")

        if not st.session_state.history:
            st.info("No analysis run yet.")
        else:
            # Report Download Button
            report_html = generate_html_report(st.session_state.history)
            st.download_button(
                label="Download Full HTML Report",
                data=report_html,
                file_name="mannkensen_report.html",
                mime="text/html"
            )

            st.markdown("---")

            # Display History (Reverse order to show newest first)
            for i, res in enumerate(reversed(st.session_state.history)):
                idx = len(st.session_state.history) - i
                with st.expander(f"Run {idx}: {res['test_type']} ({res['timestamp']})", expanded=(i==0)):

                    if res.get('error'):
                        st.error(f"Error: {res['error']}")
                        if 'traceback' in res:
                            st.code(res['traceback'])
                    else:
                        output = res['output']

                        col1, col2 = st.columns([1, 2])

                        with col1:
                            st.subheader("Statistics")
                            if hasattr(output, 'trend'): # Trend / Seasonal Trend
                                st.metric("Trend", output.classification)
                                st.write(f"**P-value:** {output.p:.4f}")
                                st.write(f"**Slope:** {output.scaled_slope:.4g} {output.slope_units}")
                                st.write(f"**Kendall's Tau:** {output.Tau:.4f}")
                                st.write(f"**Confidence:** {output.C:.4f}")
                                if output.analysis_notes:
                                    st.warning(f"Notes: {', '.join(output.analysis_notes)}")

                            elif hasattr(output, 'is_seasonal'): # Seasonality Check
                                st.metric("Seasonal?", "Yes" if output.is_seasonal else "No")
                                st.write(f"**H-Statistic:** {output.h_statistic:.4f}")
                                st.write(f"**P-value:** {output.p_value:.4f}")

                        with col2:
                            if res.get('plot_bytes'):
                                st.image(res['plot_bytes'], use_container_width=True)

            if st.button("Clear History"):
                st.session_state.history = []
                st.rerun()

if __name__ == "__main__":
    main()
