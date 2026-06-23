from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", TemplateView.as_view(template_name="landing.html"), name="landing"),
    path("about/", TemplateView.as_view(template_name="about.html"), name="about"),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path("incidents/", include("incidents.urls", namespace="incidents")),
    path("resources/", include("resources.urls", namespace="resources")),
    path("reporting/", include("reporting.urls", namespace="reporting")),
    path("dashboard/", include("dashboard.urls", namespace="dashboard")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    re_path(r"^.*$", TemplateView.as_view(template_name="404.html"), name="not_found"),
]

handler404 = "ragnar.views.custom_page_not_found"
