import json
from typing import Literal

from dash import dcc, html
from dash.development.base_component import Component
import dash_bootstrap_components as dbc

from src.penguin_classifier.config import (
    FEATURE_CONSTRAINTS,
    FEATURES,
    ISLAND_OPTIONS,
    METRICS_PATH,
    OFFSET,
    SEX_OPTIONS,
)

FIELD_LABELS = {
    "island": "Island Location",
    "bill_length_mm": "Bill Length (mm)",
    "bill_depth_mm": "Bill Depth (mm)",
    "flipper_length_mm": "Flipper Length (mm)",
    "body_mass_g": "Body Mass (g)",
    "sex": "Sex",
}

PLACEHOLDERS = {
    "island": "e.g. Torgersen",
    "bill_length_mm": "e.g. 38.5",
    "bill_depth_mm": "e.g. 18.1",
    "flipper_length_mm": "e.g. 180.0",
    "body_mass_g": "e.g. 3750.0",
    "sex": "female",
}


def _create_performance_card() -> dbc.Card:
    """Load metrics and create performance card."""
    try:
        with open(METRICS_PATH, "r") as f:
            report = json.load(f)

        accuracy = report.get("accuracy", 0)
        macro_avg = report.get("macro avg", {})

        acc_text = f"{accuracy:.1%}"
        f1_text = f"{macro_avg.get('f1-score', 0):.1%}"
        precision_text = f"{macro_avg.get('precision', 0):.1%}"
        recall_text = f"{macro_avg.get('recall', 0):.1%}"

        content = [
            html.H5("Model-Performance", className="card-title"),
            html.P(
                "The model was trained on historic data",
                className="card-text text-muted small",
            ),
            html.Hr(),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H2(acc_text, className="text-primary"),
                            html.Small("Accuracy"),
                        ],
                        width=3,
                        xs=6,
                    ),
                    dbc.Col(
                        [
                            html.H2(precision_text, className="text-info"),
                            html.Small("Precision"),
                        ],
                        width=3,
                        xs=6,
                    ),
                    dbc.Col(
                        [
                            html.H2(recall_text, className="text-info"),
                            html.Small("Recall"),
                        ],
                        width=3,
                        xs=6,
                    ),
                    dbc.Col(
                        [
                            html.H2(f1_text, className="text-info"),
                            html.Small("F1-Score"),
                        ],
                        width=3,
                        xs=6,
                    ),
                ],
                className="text-center",
            ),
        ]
    except FileNotFoundError:
        content = [
            html.H5("Model-Performance", className="card-title"),
            dbc.Alert(
                "No metrics found. Please train model.",
                color="warning",
            ),
        ]

    return dbc.Card(
        dbc.CardBody(content), className="shadow-sm border-1 h-100"
    )


def _create_select(
    label: str, options: list[dict], required: bool = False
) -> dbc.Select:
    """create a select component with dash bootstrap components"""
    component_id = "{}_input".format(label)
    return dbc.Select(
        id=component_id,
        options=options,
        placeholder=PLACEHOLDERS[label],
        required=required,
    )


def _create_input(
    label: str, input_type: Literal["text", "number"]
) -> dbc.Input:
    """create an input component with dash bootstrap components"""
    component_id = "{}_input".format(label)
    return dbc.Input(
        id=component_id,
        type=input_type,
        placeholder=PLACEHOLDERS[label],
        min=FEATURE_CONSTRAINTS[label]["min"],
        max=FEATURE_CONSTRAINTS[label]["max"],
        value=FEATURE_CONSTRAINTS[label][
            "default"
        ],  # deactivate to enable placeholders
    )


def _create_input_card(
    label: str,
    input_component: Component,
    offset: str = OFFSET,
    help_text: str = "Please enter a value.",
) -> dbc.Card:
    return dbc.Card(
        children=[
            dbc.CardBody(
                [
                    dbc.Label(
                        children=FIELD_LABELS[label],
                        html_for=input_component.id,
                    ),
                    input_component,
                    dbc.FormText(
                        children=help_text,
                        color="secondary",
                    ),
                ]
            )
        ],
        className="{}".format(offset),
    )


def _create_axis_dropdown(
    label: str, component_id: str, default_value: str
) -> dbc.Col:
    """Create a dropdown for scatter plot axis selection."""
    return dbc.Col(
        [
            dbc.Label(label),
            dcc.Dropdown(
                id=component_id,
                options=[
                    {"label": FIELD_LABELS[feat], "value": feat}
                    for feat in FEATURES
                ],
                value=default_value,
                clearable=False,
            ),
        ],
        width=6,
    )


def create_layout() -> dbc.Container:
    """Create the layout structure component."""
    return dbc.Container(
        children=[
            dcc.Store(id="latest_prediction_store"),
            dbc.Row(
                [
                    # Left side: input
                    dbc.Col(
                        width=3,
                        children=[
                            html.H4("Input Data", className="mb-3"),
                            # 1. Input: Island
                            _create_input_card(
                                label="island",
                                input_component=_create_select(
                                    label="island",
                                    options=ISLAND_OPTIONS,
                                    required=True,
                                ),
                            ),
                            # 2. Input: Bill length
                            _create_input_card(
                                label="bill_length_mm",
                                input_component=_create_input(
                                    label="bill_length_mm", input_type="number"
                                ),
                            ),
                            # 3. Input: Bill depth
                            _create_input_card(
                                label="bill_depth_mm",
                                input_component=_create_input(
                                    label="bill_depth_mm", input_type="number"
                                ),
                            ),
                            # 4. Input: Flipper Length
                            _create_input_card(
                                label="flipper_length_mm",
                                input_component=_create_input(
                                    label="flipper_length_mm",
                                    input_type="number",
                                ),
                            ),
                            # 5. Input: Body Mass
                            _create_input_card(
                                label="body_mass_g",
                                input_component=_create_input(
                                    label="body_mass_g",
                                    input_type="number",
                                ),
                            ),
                            # 5. Input: Sex
                            _create_input_card(
                                label="sex",
                                input_component=_create_select(
                                    label="sex",
                                    options=SEX_OPTIONS,
                                ),
                            ),
                            dbc.Card(
                                children=[
                                    dbc.CardBody(
                                        children=[
                                            dbc.Button(
                                                children="Classify",
                                                id="classify_button",
                                                color="primary",
                                                className="w-100",
                                                size="lg",
                                            ),
                                        ]
                                    )
                                ],
                                className="shadow-sm border-0",
                            ),
                        ],
                    ),
                    # Right side: Output
                    dbc.Col(
                        width=9,
                        lg=9,
                        children=[
                            # Output classification and score.
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            html.H3(
                                                "Penguin Classifier",
                                                className="mb-3",
                                            ),
                                            dbc.Card(
                                                children=[
                                                    dbc.CardHeader(
                                                        "Classification Result",
                                                        className="fw-bold",
                                                    ),
                                                    dbc.CardBody(
                                                        dbc.Alert(
                                                            children="Bitte Werte eingeben und 'Classify' drücken...",
                                                            id="classification_result",
                                                            color="info",
                                                            className="text-center fw-bold m-0",
                                                            style={
                                                                "marginTop": "10px"
                                                            },
                                                        ),
                                                    ),
                                                ]
                                            ),
                                        ]
                                    )
                                ]
                            ),
                            html.Br(),
                            # Output Scatterplot and Table
                            dbc.Row(
                                [
                                    # Scatterplot
                                    dbc.Col(
                                        width=8,
                                        xl=8,
                                        children=[
                                            dbc.Card(
                                                children=[
                                                    dbc.CardHeader(
                                                        "Penguin Data Analysis"
                                                    ),
                                                    dbc.CardBody(
                                                        [
                                                            dcc.Graph(
                                                                id="scatter_graph",
                                                                figure={},
                                                                responsive=True,
                                                                style={
                                                                    "height": "450px",
                                                                },
                                                            ),
                                                            # Add dropdowns for scatter plot customization
                                                            dbc.Row(
                                                                [
                                                                    _create_axis_dropdown(
                                                                        "Y-Axis",
                                                                        "scatter_y_axis",
                                                                        "bill_length_mm",
                                                                    ),
                                                                    _create_axis_dropdown(
                                                                        "X-Axis",
                                                                        "scatter_x_axis",
                                                                        "flipper_length_mm",
                                                                    ),
                                                                ],
                                                                className="mt-3",
                                                            ),
                                                        ],
                                                        className="p-1",
                                                    ),
                                                ],
                                                outline=True,
                                                className="shadow-sm border-1 h-100",
                                            ),
                                        ],
                                    ),
                                    # Table
                                    dbc.Col(
                                        width=4,
                                        children=[
                                            dbc.Card(
                                                [
                                                    dbc.CardHeader("History"),
                                                    dbc.CardBody(
                                                        html.Div(
                                                            id="table_container",
                                                            style={
                                                                "maxHeight": "430px",
                                                                "overflowY": "auto",
                                                            },
                                                        )
                                                    ),
                                                ],
                                                className="shadow-sm border-1 h-100",
                                            )
                                        ],
                                    ),
                                ],
                                className="g-3",
                            ),
                            html.Br(),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        width=12,
                                        children=[_create_performance_card()],
                                    )
                                ],
                            ),
                        ],
                    ),
                ],
                className="g-4",
            ),
        ],
        fluid=True,
        className="p-4 bg-light",
    )
