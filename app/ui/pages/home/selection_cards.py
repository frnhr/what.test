import json

import dash
import dash_bootstrap_components as dbc
from dash import ALL, MATCH, Input, Output, State, dcc, html
from dash_extensions.enrich import Trigger

__all__ = [
    "duplicate_selection_toast",
    "selected_products_container",
    "register_selection_cards_callbacks",
]


duplicate_selection_toast = dbc.Toast(
    id="duplicate_selection_toast",
    header="Duplicate selection",
    is_open=False,
    dismissable=True,
    duration=2000,
    icon="danger",
    children=[
        html.P("This product is already selected:"),
        html.P("", id="duplicate_selection_toast_product_name"),
    ],
)


selected_products_container = dbc.Row(
    id="selected_products_container",
    children=[],
)


def register_selection_cards_callbacks(app: dash.Dash) -> None:
    """
    Callbacks relevant to the selection cards. It depends on the AG Grid from
    `products` module.

    Unlike the `products` module, this module uses the `clientside` decorator
    to define the clientside callbacks.
    It is weird to mix JS and Python, but there are some advantages, too.
    One even uses f-string...

    A must-have is an editor that can handle both languages, though!
    """

    @app.clientside(
        [
            Output("product_grid", "cellRendererData"),
            Output("selected_product_store", "data", allow_duplicate=True),
            Output("duplicate_selection_toast", "is_open"),
            Output("duplicate_selection_toast_product_name", "children"),
        ],
        Input("product_grid", "cellRendererData"),
        Trigger({"type": "selected_trigger", "id": ALL}, "value"),
        State("selected_product_store", "data"),
        State("duplicate_selection_toast", "is_open"),
        State("duplicate_selection_toast_product_name", "children"),
        State("settings", "data"),
        prevent_initial_call=False,
    )
    def select_product() -> str:
        return """ async (
            data,
            store,
            duplicateToastShow,
            duplicateToastProductName,
            settings,
        ) => {
            // new product selected
            if (data) {
                if (store.some((sel) => sel.product.id === data.value.id)) {
                    duplicateToastShow = true;
                    duplicateToastProductName = data.value.name;
                } else {
                    const response = await fetch(
                        `${settings.backendPath}api/selection/`,
                        {
                            method: "POST",
                            credentials: "include",
                            headers: {
                                "Content-Type": "application/json",
                                'X-CSRFToken': Cookies.get('csrftoken'),
                            },
                            body: JSON.stringify(
                                {
                                    "product_id": data.value.id
                                }
                            )
                        }
                    );
                    await response.json();
                }
            }

            // load selections from api
            const response = await fetch(
                `${settings.backendPath}api/selection/`,
                {credentials: 'include'}
            );
            const responseData = await response.json();
            store = responseData.results;
            data = null;

            return [
                data,
                store,
                duplicateToastShow,
                duplicateToastProductName,
            ];
        };
        """

    @app.clientside(
        [
            Output("selected_products_container", "children"),
        ],
        Input("selected_product_store", "data"),
    )
    def rendered_selected_products() -> str:
        selected_product_template = dbc.Col(
            id={"type": "selected_product_wrapper", "id": "PRODUCT_ID"},
            className="selected_product",
            children=[
                html.H5(
                    "PRODUCT_NAME",
                    id={"type": "selected_product_name", "id": "PRODUCT_ID"},
                    className="selected_product_name",
                ).to_plotly_json(),
                html.Button(
                    "X",
                    id={"type": "selected_product_remove", "id": "PRODUCT_ID"},
                    className="selected_product_remove",
                ).to_plotly_json(),
                dcc.Input(
                    id={"type": "selected_selection_id", "id": "PRODUCT_ID"},
                    value="SELECTION_ID",
                    type="hidden",
                ).to_plotly_json(),
                dcc.Input(
                    id={"type": "selected_trigger", "id": "PRODUCT_ID"},
                    value="",
                    type="hidden",
                ).to_plotly_json(),
                html.P(
                    "PRODUCT_DESCRIPTION",
                    id={
                        "type": "selected_product_description",
                        "id": "PRODUCT_ID",
                    },
                ).to_plotly_json(),
                html.P(
                    "PRODUCT_PRICE",
                    id={"type": "selected_product_price", "id": "PRODUCT_ID"},
                ).to_plotly_json(),
                html.P(
                    "PRODUCT_STOCK",
                    id={"type": "selected_product_stock", "id": "PRODUCT_ID"},
                ).to_plotly_json(),
            ],
        ).to_plotly_json()
        template = json.dumps(selected_product_template).replace("\n", " ")
        return f""" (store) => {{
            let children = [];
            for (const selection of store) {{
                let template = '{template}';
                template = template.replaceAll(
                    "PRODUCT_ID", selection.product.id
                );
                template = template.replaceAll(
                    "PRODUCT_NAME", selection.product.name
                );
                template = template.replaceAll(
                    "PRODUCT_DESCRIPTION", selection.product.description
                );
                template = template.replaceAll(
                    "PRODUCT_PRICE", selection.product.price
                );
                template = template.replaceAll(
                    "PRODUCT_STOCK", selection.product.stock
                );
                template = template.replaceAll(
                    "SELECTION_ID", selection.id
                );
                template = template.replaceAll("\\n", " ");
                children.push(JSON.parse(template));
            }}
            return children;
        }};
        """

    @app.clientside(
        [
            Output(
                {"type": "selected_product_remove", "id": MATCH},
                "n_clicks",
            ),
            Output({"type": "selected_trigger", "id": MATCH}, "value"),
        ],
        Trigger({"type": "selected_product_remove", "id": MATCH}, "n_clicks"),
        State({"type": "selected_selection_id", "id": MATCH}, "value"),
        State("settings", "data"),
    )
    def remove_selection() -> str:
        return """ async (selectionId, settings) => {
            await fetch(
                `${settings.backendPath}api/selection/${selectionId}/`,
                {
                    method: "DELETE",
                    credentials: "include",
                    headers: {
                        "Content-Type": "application/json",
                        'X-CSRFToken': Cookies.get('csrftoken'),
                    },
                }
            );
            return [0, Date.now()];
        }
        """
