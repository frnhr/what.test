import dash
import dash_ag_grid as dag
from dash import Input, Output, State, html

from ui.pages._common_layout import common_layout

_PATH = "/"


column_defs = [
    # this row shows the row index, doesn't use any data from the row
    # {
    #     "headerName": "ID",
    #     "maxWidth": 100,
    #     # it is important to have node.id here, so that when the id changes
    #     # (which happens when the row is loaded) then the cell is refreshed.
    #     "valueGetter": {"function": "params.node.id"},
    #     # "cellRenderer": "SpinnerCellRenderer",
    # },
    {"field": "id", "minWidth": 150, "cellRenderer": "SpinnerCellRenderer"},
    {"field": "name", "minWidth": 150},
    {"field": "description", "minWidth": 150},
    {"field": "price"},
    {"field": "stock", "minWidth": 150},
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
        # The number of rows rendered outside the viewable area the grid renders
        "rowBuffer": 0,
        # How many blocks to keep in the store. Default is no limit, so every
        # requested block is kept.
        "maxBlocksInCache": 5,
        "cacheBlockSize": 500,
        "cacheOverflowSize": 2,
        "maxConcurrentDatasourceRequests": 2,
        "infiniteInitialRowCount": 1,
        "rowSelection": "multiple",
        "pagination": True,
    },
)


layout = common_layout(
    html.H1("This is our Home page"),
    html.Div("This is our Home page content."),
    ag_grid,
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
