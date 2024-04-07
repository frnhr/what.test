import dash_bootstrap_components as dbc
from dash import dcc, html, page_container, page_registry
from dash.development.base_component import Component

__all__ = ["get_layout"]

from ui.settings import settings


def get_layout() -> Component:
    return html.Div(
        [
            dcc.Location(id="url", refresh=False),
            dcc.Store(id="user_data", data=None),
            dcc.Store(id="settings", data=settings.model_dump()),
            _get_navbar(),
            page_container,
        ],
    )


def _get_navbar() -> Component:
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink(page["name"], href=page["relative_path"]))
            for page in page_registry.values()
        ],
        brand="ProdSelect",
        brand_href="/",
        color="primary",
        dark=True,
    )
    return navbar
