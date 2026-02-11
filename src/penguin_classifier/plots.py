import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def create_scatter_plot(
    df_historic: pd.DataFrame,
    x_column: str = "flipper_length_mm",
    y_column: str = "bill_length_mm",
    size_column: str = None,
    new_data: pd.DataFrame = None,
) -> go.Figure:
    """
    Create a scatter plot of penguin dataset.
    The latest datapoint generated is highlighted.
    """
    color_map = {
        "Adelie": "#636EFA",
        "Chinstrap": "#EF553B",
        "Gentoo": "#00CC96",
    }
    fig = px.scatter(
        data_frame=df_historic,
        x=x_column,
        y=y_column,
        color="species",
        color_discrete_map=color_map,
        title="Penguin Data",
        size=size_column,
        template="simple_white",
        opacity=0.5,
    )

    if new_data is not None:
        fig.add_trace(
            go.Scatter(
                x=new_data[x_column],
                y=new_data[y_column],
                mode="markers",
                marker=dict(
                    color="yellow",
                    size=15,
                    opacity=1,
                    symbol="star",
                    line=dict(width=1, color="black"),
                ),
                name="Latest Prediction",
            )
        )

    fig.update_layout(
        legend_title="Species",
    )

    return fig
