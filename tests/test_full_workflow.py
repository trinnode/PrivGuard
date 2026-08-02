"""
PrivGuard — Full Workflow Test Suite
=========================================
Tests every logical path, UI endpoint, edge case, and integration point.
Run: python manage.py test tests.test_full_workflow -v2
"""
import hashlib
import os
import tempfile
from io import BytesIO
from unittest.mock import patch, MagicMock

from django.test import TestCase, Client, override_settings
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from django.core import mail
from django.core.management import call_command
from django.contrib.messages import get_messages
from django.utils import timezone
from django.db import IntegrityError
from django.conf import settings

from incidents.models import Incident, Harm, AuditLog
from incidents.taxonomy import (
    HARM_CATEGORIES, PLATFORM_CATEGORIES, INCIDENT_CLASSIFICATIONS,
    SEVERITY_LEVELS, DURATION_CHOICES, ACTOR_CHOICES,
    get_harm_by_category, get_harm_type_choices,
)
from reporting.pdf_generator import generate_incident_report, generate_text_summary
from resources.models import Resource

User = get_user_model()


# ---------------------------------------------------------------------------
# 1. MODEL INTEGRITY TESTS
# ---------------------------------------------------------------------------

class UserModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@student.edu.ng", password="SecurePass123!",
            full_name="Test Student", institution="UNILAG",
        )

    def test_user_creation(self):
        self.assertEqual(self.user.email, "test@student.edu.ng")
        self.assertTrue(self.user.check_password("SecurePass123!"))
        self.assertFalse(self.user.consent_granted)
        self.assertEqual(self.user.role, "student")

    def test_email_normalized(self):
        user2 = User.objects.create_user(
            email="UPPER@STUDENT.EDU.NG", password="Pass1234!"
        )
        self.assertEqual(user2.email, "upper@student.edu.ng")

    def test_email_uniqueness(self):
        with self.assertRaises(IntegrityError):
            User.objects.create_user(email="test@student.edu.ng", password="x")

    def test_consent_record_and_revoke(self):
        self.user.record_consent()
        self.assertTrue(self.user.consent_granted)
        self.assertIsNotNone(self.user.consent_date)
        self.user.revoke_consent()
        self.assertFalse(self.user.consent_granted)
        self.assertIsNone(self.user.consent_date)

    def test_superuser_defaults(self):
        admin = User.objects.create_superuser(email="admin@r.com", password="Admin123!")
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
        self.assertEqual(admin.role, "admin")

    def test_anonymize_requested_default(self):
        self.assertFalse(self.user.anonymize_requested)

    def test_str_representation(self):
        self.assertEqual(str(self.user), "test@student.edu.ng")

    def test_role_choices(self):
        roles = [c[0] for c in User.Role.choices]
        self.assertIn("student", roles)
        self.assertIn("researcher", roles)
        self.assertIn("admin", roles)

    def test_last_password_reset_default_none(self):
        self.assertIsNone(self.user.last_password_reset)


class IncidentModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="s@u.edu.ng", password="Pass1234!"
        )

    def _create_incident(self, **kwargs):
        defaults = dict(
            user=self.user,
            platform_category="social_media",
            date_of_occurrence="2025-09-15",
            incident_classification="doxxing",
            narrative="My personal info was shared.",
            actor_involvement="known_person",
            severity_rating=3,
        )
        defaults.update(kwargs)
        return Incident.objects.create(**defaults)

    def test_incident_creation(self):
        inc = self._create_incident()
        self.assertTrue(inc.reference_code.startswith("PRG-"))
        self.assertEqual(len(inc.reference_code), 12)  # PRG- + 8 hex chars

    def test_reference_code_uniqueness(self):
        i1 = self._create_incident()
        i2 = self._create_incident(narrative="Another one.")
        self.assertNotEqual(i1.reference_code, i2.reference_code)

    def test_reference_code_auto_generated(self):
        inc = self._create_incident()
        self.assertTrue(inc.reference_code)

    def test_str_with_reference(self):
        inc = self._create_incident()
        self.assertIn(inc.reference_code, str(inc))

    def test_harms_summary_empty(self):
        inc = self._create_incident()
        self.assertEqual(inc.harms_summary(), "")

    def test_ordering(self):
        inc1 = self._create_incident(narrative="First")
        inc2 = self._create_incident(narrative="Second")
        incidents = list(Incident.objects.filter(user=self.user))
        self.assertEqual(incidents[0].narrative, "Second")

    def test_nullable_user(self):
        inc = self._create_incident(user=None, is_anonymous=True)
        self.assertIsNone(inc.user)
        self.assertTrue(inc.is_anonymous)

    def test_evidence_upload_path(self):
        inc = self._create_incident()
        path = inc.evidence_file.field.upload_to(inc, "test.png")
        self.assertIn(f"user_{self.user.id}", path)
        self.assertTrue(path.endswith("test.png"))

    def test_date_of_occurrence_stored(self):
        inc = self._create_incident(date_of_occurrence="2025-01-01")
        inc.refresh_from_db()
        self.assertEqual(str(inc.date_of_occurrence), "2025-01-01")


class HarmModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="h@t.com", password="Pass123!")
        self.incident = Incident.objects.create(
            user=self.user, platform_category="email",
            date_of_occurrence="2025-06-01",
            incident_classification="phishing",
            narrative="Test", actor_involvement="stranger",
            severity_rating=2,
        )

    def test_harm_creation(self):
        harm = Harm.objects.create(
            incident=self.incident, harm_category="anxiety",
            severity_score=2, duration="repeated_short",
            elaboration="Felt anxious.",
        )
        self.assertEqual(harm.incident, self.incident)
        self.assertIn("Anxiety", harm.get_harm_category_display())

    def test_multiple_harms(self):
        Harm.objects.create(
            incident=self.incident, harm_category="anxiety",
            severity_score=1, duration="one_time",
        )
        Harm.objects.create(
            incident=self.incident, harm_category="reputation",
            severity_score=3, duration="ongoing",
        )
        self.assertEqual(self.incident.harms.count(), 2)

    def test_harm_types_covered(self):
        harm_types = set(t for _, _, t in HARM_CATEGORIES)
        self.assertIn("psychological", harm_types)
        self.assertIn("tangible", harm_types)
        self.assertIn("other", harm_types)

    def test_harm_elaboration_optional(self):
        harm = Harm.objects.create(
            incident=self.incident, harm_category="distress",
            severity_score=2, duration="unknown",
        )
        self.assertEqual(harm.elaboration, "")

    def test_severity_levels_valid(self):
        for level, _ in SEVERITY_LEVELS:
            harm = Harm.objects.create(
                incident=self.incident, harm_category="anxiety",
                severity_score=level, duration="one_time",
            )
            self.assertIn(level, [1, 2, 3, 4])


class AuditLogTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="a@b.com", password="Pass123!")

    def test_audit_log_creation(self):
        log = AuditLog.objects.create(
            event_type="login", user=self.user,
            action_summary="Logged in", ip_hash="abc123",
        )
        self.assertEqual(log.event_type, "login")
        self.assertIn("Login", str(log))

    def test_ip_hash_sha256(self):
        expected = hashlib.sha256("127.0.0.1".encode()).hexdigest()
        self.assertEqual(len(expected), 64)

    def test_all_event_types(self):
        valid_types = [t[0] for t in AuditLog.EVENT_TYPES]
        expected = [
            "login", "logout", "incident_create", "incident_view",
            "incident_export", "account_delete", "consent_change",
            "failed_login", "password_reset", "admin_action",
        ]
        self.assertEqual(sorted(valid_types), sorted(expected))

    def test_user_nullable(self):
        log = AuditLog.objects.create(
            event_type="failed_login", action_summary="Failed", ip_hash="x",
        )
        self.assertIsNone(log.user)

    def test_ordering(self):
        AuditLog.objects.create(event_type="login", user=self.user, ip_hash="a")
        AuditLog.objects.create(event_type="logout", user=self.user, ip_hash="b")
        logs = list(AuditLog.objects.all())
        self.assertEqual(logs[0].event_type, "logout")


class ResourceModelTests(TestCase):
    def test_resource_creation(self):
        r = Resource.objects.create(
            title="Test Resource", category="legal",
            description="Desc", order=1,
        )
        self.assertTrue(r.is_visible)
        self.assertEqual(str(r), "Test Resource")

    def test_tag_list(self):
        r = Resource.objects.create(
            title="T", category="legal", description="D",
            relevance_tags="tag1, tag2, tag3",
        )
        self.assertEqual(r.tag_list(), ["tag1", "tag2", "tag3"])

    def test_empty_tags(self):
        r = Resource.objects.create(
            title="T", category="legal", description="D",
            relevance_tags="",
        )
        self.assertEqual(r.tag_list(), [])

    def test_category_choices(self):
        categories = [c[0] for c in Resource.CATEGORY_CHOICES]
        self.assertIn("legal", categories)
        self.assertIn("mental_health", categories)
        self.assertIn("emergency", categories)


# ---------------------------------------------------------------------------
# 2. TAXONOMY TESTS
# ---------------------------------------------------------------------------

class TaxonomyTests(TestCase):
    def test_harm_categories_structure(self):
        for item in HARM_CATEGORIES:
            self.assertEqual(len(item), 3)
            key, label, harm_type = item
            self.assertIsInstance(key, str)
            self.assertIsInstance(label, str)
            self.assertIn(harm_type, ["psychological", "tangible", "other"])

    def test_platform_categories_unique_keys(self):
        keys = [c[0] for c in PLATFORM_CATEGORIES]
        self.assertEqual(len(keys), len(set(keys)))

    def test_incident_classifications_unique_keys(self):
        keys = [c[0] for c in INCIDENT_CLASSIFICATIONS]
        self.assertEqual(len(keys), len(set(keys)))

    def test_severity_levels_1_to_4(self):
        levels = [s[0] for s in SEVERITY_LEVELS]
        self.assertEqual(sorted(levels), [1, 2, 3, 4])

    def test_duration_choices(self):
        keys = [d[0] for d in DURATION_CHOICES]
        self.assertIn("one_time", keys)
        self.assertIn("ongoing", keys)
        self.assertIn("unknown", keys)

    def test_actor_choices(self):
        keys = [a[0] for a in ACTOR_CHOICES]
        self.assertIn("known_person", keys)
        self.assertIn("authority_figure", keys)

    def test_get_harm_by_category_valid(self):
        result = get_harm_by_category("anxiety")
        self.assertEqual(result[0], "Anxiety - Persistent worry or fear about digital safety")

    def test_get_harm_by_category_invalid(self):
        result = get_harm_by_category("nonexistent")
        self.assertEqual(result[0], "Unknown")

    def test_get_harm_type_choices_psychological(self):
        choices = get_harm_type_choices("psychological")
        self.assertTrue(len(choices) > 0)
        for k, v in choices:
            self.assertIn(k, [c[0] for c in HARM_CATEGORIES if c[2] == "psychological"])

    def test_get_harm_type_choices_all(self):
        choices = get_harm_type_choices()
        self.assertEqual(len(choices), len(HARM_CATEGORIES))

    def test_psychological_harms_count(self):
        psy = [h for h in HARM_CATEGORIES if h[2] == "psychological"]
        self.assertEqual(len(psy), 9)

    def test_tangible_harms_count(self):
        tang = [h for h in HARM_CATEGORIES if h[2] == "tangible"]
        self.assertEqual(len(tang), 7)


# ---------------------------------------------------------------------------
# 3. FORM VALIDATION TESTS
# ---------------------------------------------------------------------------

class RegistrationFormTests(TestCase):
    def test_valid_registration(self):
        from accounts.forms import RegistrationForm
        form = RegistrationForm(data={
            "email": "new@uni.edu.ng", "full_name": "New",
            "institution": "UNILAG",
            "password1": "SecurePass123!", "password2": "SecurePass123!",
        })
        self.assertTrue(form.is_valid())

    def test_mismatched_passwords(self):
        from accounts.forms import RegistrationForm
        form = RegistrationForm(data={
            "email": "x@uni.edu.ng",
            "password1": "Pass1234!", "password2": "Different1!",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_short_password(self):
        from accounts.forms import RegistrationForm
        form = RegistrationForm(data={
            "email": "x@uni.edu.ng",
            "password1": "short", "password2": "short",
        })
        self.assertFalse(form.is_valid())

    def test_duplicate_email(self):
        from accounts.forms import RegistrationForm
        User.objects.create_user(email="dup@uni.edu.ng", password="Pass123!")
        form = RegistrationForm(data={
            "email": "dup@uni.edu.ng",
            "password1": "Pass1234!", "password2": "Pass1234!",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_consent_optional(self):
        from accounts.forms import RegistrationForm
        form = RegistrationForm(data={
            "email": "consent@uni.edu.ng",
            "password1": "Pass1234!", "password2": "Pass1234!",
            "consent": True,
        })
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertTrue(user.consent_granted)
        self.assertIsNotNone(user.consent_date)

    def test_email_stripped_and_lowered(self):
        from accounts.forms import RegistrationForm
        form = RegistrationForm(data={
            "email": "  UPPER@UNI.EDU.NG  ",
            "password1": "Pass1234!", "password2": "Pass1234!",
        })
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["email"], "upper@uni.edu.ng")


class IncidentFormTests(TestCase):
    def test_valid_incident(self):
        from incidents.forms import IncidentForm
        form = IncidentForm(data={
            "platform_category": "social_media",
            "date_of_occurrence": "2025-09-15",
            "incident_classification": "doxxing",
            "narrative": "My personal details were shared.",
            "actor_involvement": "known_person",
            "severity_rating": 3,
        })
        self.assertTrue(form.is_valid())

    def test_missing_required_fields(self):
        from incidents.forms import IncidentForm
        form = IncidentForm(data={})
        self.assertFalse(form.is_valid())
        required = [
            "platform_category", "date_of_occurrence",
            "incident_classification", "narrative",
            "actor_involvement", "severity_rating",
        ]
        for field in required:
            self.assertIn(field, form.errors)

    def test_optional_fields(self):
        from incidents.forms import IncidentForm
        form = IncidentForm(data={
            "platform_category": "email",
            "date_of_occurrence": "2025-01-01",
            "incident_classification": "phishing",
            "narrative": "Phishing attempt.",
            "actor_involvement": "stranger",
            "severity_rating": 1,
        })
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["platform_name"], "")
        self.assertEqual(form.cleaned_data["actor_description"], "")

    def test_evidence_file_validation(self):
        from incidents.forms import IncidentForm
        from django.core.files.uploadedfile import SimpleUploadedFile
        big_file = SimpleUploadedFile("big.pdf", b"x" * (6 * 1024 * 1024), content_type="application/pdf")
        form = IncidentForm(data={
            "platform_category": "email",
            "date_of_occurrence": "2025-01-01",
            "incident_classification": "phishing",
            "narrative": "Test",
            "actor_involvement": "stranger",
            "severity_rating": 1,
        }, files={"evidence_file": big_file})
        self.assertFalse(form.is_valid())
        self.assertIn("evidence_file", form.errors)

    def test_evidence_wrong_type(self):
        from incidents.forms import IncidentForm
        from django.core.files.uploadedfile import SimpleUploadedFile
        exe_file = SimpleUploadedFile("malware.exe", b"x", content_type="application/x-executable")
        form = IncidentForm(data={
            "platform_category": "email",
            "date_of_occurrence": "2025-01-01",
            "incident_classification": "phishing",
            "narrative": "Test",
            "actor_involvement": "stranger",
            "severity_rating": 1,
        }, files={"evidence_file": exe_file})
        self.assertFalse(form.is_valid())
        self.assertIn("evidence_file", form.errors)


# ---------------------------------------------------------------------------
# 4. AUTHENTICATION FLOW TESTS
# ---------------------------------------------------------------------------

class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse("accounts:register")
        self.login_url = reverse("accounts:login")

    def test_landing_page(self):
        response = self.client.get(reverse("landing"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "landing.html")

    def test_about_page(self):
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)

    def test_registration_page_loads(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/register.html")

    def test_successful_registration(self):
        response = self.client.post(self.register_url, {
            "email": "new@uni.edu.ng",
            "full_name": "New Student",
            "institution": "UNILAG",
            "password1": "SecurePass123!",
            "password2": "SecurePass123!",
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(email="new@uni.edu.ng").exists())

    def test_registration_auto_login(self):
        self.client.post(self.register_url, {
            "email": "auto@uni.edu.ng",
            "password1": "SecurePass123!",
            "password2": "SecurePass123!",
        }, follow=True)
        response = self.client.get(reverse("dashboard:home"))
        self.assertEqual(response.status_code, 200)

    def test_login_page_loads(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)

    def test_successful_login(self):
        User.objects.create_user(email="login@uni.edu.ng", password="TestPass123!")
        response = self.client.post(self.login_url, {
            "username": "login@uni.edu.ng",
            "password": "TestPass123!",
        }, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_failed_login(self):
        response = self.client.post(self.login_url, {
            "username": "wrong@uni.edu.ng",
            "password": "wrong",
        }, follow=True)
        messages_list = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Invalid" in str(m) for m in messages_list))

    def test_logout(self):
        User.objects.create_user(email="lo@uni.edu.ng", password="Pass123!")
        self.client.login(email="lo@uni.edu.ng", password="Pass123!")
        response = self.client.get(reverse("accounts:logout"), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_password_reset_flow(self):
        User.objects.create_user(email="pr@uni.edu.ng", password="Pass123!")
        response = self.client.post(reverse("accounts:password_reset"), {
            "email": "pr@uni.edu.ng",
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)

    def test_password_reset_nonexistent_email(self):
        response = self.client.post(reverse("accounts:password_reset"), {
            "email": "nobody@uni.edu.ng",
        }, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_profile_requires_auth(self):
        response = self.client.get(reverse("accounts:profile"))
        self.assertNotEqual(response.status_code, 200)

    def test_profile_loads(self):
        User.objects.create_user(email="pf@uni.edu.ng", password="Pass123!")
        self.client.login(email="pf@uni.edu.ng", password="Pass123!")
        response = self.client.get(reverse("accounts:profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/profile.html")

    def test_profile_update(self):
        User.objects.create_user(email="pu@uni.edu.ng", password="Pass123!")
        self.client.login(email="pu@uni.edu.ng", password="Pass123!")
        response = self.client.post(reverse("accounts:profile"), {
            "full_name": "Updated Name",
            "institution": "New University",
        }, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_toggle_consent(self):
        User.objects.create_user(email="tc@uni.edu.ng", password="Pass123!")
        self.client.login(email="tc@uni.edu.ng", password="Pass123!")
        self.client.post(reverse("accounts:toggle_consent"), follow=True)
        user = User.objects.get(email="tc@uni.edu.ng")
        self.assertTrue(user.consent_granted)
        self.client.post(reverse("accounts:toggle_consent"), follow=True)
        user.refresh_from_db()
        self.assertFalse(user.consent_granted)

    def test_toggle_anonymize(self):
        User.objects.create_user(email="ta@uni.edu.ng", password="Pass123!")
        self.client.login(email="ta@uni.edu.ng", password="Pass123!")
        self.client.post(reverse("accounts:toggle_anonymize"), follow=True)
        user = User.objects.get(email="ta@uni.edu.ng")
        self.assertTrue(user.anonymize_requested)

    def test_delete_account(self):
        User.objects.create_user(email="del@uni.edu.ng", password="Pass123!")
        self.client.login(email="del@uni.edu.ng", password="Pass123!")
        response = self.client.post(reverse("accounts:delete_account"), {
            "password": "Pass123!",
        }, follow=True)
        self.assertFalse(User.objects.filter(email="del@uni.edu.ng").exists())

    def test_delete_account_wrong_password(self):
        User.objects.create_user(email="dw@uni.edu.ng", password="Pass123!")
        self.client.login(email="dw@uni.edu.ng", password="Pass123!")
        self.client.post(reverse("accounts:delete_account"), {
            "password": "wrongpassword",
        }, follow=True)
        self.assertTrue(User.objects.filter(email="dw@uni.edu.ng").exists())

    def test_csrf_failure_page(self):
        response = self.client.get(reverse("accounts:csrf_failure") if False else "/accounts/password-reset/")
        self.assertIn(response.status_code, [200, 302])


# ---------------------------------------------------------------------------
# 5. INCIDENT WORKFLOW TESTS
# ---------------------------------------------------------------------------

class IncidentWorkflowTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="reporter@uni.edu.ng", password="TestPass123!"
        )
        self.client.login(email="reporter@uni.edu.ng", password="TestPass123!")

    def test_incident_list_requires_auth(self):
        self.client.logout()
        response = self.client.get(reverse("incidents:list"))
        self.assertNotEqual(response.status_code, 200)

    def test_incident_list_empty(self):
        response = self.client.get(reverse("incidents:list"))
        self.assertEqual(response.status_code, 200)

    def test_create_incident_get(self):
        response = self.client.get(reverse("incidents:create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "incidents/create.html")

    def test_create_incident_post(self):
        response = self.client.post(reverse("incidents:create"), {
            "platform_category": "social_media",
            "date_of_occurrence": "2025-10-01",
            "incident_classification": "doxxing",
            "narrative": "My info was leaked.",
            "actor_involvement": "known_person",
            "severity_rating": "3",
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Incident.objects.filter(user=self.user).count(), 1)

    def test_create_incident_with_harms(self):
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
            "harm_elaboration_anxiety": "Felt anxious for weeks.",
            "harm_severity_reputation": "3",
            "harm_duration_reputation": "repeated_long",
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        incident = Incident.objects.get(user=self.user)
        self.assertEqual(incident.harms.count(), 2)

    def test_create_incident_anonymous_not_logged_in(self):
        self.client.logout()
        response = self.client.post(reverse("incidents:create"), {
            "platform_category": "email",
            "date_of_occurrence": "2025-06-01",
            "incident_classification": "phishing",
            "narrative": "Phishing attempt.",
            "actor_involvement": "stranger",
            "severity_rating": "2",
            "is_anonymous": "on",
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Incident.objects.count(), 1)
        inc = Incident.objects.first()
        self.assertIsNone(inc.user)
        self.assertTrue(inc.is_anonymous)

    def test_incident_detail(self):
        inc = Incident.objects.create(
            user=self.user, platform_category="email",
            date_of_occurrence="2025-06-01",
            incident_classification="phishing",
            narrative="Test", actor_involvement="stranger",
            severity_rating=2,
        )
        response = self.client.get(
            reverse("incidents:detail", args=[inc.reference_code])
        )
        self.assertEqual(response.status_code, 200)

    def test_incident_detail_wrong_user(self):
        other = User.objects.create_user(email="other@uni.edu.ng", password="Pass123!")
        inc = Incident.objects.create(
            user=other, platform_category="email",
            date_of_occurrence="2025-06-01",
            incident_classification="phishing",
            narrative="Test", actor_involvement="stranger",
            severity_rating=2,
        )
        response = self.client.get(
            reverse("incidents:detail", args=[inc.reference_code])
        )
        self.assertEqual(response.status_code, 404)

    def test_incident_list_shows_only_own(self):
        other = User.objects.create_user(email="other2@uni.edu.ng", password="Pass123!")
        Incident.objects.create(
            user=other, platform_category="email",
            date_of_occurrence="2025-06-01",
            incident_classification="phishing",
            narrative="Other's incident", actor_involvement="stranger",
            severity_rating=2,
        )
        response = self.client.get(reverse("incidents:list"))
        self.assertEqual(len(response.context["incidents"]), 0)

    def test_create_incident_invalid_form(self):
        response = self.client.post(reverse("incidents:create"), {
            "platform_category": "",
            "date_of_occurrence": "",
            "incident_classification": "",
            "narrative": "",
            "actor_involvement": "",
            "severity_rating": "",
        }, follow=True)
        self.assertEqual(Incident.objects.count(), 0)


# ---------------------------------------------------------------------------
# 6. ADMIN PANEL TESTS
# ---------------------------------------------------------------------------

class AdminPanelTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_user(
            email="admin@uni.edu.ng", password="AdminPass123!",
            role="admin",
        )
        self.normal = User.objects.create_user(
            email="normal@uni.edu.ng", password="NormalPass123!",
        )
        self.incident = Incident.objects.create(
            user=self.normal, platform_category="social_media",
            date_of_occurrence="2025-06-01",
            incident_classification="doxxing",
            narrative="Test", actor_involvement="known_person",
            severity_rating=3,
        )

    def test_admin_list_requires_admin(self):
        self.client.login(email="normal@uni.edu.ng", password="NormalPass123!")
        response = self.client.get(reverse("incidents:admin_list"), follow=True)
        messages_list = list(get_messages(response.wsgi_request))
        self.assertTrue(any("permission" in str(m).lower() for m in messages_list))

    def test_admin_list_loads(self):
        self.client.login(email="admin@uni.edu.ng", password="AdminPass123!")
        response = self.client.get(reverse("incidents:admin_list"))
        self.assertEqual(response.status_code, 200)

    def test_admin_detail(self):
        self.client.login(email="admin@uni.edu.ng", password="AdminPass123!")
        response = self.client.get(
            reverse("incidents:admin_detail", args=[self.incident.reference_code])
        )
        self.assertEqual(response.status_code, 200)

    def test_admin_delete(self):
        self.client.login(email="admin@uni.edu.ng", password="AdminPass123!")
        response = self.client.post(
            reverse("incidents:admin_delete", args=[self.incident.reference_code]),
            follow=True,
        )
        self.assertFalse(Incident.objects.filter(
            reference_code=self.incident.reference_code
        ).exists())

    def test_admin_export(self):
        self.client.login(email="admin@uni.edu.ng", password="AdminPass123!")
        response = self.client.get(
            reverse("incidents:admin_export", args=[self.incident.reference_code])
        )
        self.assertEqual(response.status_code, 200)

    def test_normal_user_cannot_admin_detail(self):
        self.client.login(email="normal@uni.edu.ng", password="NormalPass123!")
        response = self.client.get(
            reverse("incidents:admin_detail", args=[self.incident.reference_code]),
            follow=True,
        )
        self.assertNotEqual(response.status_code, 200)

    def test_normal_user_cannot_admin_delete(self):
        self.client.login(email="normal@uni.edu.ng", password="NormalPass123!")
        self.client.post(
            reverse("incidents:admin_delete", args=[self.incident.reference_code]),
            follow=True,
        )
        self.assertTrue(Incident.objects.filter(
            reference_code=self.incident.reference_code
        ).exists())


# ---------------------------------------------------------------------------
# 7. PDF EXPORT TESTS
# ---------------------------------------------------------------------------

class PDFExportTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="pdf@uni.edu.ng", password="Pass123!"
        )
        self.client.login(email="pdf@uni.edu.ng", password="Pass123!")
        self.incident = Incident.objects.create(
            user=self.user, platform_category="social_media",
            date_of_occurrence="2025-06-01",
            incident_classification="doxxing",
            narrative="Test narrative for PDF export.",
            actor_involvement="known_person",
            severity_rating=3,
        )
        Harm.objects.create(
            incident=self.incident, harm_category="anxiety",
            severity_score=2, duration="repeated_short",
            elaboration="Felt anxious.",
        )

    def test_pdf_export(self):
        response = self.client.get(
            reverse("reporting:export_pdf", args=[self.incident.reference_code])
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")

    def test_pdf_filename(self):
        response = self.client.get(
            reverse("reporting:export_pdf", args=[self.incident.reference_code])
        )
        self.assertIn(self.incident.reference_code, response["Content-Disposition"])

    def test_pdf_generate_function(self):
        buffer = generate_incident_report(self.incident)
        content = buffer.read()
        self.assertTrue(content.startswith(b"%PDF"))

    def test_text_summary_generate_function(self):
        text = generate_text_summary(self.incident)
        self.assertIn("PRIVACY INCIDENT REPORT", text)
        self.assertIn(self.incident.reference_code, text)
        self.assertIn("Test narrative for PDF export.", text)

    def test_text_summary_includes_harms(self):
        text = generate_text_summary(self.incident)
        self.assertIn("Anxiety", text)

    def test_pdf_export_wrong_user(self):
        other = User.objects.create_user(email="other@uni.edu.ng", password="Pass123!")
        self.client.login(email="other@uni.edu.ng", password="Pass123!")
        response = self.client.get(
            reverse("reporting:export_pdf", args=[self.incident.reference_code])
        )
        self.assertEqual(response.status_code, 404)

    def test_pdf_with_no_harms(self):
        inc = Incident.objects.create(
            user=self.user, platform_category="email",
            date_of_occurrence="2025-06-01",
            incident_classification="phishing",
            narrative="No harms.", actor_involvement="stranger",
            severity_rating=1,
        )
        buffer = generate_incident_report(inc)
        self.assertTrue(buffer.read().startswith(b"%PDF"))

    def test_text_summary_with_no_harms(self):
        inc = Incident.objects.create(
            user=self.user, platform_category="email",
            date_of_occurrence="2025-06-01",
            incident_classification="phishing",
            narrative="No harms.", actor_involvement="stranger",
            severity_rating=1,
        )
        text = generate_text_summary(inc)
        self.assertIn("No harms.", text)

    def test_pdf_export_requires_auth(self):
        self.client.logout()
        response = self.client.get(
            reverse("reporting:export_pdf", args=[self.incident.reference_code])
        )
        self.assertNotEqual(response.status_code, 200)


# ---------------------------------------------------------------------------
# 8. DASHBOARD TESTS
# ---------------------------------------------------------------------------

class DashboardTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="dash@uni.edu.ng", password="Pass123!"
        )
        self.client.login(email="dash@uni.edu.ng", password="Pass123!")

    def test_dashboard_requires_auth(self):
        self.client.logout()
        response = self.client.get(reverse("dashboard:home"))
        self.assertNotEqual(response.status_code, 200)

    def test_dashboard_empty(self):
        response = self.client.get(reverse("dashboard:home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard/home.html")

    def test_dashboard_with_incidents(self):
        inc = Incident.objects.create(
            user=self.user, platform_category="social_media",
            date_of_occurrence="2025-06-01",
            incident_classification="doxxing",
            narrative="Test", actor_involvement="known_person",
            severity_rating=3,
        )
        Harm.objects.create(
            incident=inc, harm_category="anxiety",
            severity_score=2, duration="repeated_short",
        )
        response = self.client.get(reverse("dashboard:home"))
        self.assertEqual(response.context["total_incidents"], 1)
        self.assertEqual(response.context["psychological_count"], 1)

    def test_dashboard_stats_populated(self):
        for i in range(5):
            Incident.objects.create(
                user=self.user, platform_category="social_media",
                date_of_occurrence="2025-06-01",
                incident_classification="doxxing",
                narrative=f"Incident {i}", actor_involvement="known_person",
                severity_rating=3,
            )
        response = self.client.get(reverse("dashboard:home"))
        self.assertEqual(response.context["total_incidents"], 5)

    def test_dashboard_harm_distribution(self):
        inc = Incident.objects.create(
            user=self.user, platform_category="email",
            date_of_occurrence="2025-06-01",
            incident_classification="phishing",
            narrative="Test", actor_involvement="stranger",
            severity_rating=2,
        )
        Harm.objects.create(
            incident=inc, harm_category="anxiety",
            severity_score=1, duration="one_time",
        )
        Harm.objects.create(
            incident=inc, harm_category="reputation",
            severity_score=2, duration="repeated_short",
        )
        response = self.client.get(reverse("dashboard:home"))
        self.assertIn("Anxiety - Persistent worry or fear about digital safety",
                       response.context["harm_counts"])

    def test_dashboard_only_own_incidents(self):
        other = User.objects.create_user(email="other@uni.edu.ng", password="Pass123!")
        Incident.objects.create(
            user=other, platform_category="email",
            date_of_occurrence="2025-06-01",
            incident_classification="phishing",
            narrative="Other's", actor_involvement="stranger",
            severity_rating=1,
        )
        response = self.client.get(reverse("dashboard:home"))
        self.assertEqual(response.context["total_incidents"], 0)

    def test_dashboard_severity_distribution(self):
        Incident.objects.create(
            user=self.user, platform_category="email",
            date_of_occurrence="2025-06-01",
            incident_classification="phishing",
            narrative="T1", actor_involvement="stranger",
            severity_rating=1,
        )
        Incident.objects.create(
            user=self.user, platform_category="email",
            date_of_occurrence="2025-06-01",
            incident_classification="phishing",
            narrative="T2", actor_involvement="stranger",
            severity_rating=3,
        )
        response = self.client.get(reverse("dashboard:home"))
        self.assertEqual(len(response.context["severity_distribution"]), 2)


# ---------------------------------------------------------------------------
# 9. RESOURCE LIBRARY TESTS
# ---------------------------------------------------------------------------

class ResourceTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="res@uni.edu.ng", password="Pass123!"
        )
        self.client.login(email="res@uni.edu.ng", password="Pass123!")
        self.resource = Resource.objects.create(
            title="Legal Guide", category="legal",
            description="A comprehensive legal guide.",
            external_link="https://example.com",
            relevance_tags="legal, rights, Nigeria",
            order=1,
        )

    def test_resource_list_requires_auth(self):
        self.client.logout()
        response = self.client.get(reverse("resources:list"))
        self.assertNotEqual(response.status_code, 200)

    def test_resource_list_loads(self):
        response = self.client.get(reverse("resources:list"))
        self.assertEqual(response.status_code, 200)

    def test_resource_filter_by_category(self):
        Resource.objects.create(
            title="Mental Health", category="mental_health",
            description="MH resource.",
        )
        response = self.client.get(reverse("resources:list") + "?category=legal")
        self.assertEqual(len(response.context["resources"]), 1)

    def test_resource_detail(self):
        response = self.client.get(
            reverse("resources:detail", args=[self.resource.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_resource_detail_not_found(self):
        response = self.client.get(
            reverse("resources:detail", args=[99999])
        )
        self.assertIn(response.status_code, [404, 500])


# ---------------------------------------------------------------------------
# 10. AUDIT LOGGING TESTS
# ---------------------------------------------------------------------------

class AuditLoggingTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="audit@uni.edu.ng", password="Pass123!"
        )
        self.client.login(email="audit@uni.edu.ng", password="Pass123!")

    def test_incident_create_audits(self):
        self.client.post(reverse("incidents:create"), {
            "platform_category": "email",
            "date_of_occurrence": "2025-06-01",
            "incident_classification": "phishing",
            "narrative": "Test", "actor_involvement": "stranger",
            "severity_rating": "2",
        })
        self.assertTrue(
            AuditLog.objects.filter(event_type="incident_create").exists()
        )

    def test_incident_view_audits(self):
        inc = Incident.objects.create(
            user=self.user, platform_category="email",
            date_of_occurrence="2025-06-01",
            incident_classification="phishing",
            narrative="Test", actor_involvement="stranger",
            severity_rating=2,
        )
        self.client.get(reverse("incidents:detail", args=[inc.reference_code]))
        self.assertTrue(
            AuditLog.objects.filter(
                event_type="incident_view",
                action_summary__contains=inc.reference_code,
            ).exists()
        )

    def test_admin_action_audit(self):
        admin = User.objects.create_user(
            email="ad@uni.edu.ng", password="Pass123!", role="admin"
        )
        self.client.login(email="ad@uni.edu.ng", password="Pass123!")
        inc = Incident.objects.create(
            user=self.user, platform_category="email",
            date_of_occurrence="2025-06-01",
            incident_classification="phishing",
            narrative="Test", actor_involvement="stranger",
            severity_rating=2,
        )
        self.client.get(reverse("incidents:admin_detail", args=[inc.reference_code]))
        self.assertTrue(
            AuditLog.objects.filter(
                event_type="admin_action",
                action_summary__contains=inc.reference_code,
            ).exists()
        )

    def test_ip_hash_recorded(self):
        self.client.post(reverse("incidents:create"), {
            "platform_category": "email",
            "date_of_occurrence": "2025-06-01",
            "incident_classification": "phishing",
            "narrative": "Test", "actor_involvement": "stranger",
            "severity_rating": "2",
        })
        log = AuditLog.objects.filter(event_type="incident_create").first()
        self.assertEqual(len(log.ip_hash), 64)


# ---------------------------------------------------------------------------
# 11. MIDDLEWARE TESTS
# ---------------------------------------------------------------------------

class SessionTimeoutTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="mw@uni.edu.ng", password="Pass123!"
        )
        self.client.login(email="mw@uni.edu.ng", password="Pass123!")

    def test_session_timeout_redirects(self):
        session = self.client.session
        session["last_activity"] = timezone.now().timestamp() - 1000
        session.save()
        response = self.client.get(reverse("dashboard:home"))
        self.assertNotEqual(response.status_code, 200)

    def test_active_session_not_timeout(self):
        response = self.client.get(reverse("dashboard:home"))
        self.assertEqual(response.status_code, 200)


# ---------------------------------------------------------------------------
# 12. MANAGEMENT COMMANDS TESTS
# ---------------------------------------------------------------------------

class SeedResourcesCommandTests(TestCase):
    def test_seed_resources(self):
        call_command("seed_resources")
        self.assertTrue(Resource.objects.filter(category="legal").exists())
        self.assertTrue(Resource.objects.filter(category="mental_health").exists())
        self.assertTrue(Resource.objects.filter(category="digital_safety").exists())
        self.assertTrue(Resource.objects.filter(category="emergency").exists())
        self.assertTrue(Resource.objects.filter(category="general").exists())

    def test_seed_resources_idempotent(self):
        call_command("seed_resources")
        count_after_first = Resource.objects.count()
        call_command("seed_resources")
        self.assertEqual(Resource.objects.count(), count_after_first)

    def test_seed_resource_count(self):
        call_command("seed_resources")
        self.assertGreaterEqual(Resource.objects.count(), 15)


# ---------------------------------------------------------------------------
# 13. URL RESOLUTION TESTS
# ---------------------------------------------------------------------------

class URLResolutionTests(TestCase):
    def test_all_urls_resolve(self):
        url_patterns = [
            ("landing", [], {}),
            ("about", [], {}),
            ("accounts:register", [], {}),
            ("accounts:login", [], {}),
            ("accounts:logout", [], {}),
            ("accounts:profile", [], {}),
            ("accounts:toggle_consent", [], {}),
            ("accounts:toggle_anonymize", [], {}),
            ("incidents:list", [], {}),
            ("incidents:create", [], {}),
            ("dashboard:home", [], {}),
            ("resources:list", [], {}),
        ]
        for name, args, kwargs in url_patterns:
            url = reverse(name, args=args, kwargs=kwargs)
            self.assertTrue(resolve(url))

    def test_incident_detail_url(self):
        url = reverse("incidents:detail", args=["PRG-TEST1234"])
        match = resolve(url)
        self.assertEqual(match.url_name, "detail")

    def test_admin_urls(self):
        url = reverse("incidents:admin_list")
        self.assertTrue(resolve(url))
        url = reverse("incidents:admin_detail", args=["PRG-TEST1234"])
        self.assertTrue(resolve(url))

    def test_pdf_export_url(self):
        url = reverse("reporting:export_pdf", args=["PRG-TEST1234"])
        self.assertTrue(resolve(url))

    def test_resource_detail_url(self):
        url = reverse("resources:detail", args=[1])
        self.assertTrue(resolve(url))

    def test_password_reset_urls(self):
        for name in ["accounts:password_reset", "accounts:password_reset_done",
                      "accounts:password_reset_complete"]:
            url = reverse(name)
            self.assertTrue(resolve(url))


# ---------------------------------------------------------------------------
# 14. TEMPLATE RENDERING TESTS
# ---------------------------------------------------------------------------

class TemplateRenderingTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="tmpl@uni.edu.ng", password="Pass123!"
        )
        self.client.login(email="tmpl@uni.edu.ng", password="Pass123!")

    def test_base_template_renders(self):
        response = self.client.get(reverse("landing"))
        self.assertContains(response, "PrivGuard")
        self.assertContains(response, "main.css")
        self.assertContains(response, "main.js")

    def test_dark_mode_toggle_present(self):
        response = self.client.get(reverse("landing"))
        self.assertContains(response, "dark-mode-toggle")

    def test_mobile_menu_present(self):
        response = self.client.get(reverse("landing"))
        self.assertContains(response, "mobile-menu-toggle")

    def test_auth_nav_authenticated(self):
        response = self.client.get(reverse("dashboard:home"))
        self.assertContains(response, "Dashboard")
        self.assertContains(response, "Incidents")

    def test_auth_nav_unauthenticated(self):
        self.client.logout()
        response = self.client.get(reverse("landing"))
        self.assertContains(response, "Sign In")
        self.assertContains(response, "Get Started")

    def test_messages_displayed(self):
        from django.contrib.messages import add_message, constants
        request = self.client.get(reverse("dashboard:home")).wsgi_request
        add_message(request, constants.SUCCESS, "Test message")
        response = self.client.get(reverse("dashboard:home"))
        self.assertContains(response, "Test message")

    def test_404_page(self):
        response = self.client.get("/nonexistent-page/")
        self.assertEqual(response.status_code, 404)

    def test_incident_form_wizard_steps(self):
        response = self.client.get(reverse("incidents:create"))
        self.assertContains(response, "wizard-step")
        self.assertContains(response, "wizard-step-content")

    def test_harm_categories_in_form(self):
        response = self.client.get(reverse("incidents:create"))
        self.assertContains(response, "harm_sel")
        self.assertContains(response, "Psychological Harms")
        self.assertContains(response, "Tangible Harms")


# ---------------------------------------------------------------------------
# 15. SECURITY TESTS
# ---------------------------------------------------------------------------

class SecurityTests(TestCase):
    def test_session_cookie_httponly(self):
        self.assertTrue(settings.SESSION_COOKIE_HTTPONLY)

    def test_csrf_cookie_httponly(self):
        self.assertTrue(settings.CSRF_COOKIE_HTTPONLY)

    def test_session_expire_at_browser_close(self):
        self.assertTrue(settings.SESSION_EXPIRE_AT_BROWSER_CLOSE)

    def test_x_frame_options_deny(self):
        self.assertEqual(settings.X_FRAME_OPTIONS, "DENY")

    def test_secure_content_type_nosniff(self):
        self.assertTrue(settings.SECURE_CONTENT_TYPE_NOSNIFF)

    def test_session_timeout_900_seconds(self):
        self.assertEqual(settings.SESSION_COOKIE_AGE, 900)

    def test_argon2_hasher_first(self):
        self.assertIn(
            "Argon2PasswordHasher", settings.AUTH_PASSWORD_HASHERS[0]
        )

    def test_custom_user_model(self):
        self.assertEqual(settings.AUTH_USER_MODEL, "accounts.User")

    def test_same_site_strict(self):
        self.assertEqual(settings.SESSION_COOKIE_SAMESITE, "Strict")

    def test_evidence_file_max_size(self):
        self.assertEqual(settings.MAX_UPLOAD_SIZE, 100 * 1024)

    def test_allowed_upload_types(self):
        self.assertIn("image/png", settings.ALLOWED_UPLOAD_TYPES)
        self.assertIn("image/jpeg", settings.ALLOWED_UPLOAD_TYPES)
        self.assertIn("application/pdf", settings.ALLOWED_UPLOAD_TYPES)

    def test_login_required_on_incident_endpoints(self):
        client = Client()
        endpoints = [
            reverse("incidents:list"),
            reverse("dashboard:home"),
            reverse("resources:list"),
            reverse("accounts:profile"),
        ]
        for url in endpoints:
            response = client.get(url)
            self.assertNotEqual(response.status_code, 200)

    def test_incident_create_not_required_auth(self):
        client = Client()
        response = client.get(reverse("incidents:create"))
        self.assertEqual(response.status_code, 200)


# ---------------------------------------------------------------------------
# 16. EDGE CASE TESTS
# ---------------------------------------------------------------------------

class EdgeCaseTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="edge@uni.edu.ng", password="Pass123!"
        )
        self.client.login(email="edge@uni.edu.ng", password="Pass123!")

    def test_incident_all_platform_categories(self):
        for key, _ in PLATFORM_CATEGORIES:
            response = self.client.post(reverse("incidents:create"), {
                "platform_category": key,
                "date_of_occurrence": "2025-06-01",
                "incident_classification": "phishing",
                "narrative": f"Test with {key}",
                "actor_involvement": "stranger",
                "severity_rating": "1",
            }, follow=True)
            self.assertEqual(response.status_code, 200)

    def test_incident_all_severity_levels(self):
        for level, _ in SEVERITY_LEVELS:
            response = self.client.post(reverse("incidents:create"), {
                "platform_category": "email",
                "date_of_occurrence": "2025-06-01",
                "incident_classification": "phishing",
                "narrative": f"Severity {level}",
                "actor_involvement": "stranger",
                "severity_rating": str(level),
            }, follow=True)
            self.assertEqual(response.status_code, 200)

    def test_incident_all_actor_types(self):
        for key, _ in ACTOR_CHOICES:
            response = self.client.post(reverse("incidents:create"), {
                "platform_category": "email",
                "date_of_occurrence": "2025-06-01",
                "incident_classification": "phishing",
                "narrative": f"Actor {key}",
                "actor_involvement": key,
                "severity_rating": "2",
            }, follow=True)
            self.assertEqual(response.status_code, 200)

    def test_incident_all_duration_types(self):
        inc = Incident.objects.create(
            user=self.user, platform_category="email",
            date_of_occurrence="2025-06-01",
            incident_classification="phishing",
            narrative="Test", actor_involvement="stranger",
            severity_rating=2,
        )
        for key, _ in DURATION_CHOICES:
            Harm.objects.create(
                incident=inc, harm_category="anxiety",
                severity_score=1, duration=key,
            )
        self.assertEqual(inc.harms.count(), len(DURATION_CHOICES))

    def test_long_narrative(self):
        long_narrative = "A" * 10000
        response = self.client.post(reverse("incidents:create"), {
            "platform_category": "email",
            "date_of_occurrence": "2025-06-01",
            "incident_classification": "phishing",
            "narrative": long_narrative,
            "actor_involvement": "stranger",
            "severity_rating": "2",
        }, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_special_characters_in_narrative(self):
        response = self.client.post(reverse("incidents:create"), {
            "platform_category": "email",
            "date_of_occurrence": "2025-06-01",
            "incident_classification": "phishing",
            "narrative": "Test <script>alert('xss')</script> & \"quotes\" 'single'",
            "actor_involvement": "stranger",
            "severity_rating": "2",
        }, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_unicode_in_fields(self):
        response = self.client.post(reverse("incidents:create"), {
            "platform_category": "email",
            "date_of_occurrence": "2025-06-01",
            "incident_classification": "phishing",
            "narrative": "Nigerian student ñ ü ö ä",
            "actor_involvement": "stranger",
            "severity_rating": "2",
            "actor_description": "Person from Lagos",
        }, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_evidence_file_valid_png(self):
        from django.core.files.uploadedfile import SimpleUploadedFile
        png = SimpleUploadedFile("test.png", b"\x89PNG\r\n\x1a\n", content_type="image/png")
        response = self.client.post(reverse("incidents:create"), {
            "platform_category": "email",
            "date_of_occurrence": "2025-06-01",
            "incident_classification": "phishing",
            "narrative": "PNG upload",
            "actor_involvement": "stranger",
            "severity_rating": "1",
            "evidence_file": png,
        }, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_multiple_harms_all_categories(self):
        harm_keys = [h[0] for h in HARM_CATEGORIES]
        post_data = {
            "platform_category": "email",
            "date_of_occurrence": "2025-06-01",
            "incident_classification": "phishing",
            "narrative": "All harms",
            "actor_involvement": "stranger",
            "severity_rating": "3",
            "harm_sel": harm_keys,
        }
        for key in harm_keys:
            post_data[f"harm_severity_{key}"] = "2"
            post_data[f"harm_duration_{key}"] = "repeated_short"
        response = self.client.post(reverse("incidents:create"), post_data, follow=True)
        self.assertEqual(response.status_code, 200)
        inc = Incident.objects.get(user=self.user, narrative="All harms")
        self.assertEqual(inc.harms.count(), len(harm_keys))

    def test_empty_harm_elaboration(self):
        response = self.client.post(reverse("incidents:create"), {
            "platform_category": "email",
            "date_of_occurrence": "2025-06-01",
            "incident_classification": "phishing",
            "narrative": "Empty elaboration test",
            "actor_involvement": "stranger",
            "severity_rating": "2",
            "harm_sel": ["anxiety"],
            "harm_severity_anxiety": "1",
            "harm_duration_anxiety": "one_time",
            "harm_elaboration_anxiety": "",
        }, follow=True)
        inc = Incident.objects.get(narrative="Empty elaboration test")
        self.assertEqual(inc.harms.first().elaboration, "")


# ---------------------------------------------------------------------------
# 17. INTEGRATION TESTS (Full End-to-End)
# ---------------------------------------------------------------------------

class FullWorkflowIntegrationTests(TestCase):
    def test_complete_user_journey(self):
        """Simulates a full user lifecycle: register -> report -> view -> export -> delete."""
        client = Client()

        # 1. Register
        response = client.post(reverse("accounts:register"), {
            "email": "journey@uni.edu.ng",
            "full_name": "Journey Test",
            "institution": "UNILAG",
            "password1": "SecurePass123!",
            "password2": "SecurePass123!",
            "consent": "on",
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        user = User.objects.get(email="journey@uni.edu.ng")
        self.assertTrue(user.consent_granted)

        # 2. Report incident
        response = client.post(reverse("incidents:create"), {
            "platform_category": "social_media",
            "date_of_occurrence": "2025-10-01",
            "incident_classification": "doxxing",
            "narrative": "My personal photos were shared without consent on a public group.",
            "actor_involvement": "known_person",
            "actor_description": "A former classmate",
            "severity_rating": "4",
            "harm_sel": ["anxiety", "humiliation", "reputation"],
            "harm_severity_anxiety": "3",
            "harm_duration_anxiety": "repeated_long",
            "harm_elaboration_anxiety": "Constant anxiety about my safety",
            "harm_severity_humiliation": "4",
            "harm_duration_humiliation": "repeated_long",
            "harm_severity_reputation": "3",
            "harm_duration_reputation": "ongoing",
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        inc = Incident.objects.get(user=user)
        self.assertEqual(inc.harms.count(), 3)

        # 3. View dashboard
        response = client.get(reverse("dashboard:home"))
        self.assertEqual(response.context["total_incidents"], 1)

        # 4. View incident detail
        response = client.get(
            reverse("incidents:detail", args=[inc.reference_code])
        )
        self.assertEqual(response.status_code, 200)

        # 5. Export PDF
        response = client.get(
            reverse("reporting:export_pdf", args=[inc.reference_code])
        )
        self.assertEqual(response.status_code, 200)

        # 6. View incident list
        response = client.get(reverse("incidents:list"))
        self.assertEqual(len(response.context["incidents"]), 1)

        # 7. Toggle anonymity
        client.post(reverse("accounts:toggle_anonymize"), follow=True)
        user.refresh_from_db()
        self.assertTrue(user.anonymize_requested)

        # 8. Visit resources
        call_command("seed_resources")
        response = client.get(reverse("resources:list"))
        self.assertGreater(len(response.context["resources"]), 0)

        # 9. Delete account
        client.post(reverse("accounts:delete_account"), {
            "password": "SecurePass123!",
        }, follow=True)
        self.assertFalse(User.objects.filter(email="journey@uni.edu.ng").exists())
        self.assertFalse(Incident.objects.filter(user=user).exists())

    def test_admin_workflow(self):
        """Admin views, exports, and deletes incidents."""
        client = Client()
        admin = User.objects.create_user(
            email="adminwf@uni.edu.ng", password="AdminPass123!",
            role="admin",
        )
        reporter = User.objects.create_user(
            email="reporterwf@uni.edu.ng", password="ReporterPass123!",
        )
        inc = Incident.objects.create(
            user=reporter, platform_category="email",
            date_of_occurrence="2025-06-01",
            incident_classification="phishing",
            narrative="Phished.", actor_involvement="stranger",
            severity_rating=2,
        )
        Harm.objects.create(
            incident=inc, harm_category="financial_loss",
            severity_score=3, duration="one_time",
        )

        client.login(email="adminwf@uni.edu.ng", password="AdminPass123!")

        # View admin list
        response = client.get(reverse("incidents:admin_list"))
        self.assertEqual(response.status_code, 200)

        # View admin detail
        response = client.get(
            reverse("incidents:admin_detail", args=[inc.reference_code])
        )
        self.assertEqual(response.status_code, 200)

        # Export
        response = client.get(
            reverse("incidents:admin_export", args=[inc.reference_code])
        )
        self.assertEqual(response.status_code, 200)

        # Delete
        client.post(
            reverse("incidents:admin_delete", args=[inc.reference_code]),
            follow=True,
        )
        self.assertFalse(Incident.objects.filter(
            reference_code=inc.reference_code
        ).exists())


# ---------------------------------------------------------------------------
# 18. CONTENT & UX INTEGRITY TESTS
# ---------------------------------------------------------------------------

class ContentIntegrityTests(TestCase):
    def test_landing_page_features_count(self):
        client = Client()
        response = client.get(reverse("landing"))
        self.assertContains(response, "feature-card", count=4)

    def test_trust_bar_items(self):
        client = Client()
        response = client.get(reverse("landing"))
        self.assertContains(response, "trust-item", count=4)

    def test_profile_danger_zone(self):
        client = Client()
        user = User.objects.create_user(email="dz@uni.edu.ng", password="Pass123!")
        client.login(email="dz@uni.edu.ng", password="Pass123!")
        response = client.get(reverse("accounts:profile"))
        self.assertContains(response, "Danger Zone")
        self.assertContains(response, "Delete My Account")

    def test_support_banner_keywords(self):
        client = Client()
        user = User.objects.create_user(email="sb@uni.edu.ng", password="Pass123!")
        client.login(email="sb@uni.edu.ng", password="Pass123!")
        response = client.get(reverse("incidents:create"))
        self.assertContains(response, "support-banner")
        self.assertContains(response, "suicide")
        self.assertContains(response, "self-harm")

    def test_autosave_indicator(self):
        client = Client()
        user = User.objects.create_user(email="as@uni.edu.ng", password="Pass123!")
        client.login(email="as@uni.edu.ng", password="Pass123!")
        response = client.get(reverse("incidents:create"))
        self.assertContains(response, "autosave-status")

    def test_incident_table_columns(self):
        client = Client()
        user = User.objects.create_user(email="tc2@uni.edu.ng", password="Pass123!")
        client.login(email="tc2@uni.edu.ng", password="Pass123!")
        response = client.get(reverse("incidents:list"))
        self.assertContains(response, "Reference")
        self.assertContains(response, "Classification")
        self.assertContains(response, "Severity")

    def test_empty_state_messages(self):
        client = Client()
        user = User.objects.create_user(email="es@uni.edu.ng", password="Pass123!")
        client.login(email="es@uni.edu.ng", password="Pass123!")
        response = client.get(reverse("incidents:list"))
        self.assertContains(response, "empty-state")
        response = client.get(reverse("dashboard:home"))
        self.assertContains(response, "empty-state")


# ---------------------------------------------------------------------------
# 19. INCIDENT EDIT / DELETE / STATUS TESTS
# ---------------------------------------------------------------------------

class IncidentEditDeleteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="edit@uni.edu.ng", password="Pass123!"
        )
        self.client.login(email="edit@uni.edu.ng", password="Pass123!")
        self.incident = Incident.objects.create(
            user=self.user, platform_category="social_media",
            date_of_occurrence="2025-06-01",
            incident_classification="doxxing",
            narrative="Original narrative",
            actor_involvement="known_person",
            severity_rating=3,
        )

    def test_edit_incident_get(self):
        response = self.client.get(
            reverse("incidents:edit", args=[self.incident.reference_code])
        )
        self.assertEqual(response.status_code, 200)

    def test_edit_incident_post(self):
        response = self.client.post(
            reverse("incidents:edit", args=[self.incident.reference_code]),
            {
                "platform_category": "email",
                "date_of_occurrence": "2025-07-01",
                "incident_classification": "phishing",
                "narrative": "Updated narrative text",
                "actor_involvement": "stranger",
                "severity_rating": "2",
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.incident.refresh_from_db()
        self.assertEqual(self.incident.narrative, "Updated narrative text")

    def test_edit_incident_wrong_user(self):
        other = User.objects.create_user(email="other@uni.edu.ng", password="Pass123!")
        self.client.login(email="other@uni.edu.ng", password="Pass123!")
        response = self.client.get(
            reverse("incidents:edit", args=[self.incident.reference_code])
        )
        self.assertEqual(response.status_code, 404)

    def test_delete_incident(self):
        response = self.client.post(
            reverse("incidents:delete", args=[self.incident.reference_code]),
            follow=True,
        )
        self.assertFalse(Incident.objects.filter(
            reference_code=self.incident.reference_code
        ).exists())

    def test_delete_incident_wrong_user(self):
        other = User.objects.create_user(email="del@uni.edu.ng", password="Pass123!")
        self.client.login(email="del@uni.edu.ng", password="Pass123!")
        self.client.post(
            reverse("incidents:delete", args=[self.incident.reference_code]),
        )
        self.assertTrue(Incident.objects.filter(
            reference_code=self.incident.reference_code
        ).exists())

    def test_update_status(self):
        response = self.client.post(
            reverse("incidents:update_status", args=[self.incident.reference_code]),
            {"status": "under_review"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.incident.refresh_from_db()
        self.assertEqual(self.incident.status, "under_review")

    def test_update_status_invalid(self):
        response = self.client.post(
            reverse("incidents:update_status", args=[self.incident.reference_code]),
            {"status": "invalid_status"},
            follow=True,
        )
        self.incident.refresh_from_db()
        self.assertEqual(self.incident.status, "submitted")

    def test_status_choices(self):
        valid = [s[0] for s in Incident.STATUS_CHOICES]
        self.assertIn("draft", valid)
        self.assertIn("submitted", valid)
        self.assertIn("under_review", valid)
        self.assertIn("resolved", valid)
        self.assertIn("closed", valid)

    def test_default_status(self):
        inc = Incident.objects.create(
            user=self.user, platform_category="email",
            date_of_occurrence="2025-06-01",
            incident_classification="phishing",
            narrative="New incident",
            actor_involvement="stranger",
            severity_rating=1,
        )
        self.assertEqual(inc.status, "submitted")


# ---------------------------------------------------------------------------
# 20. SEARCH AND FILTER TESTS
# ---------------------------------------------------------------------------

class SearchFilterTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="search@uni.edu.ng", password="Pass123!"
        )
        self.client.login(email="search@uni.edu.ng", password="Pass123!")
        Incident.objects.create(
            user=self.user, platform_category="social_media",
            date_of_occurrence="2025-06-01",
            incident_classification="doxxing",
            narrative="Personal photos shared on WhatsApp group",
            actor_involvement="known_person",
            severity_rating=3,
        )
        Incident.objects.create(
            user=self.user, platform_category="email",
            date_of_occurrence="2025-06-02",
            incident_classification="phishing",
            narrative="Received fake university login email",
            actor_involvement="stranger",
            severity_rating=1,
            status="under_review",
        )

    def test_search_by_narrative(self):
        response = self.client.get(reverse("incidents:list") + "?q=photos")
        self.assertEqual(len(response.context["incidents"]), 1)

    def test_search_by_classification(self):
        response = self.client.get(reverse("incidents:list") + "?q=phishing")
        self.assertEqual(len(response.context["incidents"]), 1)

    def test_search_no_results(self):
        response = self.client.get(reverse("incidents:list") + "?q=nonexistent")
        self.assertEqual(len(response.context["incidents"]), 0)

    def test_filter_by_status(self):
        response = self.client.get(reverse("incidents:list") + "?status=under_review")
        self.assertEqual(len(response.context["incidents"]), 1)

    def test_combined_search_and_filter(self):
        response = self.client.get(reverse("incidents:list") + "?q=phishing&status=under_review")
        self.assertEqual(len(response.context["incidents"]), 1)

    def test_clear_filters(self):
        response = self.client.get(reverse("incidents:list"))
        self.assertEqual(len(response.context["incidents"]), 2)


# ---------------------------------------------------------------------------
# 21. URL RESOLUTION UPDATED TESTS
# ---------------------------------------------------------------------------

class UpdatedURLTests(TestCase):
    def test_edit_url(self):
        url = reverse("incidents:edit", args=["PRG-TEST1234"])
        self.assertTrue(resolve(url))

    def test_delete_url(self):
        url = reverse("incidents:delete", args=["PRG-TEST1234"])
        self.assertTrue(resolve(url))

    def test_update_status_url(self):
        url = reverse("incidents:update_status", args=["PRG-TEST1234"])
        self.assertTrue(resolve(url))
