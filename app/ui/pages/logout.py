import dash
from dash import Input, Output, State, html

from ui.pages._common_layout import common_layout

_PATH = "/logout/"
_NAME = "Logout"


layout = common_layout(
    html.H2("Signed out"),
    html.P("You have been signed out."),
)


def register(app: dash.Dash) -> None:
    dash.register_page(__name__, path=_PATH, name=_NAME, layout=layout)

    @app.clientside(
        [
            Output("new_user_data", "data", allow_duplicate=True),
        ],
        Input("url", "pathname"),
        State("settings", "data"),
    )
    def logout() -> str:
        return """ async (pathname, settings) => {
            if (pathname !== '/logout/') {
                return dash_clientside.no_update;
            }

            // cleanup persisted data:
            dash_clientside.products.clearPersistedData();

            // send logout request to backend:
            const sendLogoutRequest = async () => {
                let formData = new FormData();
                formData.append(
                    'csrfmiddlewaretoken',
                    Cookies.get('csrftoken')
                );
                return fetch(`${settings.backendPath}auth/logout/`, {
                  method: "POST",
                  body: formData
                })
               .then((response) => response.json());
            };

            // perform the operation:
            try {
                await sendLogoutRequest();
            } catch (e) {}
            return null;
        }
        """
