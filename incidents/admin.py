from django.contrib import admin
from incidents.models import Incident, Harm, AuditLog


class HarmInline(admin.TabularInline):
    model = Harm
    extra = 1


@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = ("reference_code", "user", "incident_classification", "severity_rating", "created_at")
    list_filter = ("incident_classification", "severity_rating", "platform_category", "created_at")
    search_fields = ("reference_code", "user__email", "narrative")
    readonly_fields = ("reference_code", "created_at", "updated_at")
    inlines = [HarmInline]
    date_hierarchy = "created_at"


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("event_type", "user", "timestamp", "action_summary")
    list_filter = ("event_type", "timestamp")
    search_fields = ("user__email", "action_summary")
    readonly_fields = ("timestamp",)
    date_hierarchy = "timestamp"
