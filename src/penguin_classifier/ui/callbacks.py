from dash import Input, Output, State, callback, no_update
import dash_bootstrap_components as dbc
import pandas as pd
from loguru import logger

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
    Input(component_id="classify_button", component_property="n_clicks"),
    State("island_input", "value"),
    State("bill_length_mm_input", "value"),
    State("bill_depth_mm_input", "value"),
    State("flipper_length_mm_input", "value"),
    State("body_mass_g_input", "value"),
    State("sex_input", "value"),
)
def classify_penguin(
    n_clicks,
    island,
    bill_length_mm,
    bill_depth_mm,
    flipper_length_mm,
    body_mass_g,
    sex,
):
    result_text = "Geben Sie die Daten ein und klicken Sie auf Classify."
    new_penguin_data = None
    print("Callback ausgelöst!")

    if n_clicks is not None:
        try:
            logger.info("convert values to dataframe...")
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
            logger.info("dict converted to dataframe...")
            species, proba = predict_single_penguin_proba(
                features=penguin_attributes
            )
            result_text = f"Species: {species}, Probability: {proba}"
            logger.info("penguin predicted")
            penguin_attributes["species"] = species
            new_penguin_data = penguin_attributes

            save_prediction(penguin_attributes)
            logger.info("prediction saved")

            figure = create_scatter_plot(
                df_historic=prediction_history,
                size_column="body_mass_g",
                new_data=penguin_attributes,
            )
            logger.info("scatter plot created")

            updated_data = load_combined_data().head(10)
            updated_data = updated_data.iloc[::-1]
            table = dbc.Table.from_dataframe(
                updated_data,
                striped=True,
                bordered=True,
                hover=True,
                index=True,
            )
            logger.info("table created")
            print(table)
            return result_text, figure, table

        except Exception as e:
            logger.exception("Fehler im Callback:")
            return f"DEBUG ERROR: {str(e)}", {}, ""

    current_data = load_combined_data()
    fig = create_scatter_plot(
        df_historic=current_data,
        size_column="body_mass_g",
        new_data=new_penguin_data,
    )
    try:
        updated_data = load_combined_data().head(10)
        updated_data = updated_data.iloc[::-1]
        table = dbc.Table.from_dataframe(
            updated_data.head(10), striped=True, bordered=True, hover=True
        )
    except FileNotFoundError:
        # Fallback beim allerersten Start ohne History
        table = "Noch keine historischen Daten verfügbar."

        # 4. Alles zurückgeben
    return result_text, fig, table
