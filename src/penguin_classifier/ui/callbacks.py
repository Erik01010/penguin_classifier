from dash import Input, Output, State, callback, ctx, no_update
import dash_bootstrap_components as dbc
from loguru import logger
import pandas as pd

from src.penguin_classifier.config import FEATURE_CONSTRAINTS
from src.penguin_classifier.dataset import load_combined_data, save_prediction
from src.penguin_classifier.modeling.predict import (
    predict_single_penguin_proba,
)
from src.penguin_classifier.plots import create_scatter_plot

prediction_history = load_combined_data()


@callback(
    Output(
        component_id="classification_result", component_property="children"
    ),
    Output(component_id="classification_result", component_property="is_open"),
    Output(component_id="classification_result", component_property="color"),
    Output(component_id="scatter_graph", component_property="figure"),
    Output(component_id="table_container", component_property="children"),
    Output(component_id="latest_prediction_store", component_property="data"),
    Input(component_id="classify_button", component_property="n_clicks"),
    Input(component_id="scatter_x_axis", component_property="value"),
    Input(component_id="scatter_y_axis", component_property="value"),
    State(component_id="island_input", component_property="value"),
    State(component_id="bill_length_mm_input", component_property="value"),
    State(component_id="bill_depth_mm_input", component_property="value"),
    State(component_id="flipper_length_mm_input", component_property="value"),
    State(component_id="body_mass_g_input", component_property="value"),
    State(component_id="sex_input", component_property="value"),
    State(component_id="latest_prediction_store", component_property="data"),
)
def classify_penguin(
    n_clicks,
    x_axis,
    y_axis,
    island,
    bill_length_mm,
    bill_depth_mm,
    flipper_length_mm,
    body_mass_g,
    sex,
    latest_prediction,
):
    msg = "Please enter values and press Classify"
    new_penguin_data = None
    trigger_id = ctx.triggered_id

    # Handle initial load
    if (
        trigger_id
        not in ["classify_button", "scatter_x_axis", "scatter_y_axis"]
        and n_clicks is None
    ):
        # Initial startup
        current_data = load_combined_data()
        fig = create_scatter_plot(
            df_historic=current_data,
            x_column=x_axis or "flipper_length_mm",
            y_column=y_axis or "bill_length_mm",
            size_column="body_mass_g",
            new_data=new_penguin_data,
        )
        try:
            updated_data = load_combined_data()
            table = dbc.Table.from_dataframe(
                updated_data, striped=True, bordered=True, hover=True
            )
        except FileNotFoundError:
            table = "Noch keine historischen Daten verfügbar."

        logger.info("initial callback complete")
        return msg, True, "info", fig, table, no_update

    # Handle dropdown changes only (if button wasn't clicked)
    if trigger_id in ["scatter_x_axis", "scatter_y_axis"]:
        current_data = load_combined_data()

        new_data = None
        if latest_prediction:
            try:
                new_data = pd.DataFrame(latest_prediction)
            except Exception:
                logger.warning("Could not restore classification from store")

        fig = create_scatter_plot(
            df_historic=current_data,
            x_column=x_axis,
            y_column=y_axis,
            size_column="body_mass_g",
            new_data=new_data,
        )
        logger.info("changed axis")
        return no_update, no_update, no_update, fig, no_update, no_update

    # Click on classify-button
    if trigger_id == "classify_button":
        # Input validation
        # Island input
        if not island:
            logger.warning("missing island input")
            msg = "Please enter island."
            return msg, True, "danger", no_update, no_update, no_update

        inputs_to_validate = {
            "bill_length_mm": bill_length_mm,
            "bill_depth_mm": bill_depth_mm,
            "flipper_length_mm": flipper_length_mm,
            "body_mass_g": body_mass_g,
        }
        # Numerical input
        for feature_name, value in inputs_to_validate.items():
            if value is None or value == "":
                logger.warning("alue out of bounds")
                msg = f"Please enter allowed value for '{feature_name}'."
                return (
                    msg,
                    True,
                    "danger",
                    no_update,
                    no_update,
                    no_update,
                )

        try:
            penguin_attributes = pd.DataFrame(
                {
                    "island": [island],
                    "bill_length_mm": [float(bill_length_mm)],
                    "bill_depth_mm": [float(bill_depth_mm)],
                    "flipper_length_mm": [float(flipper_length_mm)],
                    "body_mass_g": [float(body_mass_g)],
                    "sex": [sex],
                }
            )
            # classify
            species, proba = predict_single_penguin_proba(
                features=penguin_attributes
            )
            msg = (
                f"Species: {species} --- Probability: {round(proba * 100, 2)}%"
            )
            if not sex:
                msg += " - Note: No sex provided."
            logger.info("penguin predicted")
            penguin_attributes["species"] = species
            new_penguin_data = penguin_attributes

            save_prediction(new_penguin_data)

            # Serialize for store
            store_data = penguin_attributes.to_dict("records")

            # load pred history if exists
            refreshed_data = load_combined_data()

            # scatterplot
            figure = create_scatter_plot(
                df_historic=refreshed_data,
                x_column=x_axis,
                y_column=y_axis,
                size_column="body_mass_g",
                new_data=penguin_attributes,
            )
            logger.info("scatter plot created")

            # table
            updated_data = load_combined_data()
            table = dbc.Table.from_dataframe(
                updated_data,
                striped=True,
                bordered=True,
                hover=True,
            )
            logger.info("callback complete")

            return msg, True, "success", figure, table, store_data

        except Exception as e:
            logger.exception("Error in Callback:")
            return f"DEBUG ERROR: {str(e)}", {}, "", no_update

    return no_update, no_update, no_update, no_update, no_update, no_update
