import json

import dash
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
from dash import ALL, MATCH, Input, Output, State, dcc, html
from dash_extensions.enrich import Trigger

from ui.pages._common_layout import common_layout

_PATH = "/"


column_defs = [
    {"field": "id", "minWidth": 150, "cellRenderer": "SpinnerCellRenderer"},
    {"field": "name", "minWidth": 150, "filter": True, "suppressMenu": True},
    {"field": "price", "maxWidth": 120},
    {"field": "stock", "maxWidth": 120},
    {"field": "description", "minWidth": 150},
    {
        "field": "select",
        "cellRenderer": "DBC_Button_Simple",
        "cellRendererParams": {"color": "secondary"},
        "valueGetter": {"function": "'Select'"},
        "maxWidth": 120,
        "sortable": False,
    },
]

default_col_def = {
    "flex": 1,
    "minWidth": 150,
    "sortable": True,
    "resizable": True,
}

ag_grid = dag.AgGrid(
    id="product_grid",
    columnDefs=column_defs,
    defaultColDef=default_col_def,
    rowModelType="infinite",
    dashGridOptions={
        "rowBuffer": 20,
        "maxBlocksInCache": 5,
        "cacheBlockSize": 500,
        "cacheOverflowSize": 2,
        "maxConcurrentDatasourceRequests": 2,
        "infiniteInitialRowCount": 1,
        "rowSelection": "single",
        "pagination": True,
        "alwaysMultiSort": True,
    },
    # persistence=True,
    # persisted_props=["filterModel", "sortModel"]
    # TODO For some reason persistence ^ does not work.
    #      Using Store(id="product_persistence") instead.
)


search_box = html.Div(
    [
        dbc.Input(
            id="search_input",
            placeholder="Search...",
            autofocus=True,
            # persistence=True,
        ),
        dcc.Interval(id="search_timer", interval=1000),
        dcc.Store(id="search_current_value", data=""),
    ],
)

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

layout = common_layout(
    html.H1("This is our Home page"),
    html.P("This is our Home page content."),
    dcc.Store(id="selected_product_store", data=[]),
    html.Div(
        [duplicate_selection_toast],
        style={
            "position": "fixed",
            "top": 66,
            "right": 10,
            "width": 350,
            "zIndex": 2,
        },
    ),
    search_box,
    dcc.Store(id="product_persistence", data={}, storage_type="local"),
    dcc.Store(id="product_grid_is_ready", data=False, storage_type="memory"),
    ag_grid,
    html.H5("Selected products", style={"marginTop": 20}),
    selected_products_container,
    html.Hr(),
    cols=12,
)


def register(app: dash.Dash) -> None:
    dash.register_page(__name__, path=_PATH, layout=layout)

    @app.clientside(
        [
            Output("search_current_value", "data"),
        ],
        Trigger("search_timer", "n_intervals"),
        State("search_input", "value"),
        State("search_current_value", "data"),
    )
    def throttle_search_input() -> str:
        """
        Poor man's throttle function.

        Because dcc.Input only provides debounce.
        """
        return """ (value, currentValue) => {
            if (value === currentValue) {
                return dash_clientside.no_update;
            }
            return value;
        };
        """

    @app.clientside(
        [
            Output("product_grid", "filterModel"),
        ],
        Input("search_current_value", "data"),
        State("product_grid", "filterModel"),
    )
    def update_filter() -> str:
        return """ (filterValue, filterModel) => ({
            ...filterModel,
            name: {
                "filterType": "text",
                "type": "contains",
                "filter": filterValue,
            }
        });
        """

    @app.clientside(
        [
            Output("product_grid", "getRowsResponse"),
            Output("product_grid_is_ready", "data"),
            Output("product_persistence", "data"),
            Output("product_grid", "columnState"),
            Output("search_input", "value"),
        ],
        Input("product_grid", "getRowsRequest"),
        State("product_grid_is_ready", "data"),
        State("product_persistence", "data"),
        State("product_grid", "columnState"),
        State("search_input", "value"),
        State("settings", "data"),
    )
    def infinite_scroll() -> str:
        return """
        async (
            request,
            isReady,
            persistedData,
            columnState,
            userInput,
            settings,
        ) => {

            let searchInput;

            // initial load:
            if (!isReady) {
                isReady = true;
                // restore persisted data:
                searchInput = persistedData.searchInput || '';
                columnState = persistedData.columnState || columnState || null;

                persistedData = {
                    columnState: columnState,
                    searchInput: searchInput,
                };
                // Setting columnState and searchInput will trigger
                // this callback again.
                return [
                    { rowData: [], rowCount: 0 },
                    isReady,
                    persistedData,
                    columnState,
                    searchInput,
                ];
            }

            // normal call:
            searchInput = request.filterModel?.name?.filter || '';

            // User entered something, but it is not yet in the request.
            // This happens right after the initial load because there
            // the search input string was restored.
            // The callback function will be triggered again (with the
            // search value in the request), so we can ignore this one.
            if (userInput !== searchInput) {
                return dash_clientside.no_update;
            }

            const limit = request.endRow - request.startRow;
            const offset = request.startRow;
            const search = (searchInput) ? `&search=${searchInput}` : '';
            const sort = (request.sortModel.length > 0)
                         ? '&ordering=' + request.sortModel.reduce(
                             (acc, sort) => {
                                 const comma = acc ? ',' : '';
                                 const minus = (sort.sort === 'desc')
                                                 ? '-' : '';
                                 const col = sort.colId;
                                 return `${acc}${comma}${minus}${col}`;
                             },
                             '',
                           )
                         : '';
            const query = `limit=${limit}&offset=${offset}${search}${sort}`;

            let response;

            if (searchInput) {
                // searched for something, call the API:
                response = await fetch(
                    `${settings.backendPath}api/products/?${query}`,
                    { credentials: 'include' }
                )
                .then((response) => response.json());
            } else {
                // special case for no input, show empty table:
                // (we could just query the API, but this is accoring to the
                // specification)
                response = { results: [], count: 0 };
            }

            persistedData = {
                columnState: columnState,
                searchInput: searchInput,
            };

            return [
                { rowData: response.results, rowCount: response.count },
                isReady,
                persistedData,
                columnState,
                searchInput,
            ];
        }
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
        return """
            async (
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
        return f"""
            (store) => {{
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
        return """async (selectionId, settings) => {
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
