from __future__ import annotations

from collections.abc import Callable
from itertools import compress

from dash import ClientsideFunction, Dash
from dash_extensions.enrich import CallbackBlueprint, Trigger, TriggerTransform

__all__ = [
    "add_clientside_decorator",
    "enable_dash_extensions_clientside_trigger",
]


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


def enable_dash_extensions_clientside_trigger() -> None:
    """
    Allow use of Trigger with clientside callbacks.

    https://github.com/emilhe/dash-extensions/pull/318
    """

    class ClientsideTrigger:
        def apply_clientside(
            self,
            callbacks: list[CallbackBlueprint],
        ) -> list[CallbackBlueprint]:
            for callback in callbacks:
                is_not_trigger = [
                    not isinstance(item, Trigger) for item in callback.inputs
                ]
                # Check if any triggers are there.
                if all(is_not_trigger):
                    continue
                # If so, filter the callback args.
                args = [f"arg{i}" for i in range(len(callback.inputs))]
                filtered_args = compress(args, is_not_trigger)
                if isinstance(callback.f, ClientsideFunction):
                    callback.f = (
                        f"window.dash_clientside"
                        f"['{callback.f.namespace}']"
                        f"['{callback.f.function_name}']"
                    )
                callback.f = f"""
function({", ".join(args)}) {{
    const func = {callback.f};
    return func({", ".join(filtered_args)});
}}
                """.strip()
            return callbacks

    if ClientsideTrigger not in TriggerTransform.__bases__:
        TriggerTransform.__bases__ = (
            ClientsideTrigger,
            *TriggerTransform.__bases__,
        )
