import dash_bootstrap_components as dbc
from dash import html
from dash.development.base_component import Component

__all__ = ["common_layout"]


def common_layout(*contents: Component) -> Component:
    return html.Div(
        className="main-container",
        children=dbc.Row(dbc.Col([*contents], sm=12, lg=4)),
    )
