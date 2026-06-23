from django.urls import path
from incidents.views import (
    incident_list, incident_detail, incident_create, incident_edit,
    incident_delete, incident_update_status,
    admin_list, admin_detail, admin_delete, admin_export,
)

app_name = "incidents"

urlpatterns = [
    path("admin/<str:reference_code>/delete/", admin_delete, name="admin_delete"),
    path("admin/<str:reference_code>/export/", admin_export, name="admin_export"),
    path("admin/<str:reference_code>/", admin_detail, name="admin_detail"),
    path("admin/", admin_list, name="admin_list"),
    path("new/", incident_create, name="create"),
    path("<str:reference_code>/edit/", incident_edit, name="edit"),
    path("<str:reference_code>/delete/", incident_delete, name="delete"),
    path("<str:reference_code>/status/", incident_update_status, name="update_status"),
    path("", incident_list, name="list"),
    path("<str:reference_code>/", incident_detail, name="detail"),
]
