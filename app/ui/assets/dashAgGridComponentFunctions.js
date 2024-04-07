const dagcomponentfuncs = (window.dashAgGridComponentFunctions = window.dashAgGridComponentFunctions || {});

dagcomponentfuncs.SpinnerCellRenderer = function (props) {
    if (props.value !== undefined) {
        return props.value;
    } else {
        return React.createElement(window.dash_bootstrap_components.Spinner, {color: "primary", size: "sm"})
    }
}

dagcomponentfuncs.DBC_Button_Simple = function (props) {
    const {setData, data} = props;

    function onClick() {
        setData(data);
    }
    return React.createElement(
        window.dash_bootstrap_components.Button,
        {
            onClick,
            color: props.color,
        },
        props.value
    );
};
