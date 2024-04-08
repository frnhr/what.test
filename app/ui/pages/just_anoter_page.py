import dash
from dash import html

from ui.pages._common_layout import common_layout

_PATH = "/another_page/"
_NAME = "Just another page"

layout = common_layout(
    html.H1("Just another page"),
    html.Div("This is just another page."),
)


def register(_app: dash.Dash) -> None:
    dash.register_page(__name__, path=_PATH, name=_NAME, layout=layout)
