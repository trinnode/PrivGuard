from django.db import models


class Resource(models.Model):
    """Guidance resource for privacy incident support."""
    CATEGORY_CHOICES = [
        ("legal", "Legal Rights & Reporting"),
        ("mental_health", "Mental Health & Wellbeing"),
        ("digital_safety", "Digital Safety Guides"),
        ("academic_support", "Academic Support"),
        ("campus_resources", "Campus Resources"),
        ("emergency", "Emergency Contacts"),
        ("general", "General Guidance"),
    ]

    title = models.CharField(max_length=300)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    external_link = models.URLField(blank=True, help_text="Optional link to external resource")
    contact_phone = models.CharField(
        max_length=100,
        blank=True,
        help_text="Contact phone number (e.g. tel: link friendly)",
    )
    relevance_tags = models.CharField(
        max_length=500,
        blank=True,
        help_text="Comma-separated tags for filtering",
    )
    incident_types = models.CharField(
        max_length=500,
        blank=True,
        help_text="Comma-separated incident classification keys this resource helps with "
                 "(e.g. doxxing, cyberstalking, account_takeover)",
    )
    harm_categories = models.CharField(
        max_length=500,
        blank=True,
        help_text="Comma-separated harm category keys this resource addresses "
                 "(e.g. anxiety, distress, physical_safety)",
    )
    is_visible = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "title"]
        verbose_name = "Resource"
        verbose_name_plural = "Resources"

    def __str__(self):
        return self.title

    def tag_list(self):
        return [t.strip() for t in self.relevance_tags.split(",") if t.strip()]

    def incident_type_list(self):
        return [t.strip() for t in self.incident_types.split(",") if t.strip()]

    def harm_category_list(self):
        return [h.strip() for h in self.harm_categories.split(",") if h.strip()]

    @classmethod
    def recommended_for(cls, incident, limit=4):
        """Return visible resources relevant to an incident's classification and harms.

        Matches on the incident's classification key and any harm categories the
        reporter selected, scoring exact matches highest. Falls back to the most
        recently ordered resources when no targeted match exists so reporters are
        never left with an empty suggestion panel.
        """
        from django.db.models import Q
        keys = [incident.incident_classification]
        harm_keys = list(incident.harms.values_list("harm_category", flat=True))
        candidates = cls.objects.filter(is_visible=True)
        if not keys and not harm_keys:
            return list(candidates[:limit])
        query = Q(incident_types__icontains=keys[0]) if keys else Q()
        for hk in harm_keys:
            query = query | Q(harm_categories__icontains=hk)
        matches = list(candidates.filter(query).order_by("order")[:limit])
        if matches:
            return matches
        # Generic guidance fallback so suggestions are never empty.
        return list(candidates.filter(category__in=["general", "mental_health"]).order_by("order")[:limit])
