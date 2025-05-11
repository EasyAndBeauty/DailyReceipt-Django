from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions


def index(request):
    return HttpResponse("Welcome to DailyReceipt API")


schema_view = get_schema_view(
    openapi.Info(
        title="DailyReceipt API",
        default_version="v1",
        description="DailyReceipt API documentation",
        terms_of_service="https://www.yourapp.com/terms/",
        contact=openapi.Contact(email="dndb3599@gmail.com"),
        license=openapi.License(name="MIT"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    # swagger
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    # admin
    path("admin/", admin.site.urls),
    # index
    path("", index),
    # api
    path(
        "api/",
        include(
            [
                # auth
                path("auth/", include("apps.authentication.urls")),
                # tasks
                path("task/", include("apps.task.urls")),
                # receipt
                path("receipt/", include("apps.receipt.urls")),
            ]
        ),
    ),
]
