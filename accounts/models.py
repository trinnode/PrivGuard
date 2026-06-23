from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from accounts.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model with email authentication and consent tracking."""
    class Role(models.TextChoices):
        STUDENT = "student", "Student"
        RESEARCHER = "researcher", "Researcher"
        ADMIN = "admin", "Administrator"

    email = models.EmailField(unique=True, verbose_name="email address")
    full_name = models.CharField(max_length=255, blank=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STUDENT)
    institution = models.CharField(max_length=255, blank=True, help_text="University or institution name")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    consent_granted = models.BooleanField(default=False, verbose_name="Research consent granted")
    consent_date = models.DateTimeField(null=True, blank=True)
    anonymize_requested = models.BooleanField(
        default=False,
        verbose_name="Request identity concealment on exported reports",
        help_text="When enabled, your identity will be hidden on exported versions of your reports.",
    )
    last_password_reset = models.DateTimeField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-date_joined"]

    def __str__(self):
        return self.email

    def record_consent(self):
        self.consent_granted = True
        self.consent_date = timezone.now()
        self.save(update_fields=["consent_granted", "consent_date"])

    def revoke_consent(self):
        self.consent_granted = False
        self.consent_date = None
        self.save(update_fields=["consent_granted", "consent_date"])
