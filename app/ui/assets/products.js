window.dash_clientside = Object.assign({}, window.dash_clientside, {
    products: {
        /**
         * Helper function to clear the local storage for persisted state.
         * Used when logs out and also when logs in.
         */
        clearPersistedData: () => {
            window.localStorage.removeItem("product_persistence");
        },

        /**
         * Callback. Poor man's throttle function.
         *
         * Because dcc.Input only provides debounce.
         */
        throttleSearchInput: (value, currentValue) => {
            if (value === currentValue) {
                return dash_clientside.no_update;
            }
            return value;
        },

        /**
         * Callback. On input in the search field, update the filter model in AG Grid.
         */
        updateFilter: (filterValue, filterModel) => ({
            ...filterModel,
            name: {
                "filterType": "text",
                "type": "contains",
                "filter": filterValue,
            }
        }),

        /**
         * Callback. Handle all logic on the AG Grid component.
         *
         * "Infinite" is the operation mode of the AG Grid used here ("clientside" is the default mode).
         *
         * Some complexity here is due to `persistence` having no effect on the AG Grid component,
         * so we have to handle it manually.
         */
        infiniteScroll: async (request, isReady, persistedData, columnState, userInput, settings) => {
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
                                 const minus = (sort.sort === 'desc') ? '-' : '';
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
                // (we could just query the API, but this is according to the specification)
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
    }
});
