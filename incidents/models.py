from django.db import models
from django.conf import settings
from incidents.taxonomy import (
    PLATFORM_CATEGORIES,
    INCIDENT_CLASSIFICATIONS,
    HARM_CATEGORIES,
    SEVERITY_LEVELS,
    DURATION_CHOICES,
    ACTOR_CHOICES,
)


def evidence_upload_path(instance, filename):
    uid = instance.user.id if instance.user else "anonymous"
    return f"evidence/user_{uid}/{instance.id}_{filename}"


class Incident(models.Model):
    """Core incident report documenting a digital privacy violation."""
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("submitted", "Submitted"),
        ("under_review", "Under Review"),
        ("resolved", "Resolved"),
        ("closed", "Closed"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="incidents",
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="submitted",
        verbose_name="Incident Status",
    )
    platform_category = models.CharField(
        max_length=50,
        choices=PLATFORM_CATEGORIES,
        verbose_name="Platform or service where the violation occurred",
    )
    platform_name = models.CharField(
        max_length=200,
        blank=True,
        help_text="Specific platform name if not listed above",
    )
    date_of_occurrence = models.DateField(verbose_name="When did this happen?")
    incident_classification = models.CharField(
        max_length=50,
        choices=INCIDENT_CLASSIFICATIONS,
        verbose_name="Type of privacy violation",
    )
    narrative = models.TextField(
        verbose_name="Describe what happened",
        help_text="Please describe the incident in as much detail as you feel comfortable sharing.",
    )
    actor_involvement = models.CharField(
        max_length=30,
        choices=ACTOR_CHOICES,
        verbose_name="Who was involved?",
    )
    actor_description = models.CharField(
        max_length=300,
        blank=True,
        help_text="Optional: any additional details about the person or people involved",
    )
    severity_rating = models.IntegerField(
        choices=SEVERITY_LEVELS,
        verbose_name="How severe was this incident for you?",
    )
    evidence_file = models.FileField(
        upload_to=evidence_upload_path,
        blank=True,
        help_text="Attach evidence (screenshot, document). Max 5MB. Allowed: PNG, JPEG, PDF",
    )
    is_anonymous = models.BooleanField(
        default=False,
        verbose_name="Submit anonymously (your identity will not be stored with this report)",
    )
    anonymize_requested = models.BooleanField(
        default=False,
        verbose_name="Request identity concealment on exported reports",
        help_text="When enabled, your identity will be hidden in any exported version of this report.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reference_code = models.CharField(max_length=20, unique=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Incident Report"
        verbose_name_plural = "Incident Reports"

    def __str__(self):
        return f"{self.reference_code or 'Draft'} - {self.get_incident_classification_display()}"

    def save(self, *args, **kwargs):
        if not self.reference_code:
            self.reference_code = self._generate_reference()
        super().save(*args, **kwargs)

    def _generate_reference(self):
        import uuid
        return f"MMR-{uuid.uuid4().hex[:8].upper()}"

    def harms_summary(self):
        return ", ".join([h.get_harm_category_display() for h in self.harms.all()])


class Harm(models.Model):
    """Classification of harms associated with an incident."""
    HARM_TYPE_CHOICES = sorted(set(
        (t, t.capitalize()) for _, _, t in HARM_CATEGORIES
    ))

    incident = models.ForeignKey(
        Incident,
        on_delete=models.CASCADE,
        related_name="harms",
    )
    harm_category = models.CharField(
        max_length=50,
        choices=[(k, v) for k, v, t in HARM_CATEGORIES],
        verbose_name="What kind of harm did you experience?",
    )
    severity_score = models.IntegerField(
        choices=SEVERITY_LEVELS,
        verbose_name="How severe is this specific harm?",
    )
    duration = models.CharField(
        max_length=30,
        choices=DURATION_CHOICES,
        verbose_name="How long has this harm lasted?",
    )
    elaboration = models.TextField(
        blank=True,
        verbose_name="Additional details about this harm (optional)",
        help_text="Share anything else about how this harm affected you.",
    )

    class Meta:
        verbose_name = "Harm Classification"
        verbose_name_plural = "Harm Classifications"

    def __str__(self):
        return f"{self.get_harm_category_display()} ({self.get_severity_score_display()})"


class AuditLog(models.Model):
    """Security audit log for tracking system access and modifications."""
    EVENT_TYPES = [
        ("login", "Login"),
        ("logout", "Logout"),
        ("incident_create", "Incident Created"),
        ("incident_view", "Incident Viewed"),
        ("incident_export", "Incident Exported"),
        ("account_delete", "Account Deleted"),
        ("consent_change", "Consent Changed"),
        ("failed_login", "Failed Login"),
        ("password_reset", "Password Reset"),
        ("admin_action", "Admin Action"),
    ]

    event_type = models.CharField(max_length=30, choices=EVENT_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    action_summary = models.TextField(blank=True)
    ip_hash = models.CharField(max_length=64, blank=True, help_text="SHA-256 hash of IP address")

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = "Audit Log Entry"
        verbose_name_plural = "Audit Logs"

    def __str__(self):
        return f"{self.get_event_type_display()} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
