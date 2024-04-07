from dash import ClientsideFunction, Dash, Input, Output, State


def register_auth_callbacks(app: Dash) -> None:
    clientside_namespace = "auth"

    app.clientside_callback(
        ClientsideFunction(clientside_namespace, "loadUserData"),
        Output("_pages_location", "pathname"),
        Input("url", "pathname"),
        State("user_data", "data"),
        State("settings", "data"),
        prevent_initial_call=False,
    )
