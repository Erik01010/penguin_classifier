from dash import Dash
import dash_bootstrap_components as dbc
import os
import webbrowser
from threading import Timer

from src.penguin_classifier.ui.layout import create_layout

# noinspection PyUnusedImports
import src.penguin_classifier.ui.callbacks

def open_browser():
    webbrowser.open_new("http://127.0.0.1:8050/")

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.title = "Penguin Classifier"
app.layout = create_layout()

server = app.server


if __name__ == "__main__":
    if os.environ.get("WERKZEUG_RUN_MAIN") is None:
        Timer(interval=2, function=open_browser).start()
    app.run(debug=True, port=8050)
