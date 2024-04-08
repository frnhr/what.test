import dash
from dash import html

from ui.pages._common_layout import common_layout

_PATH = "/page3/"

layout = common_layout(
    html.H1("Page 3"),
    html.P("Because lorem and ispum need a place to live, too."),
)


def register(_app: dash.Dash) -> None:
    dash.register_page(__name__, path=_PATH, layout=layout)
