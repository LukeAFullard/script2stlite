import base64
import pandas as pd

def generate_html_report(history):
    """
    Generates a single HTML report string from the session history.
    """
    html = """
    <html>
    <head>
        <title>MannKenSen Analysis Report</title>
        <style>
            body { font-family: sans-serif; max-width: 900px; margin: 20px auto; color: #333; }
            h1 { color: #2c3e50; border-bottom: 2px solid #eee; padding-bottom: 10px; }
            h2 { color: #2980b9; margin-top: 40px; }
            .test-block { border: 1px solid #ddd; padding: 20px; border-radius: 5px; margin-bottom: 30px; background: #fafafa; }
            .stats-table { width: 100%; border-collapse: collapse; margin: 15px 0; }
            .stats-table th, .stats-table td { padding: 8px; border-bottom: 1px solid #ddd; text-align: left; }
            .stats-table th { background-color: #f1f1f1; }
            .img-container { text-align: center; margin-top: 20px; }
            img { max-width: 100%; border: 1px solid #ccc; }
            .error { color: red; }
            .meta { font-size: 0.9em; color: #666; margin-bottom: 10px; }
            .settings { font-size: 0.85em; color: #555; background: #eef; padding: 10px; border-radius: 4px; }
        </style>
    </head>
    <body>
        <h1>MannKenSen Analysis Report</h1>
        <p>Generated on: """ + pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
    """

    if not history:
        html += "<p>No tests run.</p></body></html>"
        return html

    for i, res in enumerate(history):
        test_type = res.get('test_type', 'Unknown Test')
        timestamp = res.get('timestamp', '')
        error = res.get('error', None)
        output = res.get('output', None)
        plot_bytes = res.get('plot_bytes', None)
        settings = res.get('settings', {})

        html += f"""
        <div class="test-block">
            <h2>{i+1}. {test_type}</h2>
            <div class="meta">Run at: {timestamp}</div>
        """

        # Settings Section
        html += "<div class='settings'><strong>Settings:</strong> "
        settings_str = ", ".join([f"{k}={v}" for k,v in settings.items()])
        html += settings_str + "</div>"

        if error:
            html += f"<p class='error'><strong>Error:</strong> {error}</p>"
        elif output:
            # Build stats table based on result type
            html += "<h3>Results</h3>"
            html += "<table class='stats-table'>"

            # Common fields for Trend/Seasonal
            if hasattr(output, 'trend'):
                # Trend Test Result
                html += f"""
                <tr><th>Trend Classification</th><td>{output.classification}</td></tr>
                <tr><th>P-value</th><td>{output.p:.4f}</td></tr>
                <tr><th>Sen's Slope</th><td>{output.scaled_slope:.4g} {output.slope_units}</td></tr>
                <tr><th>Kendall's Tau</th><td>{output.Tau:.4f}</td></tr>
                <tr><th>Mann-Kendall Score (S)</th><td>{output.s:.1f}</td></tr>
                <tr><th>Confidence (C)</th><td>{output.C:.4f}</td></tr>
                """
                if hasattr(output, 'analysis_notes') and output.analysis_notes:
                    html += f"<tr><th>Analysis Notes</th><td>{', '.join(output.analysis_notes)}</td></tr>"

            elif hasattr(output, 'is_seasonal'):
                # Seasonality Check Result
                status = "Seasonal" if output.is_seasonal else "Not Seasonal"
                html += f"""
                <tr><th>Result</th><td><strong>{status}</strong></td></tr>
                <tr><th>H-Statistic</th><td>{output.h_statistic:.4f}</td></tr>
                <tr><th>P-value</th><td>{output.p_value:.4f}</td></tr>
                """
                if output.seasons_skipped:
                    html += f"<tr><th>Skipped Seasons</th><td>{output.seasons_skipped}</td></tr>"

            html += "</table>"

            # Image embedding
            if plot_bytes:
                b64_img = base64.b64encode(plot_bytes).decode('utf-8')
                html += f"""
                <div class="img-container">
                    <img src="data:image/png;base64,{b64_img}" alt="Analysis Plot" />
                </div>
                """

        html += "</div>" # End test-block

    html += """
    </body>
    </html>
    """
    return html
