import dash
import dash_bootstrap_components as dbc
from dash import Output, State, html
from dash_extensions.enrich import Trigger

from ui.pages._common_layout import common_layout

_PATH = "/login/"


_email_input = html.Div(
    [
        dbc.Label("Email", html_for="example-email"),
        dbc.Input(type="email", id="email_input", placeholder="Enter email"),
        dbc.FormText(
            "Are you on email? You simply have to be these days",
            color="secondary",
        ),
    ],
    className="mb-3",
)

_password_input = html.Div(
    children=[
        dbc.Label("Password", html_for="example-password"),
        dbc.Input(
            type="password",
            id="password_input",
            placeholder="Enter password",
        ),
        dbc.FormText(
            "A password stops mean people taking your stuff",
            color="secondary",
        ),
    ],
    className="mb-3",
)


_login_btn = dbc.Button("Submit", id="login_btn", color="primary")

layout = common_layout(
    html.H2("Sign in"),
    html.P("Please enter your credentials."),
    dbc.Form(
        [
            _email_input,
            _password_input,
            _login_btn,
        ],
    ),
)


def register(app: dash.Dash) -> None:
    dash.register_page(__name__, path=_PATH, layout=layout)

    @app.clientside(
        [
            Output("new_user_data", "data", allow_duplicate=True),
            Output("_pages_location", "pathname"),
        ],
        Trigger("login_btn", "n_clicks"),
        State("email_input", "value"),
        State("password_input", "value"),
        State("settings", "data"),
    )
    def login() -> str:
        return """async (email, password, settings) => {

            // cleanup persisted data (possibly from previous user)::
            dash_clientside.productSelection.clearPersistedData();

            // initial callback will have no user inputs, skip:
            if (!email || !password) {
                return dash_clientside.no_update;
            }

            // load CSRF cookie from backend
            const loadCsrfCookie = async () => await fetch(
                `${settings.backendPath}auth/login/`,
                {credentials: 'same-origin'}
            );

            // send login request to backend:
            const sendLoginRequest = async () => {
                let formData = new FormData();
                formData.append('username', email);
                formData.append('password', password);
                formData.append(
                    'csrfmiddlewaretoken',
                    Cookies.get('csrftoken')
                );
                formData.append('next', '/backend/api/me/');
                return fetch(`${settings.backendPath}auth/login/`, {
                  method: "POST",
                  body: formData
                })
               .then((response) => response.json());
            };

            // perform the two operations:
            const userData = await loadCsrfCookie().then(sendLoginRequest);

            // TODO handle login errors
            const redirectPath = settings.redirectAfterLoginPath;

            return [userData, redirectPath];
        }
        """
