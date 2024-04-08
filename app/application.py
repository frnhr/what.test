#!/usr/bin/env python
"""
Main WSGI application that serves the UI and the backend.

Serve it with gunicorn or similar.

For development ONLY, run this file directly to start a dev server.
"""

import logging
import os
from functools import reduce

import wsgitypes
from dash import Dash
from django import setup as django_setup
from werkzeug import run_simple
from werkzeug.middleware.dispatcher import DispatcherMiddleware

__all__ = ["application"]


logger = logging.getLogger(__name__)


# See .env for details
DEBUG = os.environ.get("ENVIRONMENT") == "development"
logger.info("DEBUG: %s", DEBUG)


def load_prodselect_app() -> wsgitypes.Application:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "prodselect.settings")
    django_setup()

    from prodselect.wsgi import application

    return application


def load_ui_dash() -> Dash:
    from ui.app import app

    return app


ui_app_dash = load_ui_dash()

prodselect_app = load_prodselect_app()


# middlewares (outermost to innermost), and the base app at the end:
wsgi_stack = [
    # (ProxyFix, (), {"x_proto": 1, "x_host": 1}),
    (DispatcherMiddleware, (), {"mounts": {"/backend": prodselect_app}}),
    ui_app_dash.server,
]
application = reduce(
    lambda _app, _mid: _mid[0](_app, *_mid[1], **_mid[2]),
    wsgi_stack[-2::-1],
    wsgi_stack[-1],
)


if __name__ == "__main__":
    ui_app_dash.enable_dev_tools(debug=True)
    run_simple(
        "localhost",
        8000,
        application,
        use_reloader=True,
        use_debugger=True,
        reloader_type="watchdog",
        threaded=True,
    )
