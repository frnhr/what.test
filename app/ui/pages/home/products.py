import dash
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
from dash import ClientsideFunction, Input, Output, State, dcc, html
from dash_extensions.enrich import Trigger

__all__ = [
    "ag_grid",
    "search_box",
    "register_products_callbacks",
]

_column_defs = [
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


_default_col_def = {
    "flex": 1,
    "minWidth": 150,
    "sortable": True,
    "resizable": True,
}


ag_grid = dag.AgGrid(
    id="product_grid",
    columnDefs=_column_defs,
    defaultColDef=_default_col_def,
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


def register_products_callbacks(app: dash.Dash) -> None:
    """
    Clientside callbacks for the products table (the AG Grid).

    Callbacks are defined here (inputs, outputs, etc.), but the actual
    JS functions are located in `products.js`
    """
    app.clientside_callback(
        ClientsideFunction("products", "throttleSearchInput"),
        [
            Output("search_current_value", "data"),
        ],
        Trigger("search_timer", "n_intervals"),
        State("search_input", "value"),
        State("search_current_value", "data"),
    )

    app.clientside_callback(
        ClientsideFunction("products", "updateFilter"),
        [
            Output("product_grid", "filterModel"),
        ],
        Input("search_current_value", "data"),
        State("product_grid", "filterModel"),
    )

    app.clientside_callback(
        ClientsideFunction("products", "infiniteScroll"),
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
        State("search_current_value", "data"),
        State("settings", "data"),
    )
