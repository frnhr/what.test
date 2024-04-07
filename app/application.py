# noqa: INP001
import logging
import os

import wsgitypes
from django import setup as django_setup
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


def load_ui_app() -> wsgitypes.Application:
    from ui.app import app

    return app.server


application = load_ui_app()

prodselect_app = load_prodselect_app()


# outermost to innermost:
wsgi_middlewares = [
    # (ProxyFix, (), {"x_proto": 1, "x_host": 1}),
    (DispatcherMiddleware, (), {"mounts": {"/backend": prodselect_app}}),
]
for app, args, kwargs in wsgi_middlewares[::-1]:
    application = app(application, *args, **kwargs)
