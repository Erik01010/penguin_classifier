from dash import Input, Output, State, callback, ctx, no_update
import dash_bootstrap_components as dbc
from loguru import logger
import pandas as pd

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
    Output(component_id="scatter_graph", component_property="figure"),
    Output(component_id="table_container", component_property="children"),
    Output(component_id="latest_prediction_store", component_property="data"),
    Input(component_id="classify_button", component_property="n_clicks"),
    Input(component_id="scatter_x_axis", component_property="value"),
    Input(component_id="scatter_y_axis", component_property="value"),
    State("island_input", "value"),
    State("bill_length_mm_input", "value"),
    State("bill_depth_mm_input", "value"),
    State("flipper_length_mm_input", "value"),
    State("body_mass_g_input", "value"),
    State("sex_input", "value"),
    State("latest_prediction_store", "data"),
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
    result_text = "Geben Sie die Daten ein und klicken Sie auf Classify."
    new_penguin_data = None
    trigger_id = ctx.triggered_id

    # Handle initial load or dropdown interactions
    if trigger_id != "classify_button" and n_clicks is None:
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
            updated_data = load_combined_data().head(10)
            table = dbc.Table.from_dataframe(
                updated_data, striped=True, bordered=True, hover=True
            )
        except FileNotFoundError:
            table = "Noch keine historischen Daten verfügbar."

        logger.info("initial callback complete")
        return result_text, fig, table, no_update

    # Handle dropdown changes only (if button wasn't clicked)
    if trigger_id in ["scatter_x_axis", "scatter_y_axis"]:
        current_data = load_combined_data()

        # Check if we have a stored prediction to display
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
        return no_update, fig, no_update, no_update

    # Click on classify-button
    if trigger_id == "classify_button":
        # Input validation
        if not island:
            logger.warning("missing island input")
            return "Please enter island.", no_update, no_update, no_update

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
            species, proba = predict_single_penguin_proba(
                features=penguin_attributes
            )
            result_text = f"Species: {species}, Probability: {proba}"
            logger.info("penguin predicted")
            penguin_attributes["species"] = species
            new_penguin_data = penguin_attributes

            save_prediction(new_penguin_data)

            # Serialize for store
            store_data = penguin_attributes.to_dict("records")

            refreshed_data = load_combined_data()

            figure = create_scatter_plot(
                df_historic=refreshed_data,
                x_column=x_axis,
                y_column=y_axis,
                size_column="body_mass_g",
                new_data=penguin_attributes,
            )
            logger.info("scatter plot created")

            updated_data = load_combined_data().head(10)
            table = dbc.Table.from_dataframe(
                updated_data,
                striped=True,
                bordered=True,
                hover=True,
                index=True,
            )
            logger.info("callback complete")
            if not sex:
                result_text += (
                    " - Note: No sex provided. Classification may be wrong."
                )
            return result_text, figure, table, store_data

        except Exception as e:
            logger.exception("Error in Callback:")
            return f"DEBUG ERROR: {str(e)}", {}, "", no_update

    return no_update, no_update, no_update, no_update
