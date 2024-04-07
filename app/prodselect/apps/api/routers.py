from __future__ import annotations

from collections import OrderedDict

from django.urls import URLPattern
from django.views import View
from rest_framework.routers import DefaultRouter


class APIRouter(DefaultRouter):
    """
    Customized Default Router to include non-viewset views on root page.

    https://github.com/encode/django-rest-framework/discussions/7830#discussioncomment-7205311
    """

    def __init__(self, single_views: list, *args, **kwargs) -> None:
        self.single_views = single_views
        super().__init__(*args, **kwargs)

    def get_api_root_view(
        self,
        api_urls: list[URLPattern] | None = None,  # noqa: ARG002
    ) -> View:
        """Return a basic root view."""
        api_root_dict = OrderedDict()
        list_name = self.routes[0].name
        for prefix, _viewset, basename in self.registry:
            api_root_dict[prefix] = list_name.format(basename=basename)
        for single_view in self.single_views:
            api_root_dict[single_view["route"]] = single_view["name"]
        return self.APIRootView.as_view(api_root_dict=api_root_dict)
