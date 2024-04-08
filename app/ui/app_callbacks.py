from dash import ClientsideFunction, Dash, Input, Output, State


def register_auth_callbacks(app: Dash) -> None:
    clientside_namespace = "auth"

    app.clientside_callback(
        ClientsideFunction(clientside_namespace, "loadUserData"),
        [
            Output("user_data", "data"),
            Output("new_user_data", "data", allow_duplicate=True),
            Output("_pages_location", "pathname", allow_duplicate=True),
        ],
        Input("url", "pathname"),
        Input("new_user_data", "data"),
        State("user_data", "data"),
        State("settings", "data"),
        prevent_initial_call=False,
    )

    app.clientside_callback(
        ClientsideFunction(clientside_namespace, "applyUserData"),
        [
            Output("user_menu_wrap", "hidden"),
            Output("user_menu", "label"),
            Output("login_link_wrap", "hidden"),
        ],
        Input("user_data", "data"),
        prevent_initial_call=False,
    )
