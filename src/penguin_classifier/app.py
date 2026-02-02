from dash import Dash
import dash_bootstrap_components as dbc
from ui.layout import create_layout
import src.penguin_classifier.ui.callbacks

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.title = "Penguin Classifier"
app.layout = create_layout()

server = app.server


if __name__ == "__main__":
    app.run(debug=True)
