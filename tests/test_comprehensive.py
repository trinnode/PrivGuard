"""
RAGNER Comprehensive Test Suite
Tests all workflows, edge cases, and debugging scenarios.
"""
import os
import hashlib
from datetime import datetime, timedelta
from io import BytesIO

from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from django.db import connection

from incidents.models import Incident, Harm, AuditLog
from incidents.taxonomy import (
    PLATFORM_CATEGORIES, INCIDENT_CLASSIFICATIONS, HARM_CATEGORIES,
    SEVERITY_LEVELS, DURATION_CHOICES, ACTOR_CHOICES,
    get_harm_by_category, get_harm_type_choices,
)
from incidents.templatetags.incident_tags import get_item, harm_type
from resources.models import Resource
from reporting.pdf_generator import generate_incident_report, generate_text_summary
from accounts.models import User
from ragnar.middleware import SessionTimeoutMiddleware

User = get_user_model()


# ============================================================
# USER MODEL TESTS
# ============================================================

class UserModelComprehensiveTests(TestCase):
    """Tests for the custom User model."""

    def setUp(self):
        self.user = User.objects.create_user(
            email="test@student.edu.ng",
            password="testpass123",
            full_name="Test Student",
            institution="University of Lagos",
        )

    def test_user_creation(self):
        self.assertEqual(self.user.email, "test@student.edu.ng")
        self.assertTrue(self.user.check_password("testpass123"))
        self.assertFalse(self.user.consent_granted)
        self.assertIsNone(self.user.consent_date)
        self.assertEqual(self.user.role, "student")
        self.assertFalse(self.user.anonymize_requested)
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)

    def test_superuser_creation(self):
        admin = User.objects.create_superuser(
            email="admin@uni.edu.ng",
            password="adminpass123",
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
        self.assertEqual(admin.role, "admin")

    def test_email_normalization(self):
        user = User.objects.create_user(
            email="Test@Uni.Edu.NG",
            password="testpass123",
        )
        self.assertEqual(user.email, "test@uni.edu.ng")

    def test_email_uniqueness(self):
        with self.assertRaises(Exception):
            User.objects.create_user(
                email="test@student.edu.ng",
                password="anotherpass",
            )

    def test_consent_toggle(self):
        self.user.record_consent()
        self.assertTrue(self.user.consent_granted)
        self.assertIsNotNone(self.user.consent_date)

        self.user.revoke_consent()
        self.assertFalse(self.user.consent_granted)
        self.assertIsNone(self.user.consent_date)

    def test_anonymize_toggle(self):
        self.assertFalse(self.user.anonymize_requested)
        self.user.anonymize_requested = True
        self.user.save(update_fields=["anonymize_requested"])
        self.user.refresh_from_db()
        self.assertTrue(self.user.anonymize_requested)

    def test_str_representation(self):
        self.assertEqual(str(self.user), "test@student.edu.ng")

    def test_ordering(self):
        user2 = User.objects.create_user(
            email="second@student.edu.ng",
            password="testpass123",
        )
        users = list(User.objects.all())
        self.assertEqual(users[0], user2)  # Most recent first
        self.assertEqual(users[1], self.user)


# ============================================================
# INCIDENT MODEL TESTS
# ============================================================

class IncidentModelComprehensiveTests(TestCase):
    """Tests for the Incident model."""

    def setUp(self):
        self.user = User.objects.create_user(
            email="student@uni.edu.ng",
            password="testpass123",
        )

    def test_incident_creation(self):
        incident = Incident.objects.create(
            user=self.user,
            platform_category="social_media",
            date_of_occurrence="2025-09-15",
            incident_classification="doxxing",
            narrative="My personal information was shared online without consent.",
            actor_involvement="known_person",
            severity_rating=3,
        )
        self.assertTrue(incident.reference_code.startswith("MMR-"))
        self.assertEqual(len(incident.reference_code), 12)  # MMR- + 8 hex chars
        self.assertEqual(incident.user, self.user)
        self.assertEqual(incident.harms.count(), 0)
        self.assertFalse(incident.is_anonymous)

    def test_reference_code_uniqueness(self):
        codes = set()
        for i in range(10):
            incident = Incident.objects.create(
                user=self.user,
                platform_category="email",
                date_of_occurrence="2025-01-01",
                incident_classification="phishing",
                narrative=f"Test {i}",
                actor_involvement="stranger",
                severity_rating=2,
            )
            codes.add(incident.reference_code)
        self.assertEqual(len(codes), 10)  # All unique

    def test_reference_code_format(self):
        incident = Incident.objects.create(
            user=self.user,
            platform_category="email",
            date_of_occurrence="2025-01-01",
            incident_classification="phishing",
            narrative="Test",
            actor_involvement="stranger",
            severity_rating=2,
        )
        self.assertRegex(incident.reference_code, r'^MMR-[0-9A-F]{8}$')

    def test_harm_summary(self):
        incident = Incident.objects.create(
            user=self.user,
            platform_category="social_media",
            date_of_occurrence="2025-09-15",
            incident_classification="doxxing",
            narrative="Test",
            actor_involvement="known_person",
            severity_rating=3,
        )
        Harm.objects.create(
            incident=incident,
            harm_category="anxiety",
            severity_score=2,
            duration="repeated_short",
        )
        Harm.objects.create(
            incident=incident,
            harm_category="reputation",
            severity_score=3,
            duration="repeated_long",
        )
        summary = incident.harms_summary()
        self.assertIn("Anxiety", summary)
        self.assertIn("Reputation", summary)

    def test_str_representation(self):
        incident = Incident.objects.create(
            user=self.user,
            platform_category="social_media",
            date_of_occurrence="2025-09-15",
            incident_classification="doxxing",
            narrative="Test",
            actor_involvement="known_person",
            severity_rating=3,
        )
        self.assertIn(incident.reference_code, str(incident))
        self.assertIn("Doxxing", str(incident))

    def test_ordering(self):
        i1 = Incident.objects.create(
            user=self.user,
            platform_category="email",
            date_of_occurrence="2025-01-01",
            incident_classification="phishing",
            narrative="First",
            actor_involvement="stranger",
            severity_rating=2,
        )
        i2 = Incident.objects.create(
            user=self.user,
            platform_category="email",
            date_of_occurrence="2025-01-02",
            incident_classification="phishing",
            narrative="Second",
            actor_involvement="stranger",
            severity_rating=2,
        )
        incidents = list(Incident.objects.filter(user=self.user))
        self.assertEqual(incidents[0], i2)  # Most recent first
        self.assertEqual(incidents[1], i1)


# ============================================================
# HARM MODEL TESTS
# ============================================================

class HarmModelComprehensiveTests(TestCase):
    """Tests for the Harm model."""

    def setUp(self):
        self.user = User.objects.create_user(
            email="t@t.com",
            password="testpass123",
        )
        self.incident = Incident.objects.create(
            user=self.user,
            platform_category="social_media",
            date_of_occurrence="2025-09-15",
            incident_classification="doxxing",
            narrative="Test narrative.",
            actor_involvement="known_person",
            severity_rating=3,
        )

    def test_harm_creation(self):
        harm = Harm.objects.create(
            incident=self.incident,
            harm_category="anxiety",
            severity_score=2,
            duration="repeated_short",
            elaboration="I felt anxious for weeks.",
        )
        self.assertEqual(harm.incident, self.incident)
        self.assertIn("Anxiety", harm.get_harm_category_display())

    def test_multiple_harms_per_incident(self):
        Harm.objects.create(
            incident=self.incident,
            harm_category="anxiety",
            severity_score=2,
            duration="repeated_short",
        )
        Harm.objects.create(
            incident=self.incident,
            harm_category="reputation",
            severity_score=3,
            duration="repeated_long",
        )
        self.assertEqual(self.incident.harms.count(), 2)

    def test_harm_cascade_delete(self):
        Harm.objects.create(
            incident=self.incident,
            harm_category="anxiety",
            severity_score=2,
            duration="repeated_short",
        )
        incident_id = self.incident.id
        self.incident.delete()
        self.assertEqual(Harm.objects.filter(incident_id=incident_id).count(), 0)


# ============================================================
# AUDIT LOG TESTS
# ============================================================

class AuditLogComprehensiveTests(TestCase):
    """Tests for the AuditLog model."""

    def setUp(self):
        self.user = User.objects.create_user(
            email="admin@r.com",
            password="testpass123",
        )

    def test_audit_log_creation(self):
        log = AuditLog.objects.create(
            event_type="login",
            user=self.user,
            action_summary="User logged in",
            ip_hash="abc123",
        )
        self.assertEqual(log.event_type, "login")
        self.assertIsNotNone(log.timestamp)

    def test_audit_log_null_user(self):
        log = AuditLog.objects.create(
            event_type="incident_create",
            user=None,
            action_summary="Anonymous incident created",
            ip_hash="def456",
        )
        self.assertIsNone(log.user)

    def test_ip_hashing(self):
        ip = "192.168.1.1"
        expected_hash = hashlib.sha256(ip.encode()).hexdigest()
        log = AuditLog.objects.create(
            event_type="login",
            user=self.user,
            action_summary="Test",
            ip_hash=expected_hash,
        )
        self.assertEqual(log.ip_hash, expected_hash)


# ============================================================
# TAXONOMY TESTS
# ============================================================

class TaxonomyTests(TestCase):
    """Tests for taxonomy constants and helper functions."""

    def test_platform_categories_count(self):
        self.assertEqual(len(PLATFORM_CATEGORIES), 9)

    def test_incident_classifications_count(self):
        self.assertEqual(len(INCIDENT_CLASSIFICATIONS), 14)

    def test_harm_categories_count(self):
        self.assertEqual(len(HARM_CATEGORIES), 17)

    def test_harm_types(self):
        psych = [h for h in HARM_CATEGORIES if h[2] == "psychological"]
        tangible = [h for h in HARM_CATEGORIES if h[2] == "tangible"]
        other = [h for h in HARM_CATEGORIES if h[2] == "other"]
        self.assertEqual(len(psych), 9)
        self.assertEqual(len(tangible), 7)
        self.assertEqual(len(other), 1)

    def test_severity_levels(self):
        self.assertEqual(len(SEVERITY_LEVELS), 4)
        for level, _ in SEVERITY_LEVELS:
            self.assertIn(level, [1, 2, 3, 4])

    def test_duration_choices(self):
        self.assertEqual(len(DURATION_CHOICES), 5)

    def test_actor_choices(self):
        self.assertEqual(len(ACTOR_CHOICES), 8)

    def test_get_harm_by_category(self):
        result = get_harm_by_category("anxiety")
        self.assertIn("Anxiety", result[1])

    def test_get_harm_by_category_unknown(self):
        result = get_harm_by_category("nonexistent")
        self.assertEqual(result, ("Unknown", "Unknown category", "other"))

    def test_get_harm_type_choices_all(self):
        choices = get_harm_type_choices()
        self.assertEqual(len(choices), 17)

    def test_get_harm_type_choices_filtered(self):
        psych = get_harm_type_choices("psychological")
        self.assertEqual(len(psych), 9)


# ============================================================
# TEMPLATE TAG TESTS
# ============================================================

class TemplateTagTests(TestCase):
    """Tests for custom template tags and filters."""

    def test_get_item_filter(self):
        data = {"key": "value"}
        self.assertEqual(get_item(data, "key"), "value")

    def test_get_item_missing_key(self):
        data = {"key": "value"}
        self.assertIsNone(get_item(data, "missing"))

    def test_harm_type_filter(self):
        self.assertEqual(harm_type("anxiety"), "psychological")
        self.assertEqual(harm_type("reputation"), "tangible")
        self.assertEqual(harm_type("other_harm"), "other")
        self.assertEqual(harm_type("nonexistent"), "other")


# ============================================================
# AUTHENTICATION FLOW TESTS
# ============================================================

class AuthenticationComprehensiveTests(TestCase):
    """Comprehensive tests for authentication flows."""

    def setUp(self):
        self.client = Client()
        self.register_url = reverse("accounts:register")
        self.login_url = reverse("accounts:login")
        self.logout_url = reverse("accounts:logout")
        self.profile_url = reverse("accounts:profile")

    def test_registration_page_loads(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)

    def test_successful_registration(self):
        response = self.client.post(self.register_url, {
            "email": "newstudent@uni.edu.ng",
            "full_name": "New Student",
            "institution": "University of Ibadan",
            "password1": "securepass123",
            "password2": "securepass123",
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(email="newstudent@uni.edu.ng").exists())

    def test_registration_with_consent(self):
        self.client.post(self.register_url, {
            "email": "consent@uni.edu.ng",
            "full_name": "Consent Student",
            "institution": "University of Lagos",
            "password1": "securepass123",
            "password2": "securepass123",
            "consent": True,
        })
        user = User.objects.get(email="consent@uni.edu.ng")
        self.assertTrue(user.consent_granted)
        self.assertIsNotNone(user.consent_date)

    def test_registration_duplicate_email(self):
        User.objects.create_user(email="existing@uni.edu.ng", password="testpass123")
        response = self.client.post(self.register_url, {
            "email": "existing@uni.edu.ng",
            "password1": "securepass123",
            "password2": "securepass123",
        })
        self.assertEqual(response.status_code, 200)  # Form re-rendered
        self.assertFalse(User.objects.filter(email="existing@uni.edu.ng").count() > 1)

    def test_registration_mismatched_passwords(self):
        response = self.client.post(self.register_url, {
            "email": "mismatch@uni.edu.ng",
            "password1": "password123",
            "password2": "different123",
        })
        self.assertEqual(response.status_code, 200)

    def test_registration_short_password(self):
        response = self.client.post(self.register_url, {
            "email": "short@uni.edu.ng",
            "password1": "short",
            "password2": "short",
        })
        self.assertEqual(response.status_code, 200)

    def test_login_page_loads(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)

    def test_successful_login(self):
        User.objects.create_user(email="user@uni.edu.ng", password="testpass123")
        response = self.client.post(self.login_url, {
            "username": "user@uni.edu.ng",
            "password": "testpass123",
        }, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_failed_login(self):
        response = self.client.post(self.login_url, {
            "username": "nonexistent@uni.edu.ng",
            "password": "wrongpass",
        })
        self.assertEqual(response.status_code, 200)  # Form re-rendered

    def test_logout(self):
        User.objects.create_user(email="logout@uni.edu.ng", password="testpass123")
        self.client.login(email="logout@uni.edu.ng", password="testpass123")
        response = self.client.get(self.logout_url, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_profile_requires_auth(self):
        response = self.client.get(self.profile_url)
        self.assertNotEqual(response.status_code, 200)

    def test_profile_loads(self):
        User.objects.create_user(email="profile@uni.edu.ng", password="testpass123")
        self.client.login(email="profile@uni.edu.ng", password="testpass123")
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)

    def test_profile_update(self):
        User.objects.create_user(email="update@uni.edu.ng", password="testpass123")
        self.client.login(email="update@uni.edu.ng", password="testpass123")
        response = self.client.post(self.profile_url, {
            "full_name": "Updated Name",
            "institution": "Updated Institution",
        }, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_consent_toggle(self):
        user = User.objects.create_user(email="toggle@uni.edu.ng", password="testpass123")
        self.client.login(email="toggle@uni.edu.ng", password="testpass123")
        self.assertFalse(user.consent_granted)
        response = self.client.post(reverse("accounts:toggle_consent"), follow=True)
        self.assertEqual(response.status_code, 200)
        user.refresh_from_db()
        self.assertTrue(user.consent_granted)

    def test_anonymize_toggle(self):
        user = User.objects.create_user(email="anon@uni.edu.ng", password="testpass123")
        self.client.login(email="anon@uni.edu.ng", password="testpass123")
        self.assertFalse(user.anonymize_requested)
        response = self.client.post(reverse("accounts:toggle_anonymize"), follow=True)
        self.assertEqual(response.status_code, 200)
        user.refresh_from_db()
        self.assertTrue(user.anonymize_requested)


# ============================================================
# INCIDENT WORKFLOW TESTS
# ============================================================

class IncidentWorkflowComprehensiveTests(TestCase):
    """Comprehensive tests for incident reporting workflow."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="reporter@uni.edu.ng",
            password="testpass123",
        )
        self.client.login(email="reporter@uni.edu.ng", password="testpass123")

    def test_incident_list_requires_auth(self):
        self.client.logout()
        response = self.client.get(reverse("incidents:list"))
        self.assertNotEqual(response.status_code, 200)

    def test_incident_list_loads(self):
        response = self.client.get(reverse("incidents:list"))
        self.assertEqual(response.status_code, 200)

    def test_create_incident_basic(self):
        response = self.client.post(reverse("incidents:create"), {
            "platform_category": "social_media",
            "date_of_occurrence": "2025-10-01",
            "incident_classification": "doxxing",
            "narrative": "My personal info was leaked.",
            "actor_involvement": "known_person",
            "severity_rating": "3",
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Incident.objects.filter(user=self.user).count(), 1)

    def test_create_incident_with_harm(self):
        response = self.client.post(reverse("incidents:create"), {
            "platform_category": "social_media",
            "date_of_occurrence": "2025-10-01",
            "incident_classification": "doxxing",
            "narrative": "Test.",
            "actor_involvement": "known_person",
            "severity_rating": "3",
            "harm_sel": ["anxiety"],
            "harm_severity_anxiety": "2",
            "harm_duration_anxiety": "repeated_short",
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        incident = Incident.objects.get(user=self.user)
        self.assertEqual(incident.harms.count(), 1)

    def test_create_incident_with_multiple_harms(self):
        response = self.client.post(reverse("incidents:create"), {
            "platform_category": "social_media",
            "date_of_occurrence": "2025-10-01",
            "incident_classification": "doxxing",
            "narrative": "Test.",
            "actor_involvement": "known_person",
            "severity_rating": "3",
            "harm_sel": ["anxiety", "reputation"],
            "harm_severity_anxiety": "2",
            "harm_duration_anxiety": "repeated_short",
            "harm_severity_reputation": "3",
            "harm_duration_reputation": "repeated_long",
        }, follow=True)
        incident = Incident.objects.get(user=self.user)
        self.assertEqual(incident.harms.count(), 2)

    def test_create_incident_with_evidence(self):
        image = SimpleUploadedFile(
            "test.png",
            b"\x89PNG\r\n\x1a\n" + b"\x00" * 100,
            content_type="image/png",
        )
        response = self.client.post(reverse("incidents:create"), {
            "platform_category": "social_media",
            "date_of_occurrence": "2025-10-01",
            "incident_classification": "doxxing",
            "narrative": "Test.",
            "actor_involvement": "known_person",
            "severity_rating": "3",
            "evidence_file": image,
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        incident = Incident.objects.get(user=self.user)
        self.assertTrue(incident.evidence_file)

    def test_incident_detail_loads(self):
        incident = Incident.objects.create(
            user=self.user,
            platform_category="social_media",
            date_of_occurrence="2025-10-01",
            incident_classification="doxxing",
            narrative="Test.",
            actor_involvement="known_person",
            severity_rating=3,
        )
        response = self.client.get(
            reverse("incidents:detail", args=[incident.reference_code])
        )
        self.assertEqual(response.status_code, 200)

    def test_incident_detail_wrong_user(self):
        other_user = User.objects.create_user(
            email="other@uni.edu.ng",
            password="testpass123",
        )
        incident = Incident.objects.create(
            user=other_user,
            platform_category="social_media",
            date_of_occurrence="2025-10-01",
            incident_classification="doxxing",
            narrative="Test.",
            actor_involvement="known_person",
            severity_rating=3,
        )
        response = self.client.get(
            reverse("incidents:detail", args=[incident.reference_code])
        )
        self.assertNotEqual(response.status_code, 200)

    def test_anonymous_incident_creation(self):
        self.client.logout()
        response = self.client.post(reverse("incidents:create"), {
            "platform_category": "social_media",
            "date_of_occurrence": "2025-10-01",
            "incident_classification": "doxxing",
            "narrative": "Anonymous report.",
            "actor_involvement": "stranger",
            "severity_rating": "2",
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        incident = Incident.objects.first()
        self.assertIsNone(incident.user)
        self.assertTrue(incident.is_anonymous)


# ============================================================
# ADMIN WORKFLOW TESTS
# ============================================================

class AdminWorkflowTests(TestCase):
    """Tests for admin-only views."""

    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_user(
            email="admin@uni.edu.ng",
            password="adminpass123",
            role="admin",
        )
        self.regular_user = User.objects.create_user(
            email="user@uni.edu.ng",
            password="userpass123",
        )
        self.incident = Incident.objects.create(
            user=self.regular_user,
            platform_category="social_media",
            date_of_occurrence="2025-10-01",
            incident_classification="doxxing",
            narrative="Test.",
            actor_involvement="known_person",
            severity_rating=3,
        )

    def test_admin_list_requires_admin_role(self):
        self.client.login(email="user@uni.edu.ng", password="userpass123")
        response = self.client.get(reverse("incidents:admin_list"))
        self.assertNotEqual(response.status_code, 200)

    def test_admin_list_loads(self):
        self.client.login(email="admin@uni.edu.ng", password="adminpass123")
        response = self.client.get(reverse("incidents:admin_list"))
        self.assertEqual(response.status_code, 200)

    def test_admin_detail_loads(self):
        self.client.login(email="admin@uni.edu.ng", password="adminpass123")
        response = self.client.get(
            reverse("incidents:admin_detail", args=[self.incident.reference_code])
        )
        self.assertEqual(response.status_code, 200)

    def test_admin_delete(self):
        self.client.login(email="admin@uni.edu.ng", password="adminpass123")
        response = self.client.post(
            reverse("incidents:admin_delete", args=[self.incident.reference_code]),
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Incident.objects.filter(pk=self.incident.pk).exists())

    def test_admin_export(self):
        self.client.login(email="admin@uni.edu.ng", password="adminpass123")
        response = self.client.get(
            reverse("incidents:admin_export", args=[self.incident.reference_code])
        )
        self.assertEqual(response.status_code, 200)


# ============================================================
# DASHBOARD TESTS
# ============================================================

class DashboardComprehensiveTests(TestCase):
    """Tests for dashboard functionality."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="dashboard@uni.edu.ng",
            password="testpass123",
        )
        self.client.login(email="dashboard@uni.edu.ng", password="testpass123")

    def test_dashboard_requires_auth(self):
        self.client.logout()
        response = self.client.get(reverse("dashboard:home"))
        self.assertNotEqual(response.status_code, 200)

    def test_dashboard_loads(self):
        response = self.client.get(reverse("dashboard:home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard/home.html")

    def test_dashboard_with_incidents(self):
        for i in range(3):
            incident = Incident.objects.create(
                user=self.user,
                platform_category="social_media",
                date_of_occurrence="2025-10-01",
                incident_classification="doxxing",
                narrative=f"Test {i}.",
                actor_involvement="known_person",
                severity_rating=3,
            )
            Harm.objects.create(
                incident=incident,
                harm_category="anxiety",
                severity_score=2,
                duration="repeated_short",
            )
        response = self.client.get(reverse("dashboard:home"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["total_incidents"], 3)

    def test_dashboard_empty(self):
        response = self.client.get(reverse("dashboard:home"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["total_incidents"], 0)


# ============================================================
# RESOURCE TESTS
# ============================================================

class ResourceComprehensiveTests(TestCase):
    """Tests for resource library."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="resource@uni.edu.ng",
            password="testpass123",
        )
        self.client.login(email="resource@uni.edu.ng", password="testpass123")
        self.resource = Resource.objects.create(
            title="Test Resource",
            category="legal",
            description="Test description.",
            is_visible=True,
            order=1,
        )

    def test_resource_list_requires_auth(self):
        self.client.logout()
        response = self.client.get(reverse("resources:list"))
        self.assertNotEqual(response.status_code, 200)

    def test_resource_list_loads(self):
        response = self.client.get(reverse("resources:list"))
        self.assertEqual(response.status_code, 200)

    def test_resource_list_filter(self):
        response = self.client.get(reverse("resources:list") + "?category=legal")
        self.assertEqual(response.status_code, 200)

    def test_resource_detail_loads(self):
        response = self.client.get(
            reverse("resources:detail", args=[self.resource.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_resource_detail_hidden(self):
        self.resource.is_visible = False
        self.resource.save()
        response = self.client.get(
            reverse("resources:detail", args=[self.resource.pk])
        )
        self.assertNotEqual(response.status_code, 200)


# ============================================================
# PDF EXPORT TESTS
# ============================================================

class PDFExportTests(TestCase):
    """Tests for PDF generation."""

    def setUp(self):
        self.user = User.objects.create_user(
            email="export@uni.edu.ng",
            password="testpass123",
        )
        self.incident = Incident.objects.create(
            user=self.user,
            platform_category="social_media",
            date_of_occurrence="2025-10-01",
            incident_classification="doxxing",
            narrative="Test narrative for PDF export.",
            actor_involvement="known_person",
            severity_rating=3,
        )
        Harm.objects.create(
            incident=self.incident,
            harm_category="anxiety",
            severity_score=2,
            duration="repeated_short",
            elaboration="Felt anxious for weeks.",
        )

    def test_pdf_generation(self):
        pdf_buffer = generate_incident_report(self.incident)
        self.assertIsNotNone(pdf_buffer)
        content = pdf_buffer.read()
        self.assertTrue(len(content) > 0)
        self.assertIn(b'%PDF', content[:10])

    def test_text_fallback_generation(self):
        text = generate_text_summary(self.incident)
        self.assertIn(self.incident.reference_code, text)
        self.assertIn("Test narrative for PDF export.", text)

    def test_pdf_export_view(self):
        self.client.login(email="export@uni.edu.ng", password="testpass123")
        response = self.client.get(
            reverse("reporting:export_pdf", args=[self.incident.reference_code])
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")


# ============================================================
# SESSION TIMEOUT MIDDLEWARE TESTS
# ============================================================

class SessionTimeoutTests(TestCase):
    """Tests for session timeout middleware."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="timeout@uni.edu.ng",
            password="testpass123",
        )

    def test_session_timeout_redirects(self):
        self.client.login(email="timeout@uni.edu.ng", password="testpass123")
        session = self.client.session
        session["last_activity"] = (timezone.now() - timedelta(minutes=16)).timestamp()
        session.save()
        response = self.client.get(reverse("dashboard:home"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_session_active_no_redirect(self):
        self.client.login(email="timeout@uni.edu.ng", password="testpass123")
        session = self.client.session
        session["last_activity"] = timezone.now().timestamp()
        session.save()
        response = self.client.get(reverse("dashboard:home"))
        self.assertEqual(response.status_code, 200)


# ============================================================
# SECURITY TESTS
# ============================================================

class SecurityTests(TestCase):
    """Tests for security features."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="security@uni.edu.ng",
            password="testpass123",
        )

    def test_csrf_cookie_set(self):
        self.client.get(reverse("landing"))
        self.assertIn("csrftoken", self.client.cookies)

    def test_session_cookie_httponly(self):
        self.client.login(email="security@uni.edu.ng", password="testpass123")
        self.assertTrue(self.client.cookies["sessionid"].get("httponly"))

    def test_file_upload_validation_too_large(self):
        self.client.login(email="security@uni.edu.ng", password="testpass123")
        large_file = SimpleUploadedFile(
            "large.pdf",
            b"\x00" * (6 * 1024 * 1024),  # 6MB
            content_type="application/pdf",
        )
        response = self.client.post(reverse("incidents:create"), {
            "platform_category": "social_media",
            "date_of_occurrence": "2025-10-01",
            "incident_classification": "doxxing",
            "narrative": "Test.",
            "actor_involvement": "known_person",
            "severity_rating": "3",
            "evidence_file": large_file,
        })
        self.assertEqual(response.status_code, 200)  # Form re-rendered

    def test_file_upload_validation_wrong_type(self):
        self.client.login(email="security@uni.edu.ng", password="testpass123")
        exe_file = SimpleUploadedFile(
            "malware.exe",
            b"\x00" * 100,
            content_type="application/octet-stream",
        )
        response = self.client.post(reverse("incidents:create"), {
            "platform_category": "social_media",
            "date_of_occurrence": "2025-10-01",
            "incident_classification": "doxxing",
            "narrative": "Test.",
            "actor_involvement": "known_person",
            "severity_rating": "3",
            "evidence_file": exe_file,
        })
        self.assertEqual(response.status_code, 200)  # Form re-rendered


# ============================================================
# EDGE CASE TESTS
# ============================================================

class EdgeCaseTests(TestCase):
    """Tests for edge cases and error handling."""

    def test_404_page(self):
        response = self.client.get("/nonexistent-page/")
        self.assertEqual(response.status_code, 404)

    def test_incident_reference_code_case_insensitive(self):
        user = User.objects.create_user(email="edge@uni.edu.ng", password="testpass123")
        incident = Incident.objects.create(
            user=user,
            platform_category="social_media",
            date_of_occurrence="2025-10-01",
            incident_classification="doxxing",
            narrative="Test.",
            actor_involvement="known_person",
            severity_rating=3,
        )
        self.client.login(email="edge@uni.edu.ng", password="testpass123")
        response = self.client.get(
            reverse("incidents:detail", args=[incident.reference_code])
        )
        self.assertEqual(response.status_code, 200)

    def test_concurrent_incident_creation(self):
        """Test that multiple incidents can be created without conflicts."""
        user = User.objects.create_user(email="concurrent@uni.edu.ng", password="testpass123")
        self.client.login(email="concurrent@uni.edu.ng", password="testpass123")
        for i in range(5):
            response = self.client.post(reverse("incidents:create"), {
                "platform_category": "social_media",
                "date_of_occurrence": "2025-10-01",
                "incident_classification": "doxxing",
                "narrative": f"Concurrent test {i}.",
                "actor_involvement": "known_person",
                "severity_rating": "3",
            }, follow=True)
            self.assertEqual(response.status_code, 200)
        self.assertEqual(Incident.objects.filter(user=user).count(), 5)


# ============================================================
# SEED RESOURCES TEST
# ============================================================

class SeedResourcesTest(TestCase):
    """Tests for the seed_resources management command."""

    def test_seed_resources_command(self):
        from django.core.management import call_command
        out = BytesIO()
        call_command("seed_resources", stdout=out)
        output = out.getvalue()
        self.assertIn("Seeded", output)
        self.assertTrue(Resource.objects.count() > 0)
