"""
Just to make things easier to navigate, this page is spit up into a few
modules.
"""

import dash
from dash import dcc, html

from ui.pages._common_layout import common_layout
from ui.pages.home.products import (
    ag_grid,
    register_products_callbacks,
    search_box,
)
from ui.pages.home.selection_cards import (
    duplicate_selection_toast,
    register_selection_cards_callbacks,
    selected_products_container,
)

_PATH = "/"
_NAME = "Home"


layout = common_layout(
    html.H1("This is our Home page"),
    html.P("This is our Home page content."),
    dcc.Store(id="selected_product_store", data=[]),
    html.Div(
        [duplicate_selection_toast],
        style={
            "position": "fixed",
            "top": 66,
            "right": 10,
            "width": 350,
            "zIndex": 2,
        },
    ),
    search_box,
    dcc.Store(id="product_persistence", data={}, storage_type="local"),
    dcc.Store(id="product_grid_is_ready", data=False, storage_type="memory"),
    ag_grid,
    html.H5("Selected products", style={"marginTop": 20}),
    selected_products_container,
    html.Hr(),
    cols=12,
)


def register(app: dash.Dash) -> None:
    dash.register_page(__name__, path=_PATH, name=_NAME, layout=layout)

    register_products_callbacks(app)
    register_selection_cards_callbacks(app)
