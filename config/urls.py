"""
Django URL Configuration
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view

schema_url_patterns = path("api/", include("api.urls"))
urlpatterns = [
    path("", lambda request: redirect("swagger-ui/", permanent=True)),
    path("admin/", admin.site.urls),
    path(
        "openapi/",
        get_schema_view(
            title="API Plerk",
            version="0.1",
            patterns=[schema_url_patterns],
        ),
        name="openapi-schema",
    ),
    path(
        "swagger-ui/",
        TemplateView.as_view(
            template_name="swagger-ui.html",
            extra_context={"schema_url": "openapi-schema"},
        ),
        name="swagger-ui",
    ),
    schema_url_patterns,
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
