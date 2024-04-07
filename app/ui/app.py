import dash_bootstrap_components as dbc
from dash_extensions.enrich import (
    DashProxy,
    NoOutputTransform,
    TriggerTransform,
)

from ui.callbacks import register_auth_callbacks
from ui.clientside_sugar import (
    add_clientside_decorator,
    enable_dash_extensions_clientside_trigger,
)
from ui.layout import get_layout

__all__ = ["app"]


app = DashProxy(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.SKETCHY],
    external_scripts=[
        "https://cdn.jsdelivr.net/npm/js-cookie@3.0.5/dist/js.cookie.min.js",
    ],
    prevent_initial_callbacks=True,
    suppress_callback_exceptions=True,
    transforms=[
        # MultiplexerTransform(),
        TriggerTransform(),
        NoOutputTransform(),
    ],
)

enable_dash_extensions_clientside_trigger()
add_clientside_decorator(app)

app.layout = get_layout()
register_auth_callbacks(app)


if __name__ == "__main__":
    app.run_server(debug=True)
