# Streamlit Echarts Demo

This example demonstrates the conversion of a more complex Streamlit application, "Streamlit Echarts Demo," to a static web page using `script2stlite`.

This application showcases various interactive charts and visualizations powered by the Echarts library, seamlessly integrated with Streamlit.

## Original Author

This application was originally created by Fanilo Andrianasolo. You can find the original repository and more of their work here:
[https://github.com/andfanilo/streamlit-echarts-demo](https://github.com/andfanilo/streamlit-echarts-demo)

## Live Demos

*   **Original Streamlit App:** [https://echarts.streamlit.app/](https://echarts.streamlit.app/)
*   **script2stlite HTML Version:** [https://lukeafullard.github.io/script2stlite/example/Example_4_echarts_demo/Streamlit_echarts_demo.html](https://lukeafullard.github.io/script2stlite/example/Example_4_echarts_demo/Streamlit_echarts_demo.html)

## `settings.yaml`

The `settings.yaml` file for this example is configured as follows:

```yaml
APP_NAME: "Streamlit echarts demo"  #give your app a nice name
APP_REQUIREMENTS: #app requirements separated by a '-' on each new line. Requirements MUST be compatible with pyodide. Suggest specifying versions.
  - streamlit
  - streamlit-echarts>=0.4.0
APP_ENTRYPOINT: app.py #entrypoint to app - change this to your main python file
CONFIG: false
APP_FILES:  #each file separated by a '-'. Can be .py files or other filetypes that will be converted to binary and embeded in the html.
  - data/countries.geo.json
  - data/disk.tree.json
  - data/drink-flavors.json
  - data/flare.json
  - data/les-miserables.json
  - data/life-expectancy-table.json
  - data/product.json
  - data/USA.json
  - demo_echarts/bar.py
  - demo_echarts/boxplot.py
  - demo_echarts/calendar.py
  - demo_echarts/candlestick.py
  - demo_echarts/dataset.py
  - demo_echarts/events.py
  - demo_echarts/extensions.py
  - demo_echarts/funnel.py
  - demo_echarts/gauge.py
  - demo_echarts/graph.py
  - demo_echarts/heatmap.py
  - demo_echarts/__init__.py
  - demo_echarts/line.py
  - demo_echarts/map.py
  - demo_echarts/parallel.py
  - demo_echarts/pictorial_bar.py
  - demo_echarts/pie.py
  - demo_echarts/radar.py
  - demo_echarts/sankey.py
  - demo_echarts/scatter.py
  - demo_echarts/sunburst.py
  - demo_echarts/themeriver.py
  - demo_echarts/tree.py
  - demo_echarts/treemap.py
  - demo_pyecharts/bar.py
  - demo_pyecharts/graph.py
  - demo_pyecharts/__init__.py
  - demo_pyecharts/line.py
  - demo_pyecharts/map.py
  - demo_pyecharts/pie.py
```

This README provides an overview of the "Streamlit Echarts Demo" example and its conversion using `script2stlite`. For more details on `script2stlite` and its usage, please refer to the main project documentation.
