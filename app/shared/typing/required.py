from __future__ import annotations

from typing import Any, TypeVar, overload

__all__ = ["required"]


_T = TypeVar("_T")


@overload
def required(value: _T | None) -> _T: ...


@overload
def required(value: Any, as_type: type[_T]) -> _T: ...


def required(value, as_type=None):
    if value is None:
        raise ValueError("Value is required")
    if as_type is not None and not isinstance(value, as_type):
        msg = f"Expected type '{as_type}', got '{type(value)}'"
        raise TypeError(msg)
    return value
