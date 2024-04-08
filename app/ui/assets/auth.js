window.dash_clientside = Object.assign({}, window.dash_clientside, {
    auth: {
        /**
         * Callback. On change of pathname, check if we have user data.
         *
         * This triggers only one time, when the app is first loaded, or possibly also when the user tries
         * to navigate to a new page without being logged in.
         */
        loadUserData: async (pathname, newUserData, userData, settings) => {
            // another callback set new_user_data, copy it to user_data:
            if (dash_clientside.callback_context.triggered_id === "new_user_data" && newUserData !== undefined) {
                return [newUserData, null, dash_clientside.no_update];
            }

            // if no user data, fetch it from backend:
            if (!userData) {
                const responseData = await fetch(settings.backendPath + "api/me/")
                    .then(response => response.json()).catch(() => null);
                if (responseData && responseData.email) {
                    return [responseData, null, dash_clientside.no_update];
                }
                return [null, null, "/login/"];
            }

            // no-op:
            return [dash_clientside.no_update, dash_clientside.no_update, dash_clientside.no_update];
        },

        /**
         * Callback. After user data is loaded, apply it to the UI.
         */
        applyUserData: (userData) => {
            const retData = {
                userMenuHidden: true,
                userMenuLabel: "",
                loginHidden: false,
            };
            if (userData) {
                retData.userMenuLabel = userData.email;
                retData.userMenuHidden = false;
                retData.loginHidden = true;
            }
            return [retData.userMenuHidden, retData.userMenuLabel, retData.loginHidden];
        },
    }
});
