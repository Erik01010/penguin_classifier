import pandas as pd
from typing import Literal

from config import (
    FEATURE_CONSTRAINTS,
    ISLAND_OPTIONS,
    OFFSET,
    SEX_OPTIONS,
)
from dash import html, dcc
from dash.development.base_component import Component
import dash_bootstrap_components as dbc

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
    """Create a Card component with another component as input."""
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


def create_layout() -> dbc.Container:
    """Create the layout structure component."""
    return dbc.Container(
        children=[
            dbc.Row(
                [
                    # Left side: input
                    dbc.Col(
                        width=3,
                        children=[
                            html.Br(),
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
                                            ),
                                        ]
                                    )
                                ],
                                className=OFFSET,
                            ),
                        ],
                    ),
                    # Right side: Output
                    dbc.Col(
                        width=9,
                        children=[
                            # Output classification and score.
                            dbc.Row(
                                [
                                    dbc.Label(
                                        children="Penguin Classifier",
                                        style={"margin-top": "10px"},
                                        size="lg",
                                    ),
                                    dbc.Card(
                                        children=[
                                            dbc.Label(
                                                children="Classification Result:",
                                                size="lg",
                                            ),
                                            dbc.Alert(
                                                children="Ergebnis erscheint hier ...",
                                                id="classification_result",
                                                color="primary",
                                                style={"margin-top": "10px"},
                                            ),
                                        ]
                                    ),
                                ]
                            ),
                            # Output Scatterplot and Table
                            dbc.Row(
                                [
                                    # Scatterplot
                                    dbc.Col(
                                        width=5,
                                        children=[
                                            dbc.Label(
                                                children="Plot",
                                                size="lg",
                                            ),
                                            dbc.Card(
                                                children=[
                                                    dcc.Graph(
                                                        id="scatter_graph",
                                                        figure={},
                                                        responsive=True,
                                                    ),
                                                ],
                                                outline=True,
                                                color="primary",
                                            ),
                                        ],
                                    ),
                                    # Table
                                    dbc.Col(
                                        width=4,
                                        children=[
                                            dbc.Label(
                                                children="Table",
                                                size="lg",
                                            ),
                                            dbc.Card(
                                                children=[],
                                                id="table_container",
                                                outline=True,
                                                color="primary",
                                            ),
                                        ],
                                    ),
                                ]
                            ),
                        ],
                    ),
                ]
            ),
        ],
        fluid=True,
    )
