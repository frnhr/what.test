const dagcomponentfuncs = (window.dashAgGridComponentFunctions = window.dashAgGridComponentFunctions || {});

dagcomponentfuncs.SpinnerCellRenderer = function (props) {
    if (props.value !== undefined) {
        return props.value;
    } else {
        return React.createElement(window.dash_bootstrap_components.Spinner, {color: "primary", size: "sm"})
    }
}
