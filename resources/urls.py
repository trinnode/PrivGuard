from django.urls import path
from resources.views import resource_list, resource_detail

app_name = "resources"

urlpatterns = [
    path("", resource_list, name="list"),
    path("<int:pk>/", resource_detail, name="detail"),
]
