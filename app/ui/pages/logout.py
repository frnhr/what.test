import dash
from dash import Input, Output, State, html

from ui.pages._common_layout import common_layout

_PATH = "/logout/"


layout = common_layout(
    html.H2("Signed out"),
    html.P("You have been signed out."),
)


def register(app: dash.Dash) -> None:
    dash.register_page(__name__, path=_PATH, layout=layout)

    @app.clientside(
        [
            Output("new_user_data", "data", allow_duplicate=True),
        ],
        Input("url", "pathname"),
        State("settings", "data"),
    )
    def logout() -> str:
        return """async (pathname, settings) => {
            if (pathname !== '/logout/') {
                return dash_clientside.no_update;
            }

            // send login request to backend:
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
            } catch (e) {
                console.error(e);
            }
            return null;
        }
        """
