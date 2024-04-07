import dash
import dash_ag_grid as dag
from dash import Input, Output, State, dcc, html

from ui.pages._common_layout import common_layout

_PATH = "/"


column_defs = [
    {"field": "id", "minWidth": 150, "cellRenderer": "SpinnerCellRenderer"},
    {"field": "name", "minWidth": 150},
    {"field": "price", "maxWidth": 120},
    {"field": "stock", "maxWidth": 120},
    {"field": "description", "minWidth": 150},
    {
        "field": "select",
        "cellRenderer": "DBC_Button_Simple",
        "cellRendererParams": {"color": "secondary"},
        "valueGetter": {"function": "'Select'"},
    },
]

default_col_def = {
    "flex": 1,
    "minWidth": 150,
    "sortable": False,
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
    },
)


layout = common_layout(
    html.H1("This is our Home page"),
    html.Div("This is our Home page content."),
    dcc.Store(id="selected_product_store", data=[]),
    ag_grid,
    cols=12,
)


def register(app: dash.Dash) -> None:
    dash.register_page(__name__, path=_PATH, layout=layout)

    @app.clientside(
        [
            Output("product_grid", "getRowsResponse"),
        ],
        Input("product_grid", "getRowsRequest"),
        State("settings", "data"),
    )
    def infinite_scroll() -> str:
        return """
        async (request, settings) => {
            if (!request) return dash_clientside.no_update;

            const limit = request.endRow - request.startRow;
            const offset = request.startRow;
            const query = `limit=${limit}&offset=${offset}`;

            const response = await fetch(
                `${settings.backendPath}api/products/?${query}`,
                { credentials: 'include' }
            )
            .then((response) => response.json());

            return { rowData: response.results, rowCount: response.count };
        }
        """

    @app.clientside(
        Output("selected_product_store", "data"),
        Input("product_grid", "cellRendererData"),
        State("selected_product_store", "data"),
    )
    def show_change() -> str:
        return """
            (data, store) => {
                console.warn(data);
                store.push(data);
                return store;
            };
        """
