from collections.abc import Callable

from dash import Dash

__all__ = ["add_clientside_decorator"]


def add_clientside_decorator(app: Dash) -> None:
    """
    Syntactic sugar for clientside callbacks.

    Makes it easier to convert serverside callbacks to clientside callbacks, by
    providing a syntax for clientside callbacks that is similar to that for
    serverside callbacks.

    Instead of:
    ``` python
    app.clientside_callback(
        '''(arg1, arg2) => {
            ...
            return ...
        '''
        Output("output1", "value"),
        Input("input1", "value"),
        Input("input2", "value"),
    )
    ```

    we can now write:

    ``` python
    @app.clientside(
        Output("output1", "value"),
        Input("input1", "value"),
        Input("input2", "value"),
    )
    def my_func():
        return '''
        (arg1, arg2) => {
            ...
            return ...
        '''
    )
    ```
    """

    def clientside_decorator(*args, **kwargs) -> Callable:
        def wrapper(func: Callable) -> None:
            clientside_function = func()
            return app.clientside_callback(
                clientside_function,
                *args,
                **kwargs,
            )

        return wrapper

    app.clientside = clientside_decorator
