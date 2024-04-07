window.dash_clientside = Object.assign({}, window.dash_clientside, {
    auth: {
        /**
         * On change of pathname, check if we have user data.
         *
         * This triggers only one time, when the app is first loaded, or possibly also when the user tries
         * to navigate to a new page without being logged in.
         */
        loadUserData: function(pathname, userData, settings) {
            if (settings.public_paths.includes(pathname)) {
                return dash_clientside.no_update;
            }
            if (!userData) {
                return settings.login_path;
            }
        }
    }
});
