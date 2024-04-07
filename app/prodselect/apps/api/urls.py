from django.urls import include, path

from prodselect.apps.api import views
from prodselect.apps.api.routers import APIRouter

single_views = [
    {
        "route": "me/",
        "view": views.MeView.as_view(),
        "name": "me_view",
    },
]

router = APIRouter(single_views=single_views)
router.register(r"products", views.ProductViewSet)
router.register(r"selection", views.UserSelectionSerializerViewSet)

urlpatterns = [
    path("", include(router.urls)),
    *[
        path(route=i["route"], view=i["view"], name=i["name"])
        for i in single_views
    ],
]
