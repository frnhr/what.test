import dash_bootstrap_components as dbc
from dash import Dash

from ui.callbacks import register_auth_callbacks
from ui.clientside_sugar import add_clientside_decorator
from ui.layout import get_layout

__all__ = ["app"]


app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.SKETCHY],
    prevent_initial_callbacks=True,
)

add_clientside_decorator(app)

app.layout = get_layout()
register_auth_callbacks(app)


if __name__ == "__main__":
    app.run_server(debug=True)
