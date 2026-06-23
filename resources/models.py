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
    relevance_tags = models.CharField(
        max_length=500,
        blank=True,
        help_text="Comma-separated tags for filtering",
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
