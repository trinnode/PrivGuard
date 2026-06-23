from django.contrib import admin
from resources.models import Resource


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "is_visible", "order")
    list_filter = ("category", "is_visible")
    search_fields = ("title", "description", "relevance_tags")
    list_editable = ("order", "is_visible")
