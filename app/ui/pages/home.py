import dash
from dash import html

from ui.pages._common_layout import common_layout

_PATH = "/"

layout = common_layout(
    html.H1("This is our Home page"),
    html.Div("This is our Home page content."),
)


def register(_app: dash.Dash) -> None:
    dash.register_page(__name__, path=_PATH, layout=layout)
