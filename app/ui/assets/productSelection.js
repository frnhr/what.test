window.dash_clientside = Object.assign({}, window.dash_clientside, {
    productSelection: {
        /**
         * Helper function to clear the local storage for persisted state.
         * Used when logs out and also when logs in.
         */
        clearPersistedData: () => {
            window.localStorage.removeItem("product_persistence");
        },
    }
});
