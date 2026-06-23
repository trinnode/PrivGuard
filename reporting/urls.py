from django.urls import path
from reporting.views import export_pdf, admin_export_bulk

app_name = "reporting"

urlpatterns = [
    path("export/all/pdf/", admin_export_bulk, name="admin_export_bulk"),
    path("export/<str:reference_code>/pdf/", export_pdf, name="export_pdf"),
]
