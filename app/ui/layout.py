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
            dcc.Store(id="new_user_data", data=None),
            dcc.Store(id="settings", data=settings.model_dump(by_alias=True)),
            _get_navbar(),
            page_container,
        ],
    )


def _get_navbar() -> Component:
    login_page = page_registry["ui.pages.login"]
    logout_page = page_registry["ui.pages.logout"]
    special_pages = [login_page, logout_page]

    navbar = dbc.NavbarSimple(
        children=[
            *[
                dbc.NavItem(
                    dbc.NavLink(page["name"], href=page["relative_path"]),
                )
                for page in page_registry.values()
                if page not in special_pages
            ],
            html.Div(
                id="login_link_wrap",
                hidden=False,
                children=dbc.NavItem(
                    dbc.NavLink(
                        login_page["name"],
                        href=login_page["relative_path"],
                    ),
                ),
            ),
            html.Div(
                id="user_menu_wrap",
                hidden=True,
                children=dbc.DropdownMenu(
                    id="user_menu",
                    children=[
                        dbc.DropdownMenuItem("User Menu", header=True),
                        dbc.DropdownMenuItem(
                            "Logout",
                            href=logout_page["relative_path"],
                        ),
                        dbc.DropdownMenuItem("Page 3", href="#"),
                    ],
                    nav=True,
                    in_navbar=True,
                    label="",
                ),
            ),
        ],
        brand="ProdSelect",
        brand_href="/",
        color="primary",
        dark=True,
    )
    return navbar
