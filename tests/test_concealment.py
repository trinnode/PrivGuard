"""
PrivGuard — Identity concealment tests
=======================================
Covers pending-request on user request, admin grant/deny/revoke, redaction of
reporter identity in exports, and the admin toggle endpoint.
Run: python manage.py test tests.test_concealment -v2
"""
import base64
import re
import zlib

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages

from incidents.models import Incident, Harm
from reporting.pdf_generator import (
    generate_text_summary,
    generate_bulk_report,
    redact_identity,
    should_conceal,
)

User = get_user_model()


def pdf_text(content):
    """Extract decompressed text streams from a ReportLab PDF byte string."""
    text = []
    for match in re.finditer(rb"stream\r?\n(.*?)endstream", content, re.DOTALL):
        data = match.group(1)
        try:
            data = base64.a85decode(data, adobe=True)
        except Exception:
            pass
        try:
            data = zlib.decompress(data)
        except Exception:
            pass
        text.append(data)
    return b"".join(text)


class AutoGrantModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="conceal@uni.edu.ng", password="Pass123!", full_name="Ada Lovelace",
            institution="FUT Minna",
        )

    def test_request_becomes_pending(self):
        inc = Incident.objects.create(
            user=self.user, platform_category="social_media",
            date_of_occurrence="2025-06-01",
            incident_classification="doxxing",
            narrative="Test", actor_involvement="stranger",
            severity_rating=1, anonymize_requested=True,
        )
        inc.refresh_from_db()
        self.assertEqual(inc.concealment_status, "requested")
        self.assertFalse(inc.concealment_active)

    def test_no_request_keeps_none(self):
        inc = Incident.objects.create(
            user=self.user, platform_category="social_media",
            date_of_occurrence="2025-06-01",
            incident_classification="doxxing",
            narrative="Test", actor_involvement="stranger",
            severity_rating=1,
        )
        inc.refresh_from_db()
        self.assertEqual(inc.concealment_status, "none")
        self.assertFalse(inc.concealment_active)

    def test_withdraw_request_disables(self):
        inc = Incident.objects.create(
            user=self.user, platform_category="social_media",
            date_of_occurrence="2025-06-01",
            incident_classification="doxxing",
            narrative="Test", actor_involvement="stranger",
            severity_rating=1, anonymize_requested=True,
        )
        inc.anonymize_requested = False
        inc.save()
        inc.refresh_from_db()
        self.assertEqual(inc.concealment_status, "none")
        self.assertFalse(inc.concealment_active)

    def test_admin_deny_overrides_request(self):
        inc = Incident.objects.create(
            user=self.user, platform_category="social_media",
            date_of_occurrence="2025-06-01",
            incident_classification="doxxing",
            narrative="Test", actor_involvement="stranger",
            severity_rating=1, anonymize_requested=True,
        )
        inc.concealment_status = "revoked"
        inc.anonymize_requested = False
        inc.save()
        inc.refresh_from_db()
        self.assertFalse(inc.concealment_active)
        # Re-requesting must not override an admin denial.
        inc.anonymize_requested = True
        inc.save()
        inc.refresh_from_db()
        self.assertEqual(inc.concealment_status, "revoked")
        self.assertFalse(inc.concealment_active)

    def test_admin_grant_activates(self):
        inc = Incident.objects.create(
            user=self.user, platform_category="social_media",
            date_of_occurrence="2025-06-01",
            incident_classification="doxxing",
            narrative="Test", actor_involvement="stranger",
            severity_rating=1,
        )
        inc.concealment_status = "granted"
        inc.anonymize_requested = True
        inc.save()
        inc.refresh_from_db()
        self.assertTrue(inc.concealment_active)

    def test_user_level_anonymize_applies(self):
        inc = Incident.objects.create(
            user=self.user, platform_category="social_media",
            date_of_occurrence="2025-06-01",
            incident_classification="doxxing",
            narrative="Test", actor_involvement="stranger",
            severity_rating=1,
        )
        self.user.anonymize_requested = True
        self.user.save(update_fields=["anonymize_requested"])
        inc = Incident.objects.get(pk=inc.pk)
        self.assertTrue(inc.concealment_active)


class RedactionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="victim@uni.edu.ng", password="Pass123!",
            full_name="Chinwe Okafor", institution="Federal University of Technology Minna",
        )
        self.incident = Incident.objects.create(
            user=self.user, platform_category="email",
            date_of_occurrence="2025-06-01",
            incident_classification="phishing",
            narrative=(
                "victim@uni.edu.ng was targeted. My name is Chinwe Okafor "
                "and I study at Federal University of Technology Minna."
            ),
            actor_involvement="stranger",
            severity_rating=2,
        )

    def test_redact_identity_replaces_markers(self):
        out = redact_identity(self.incident.narrative, self.incident)
        self.assertNotIn("victim@uni.edu.ng", out)
        self.assertNotIn("Chinwe Okafor", out)
        self.assertNotIn("Federal University of Technology Minna", out)
        self.assertIn("[REDACTED]", out)

    def test_redact_identity_passthrough(self):
        out = redact_identity("Nothing personal here.", self.incident)
        self.assertEqual(out, "Nothing personal here.")

    def test_redact_identity_none(self):
        self.assertIsNone(redact_identity(None, self.incident))

    def test_should_conceal(self):
        self.assertFalse(should_conceal(self.incident))
        self.incident.anonymize_requested = True
        self.incident.concealment_status = "granted"
        self.incident.save()
        self.incident.refresh_from_db()
        self.assertTrue(should_conceal(self.incident))

    def test_text_summary_redacted(self):
        text = generate_text_summary(self.incident, conceal=True)
        self.assertIn("[REDACTED]", text)
        self.assertIn("IDENTITY CONCEALMENT ENABLED", text)
        self.assertNotIn("victim@uni.edu.ng", text)

    def test_text_summary_unredacted(self):
        text = generate_text_summary(self.incident, conceal=False)
        self.assertIn("victim@uni.edu.ng", text)
        self.assertNotIn("[REDACTED]", text)


class AdminToggleTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_user(
            email="admin@uni.edu.ng", password="AdminPass123!", role="admin",
        )
        self.normal = User.objects.create_user(
            email="normal@uni.edu.ng", password="NormalPass123!",
        )
        self.incident = Incident.objects.create(
            user=self.normal, platform_category="social_media",
            date_of_occurrence="2025-06-01",
            incident_classification="doxxing",
            narrative="Test", actor_involvement="stranger",
            severity_rating=3,
        )

    def test_non_admin_cannot_toggle(self):
        self.client.login(email="normal@uni.edu.ng", password="NormalPass123!")
        response = self.client.post(
            reverse("incidents:admin_toggle_concealment", args=[self.incident.reference_code]),
            {"action": "grant"}, follow=True,
        )
        self.incident.refresh_from_db()
        self.assertNotEqual(self.incident.concealment_status, "granted")

    def test_admin_grants(self):
        self.client.login(email="admin@uni.edu.ng", password="AdminPass123!")
        response = self.client.post(
            reverse("incidents:admin_toggle_concealment", args=[self.incident.reference_code]),
            {"action": "grant"}, follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.incident.refresh_from_db()
        self.assertEqual(self.incident.concealment_status, "granted")
        self.assertTrue(self.incident.anonymize_requested)
        self.assertTrue(self.incident.concealment_active)

    def test_admin_revokes(self):
        self.incident.anonymize_requested = True
        self.incident.concealment_status = "granted"
        self.incident.save()
        self.incident.refresh_from_db()
        self.assertTrue(self.incident.concealment_active)

        self.client.login(email="admin@uni.edu.ng", password="AdminPass123!")
        response = self.client.post(
            reverse("incidents:admin_toggle_concealment", args=[self.incident.reference_code]),
            {"action": "revoke"}, follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.incident.refresh_from_db()
        self.assertEqual(self.incident.concealment_status, "revoked")
        self.assertFalse(self.incident.concealment_active)

    def test_admin_denies_pending_request(self):
        self.incident.anonymize_requested = True
        self.incident.save()
        self.incident.refresh_from_db()
        self.assertEqual(self.incident.concealment_status, "requested")

        self.client.login(email="admin@uni.edu.ng", password="AdminPass123!")
        response = self.client.post(
            reverse("incidents:admin_toggle_concealment", args=[self.incident.reference_code]),
            {"action": "deny"}, follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.incident.refresh_from_db()
        self.assertEqual(self.incident.concealment_status, "revoked")
        self.assertFalse(self.incident.anonymize_requested)
        self.assertFalse(self.incident.concealment_active)

    def test_admin_export_page_shows_redaction(self):
        self.incident.anonymize_requested = True
        self.incident.concealment_status = "granted"
        self.incident.save()
        self.client.login(email="admin@uni.edu.ng", password="AdminPass123!")
        response = self.client.get(
            reverse("incidents:admin_export", args=[self.incident.reference_code])
        )
        self.assertContains(response, "Identity concealment is enabled")


class BulkExportRedactionTests(TestCase):
    def test_bulk_report_redacts(self):
        user = User.objects.create_user(
            email="bulk@uni.edu.ng", password="Pass123!",
        )
        inc = Incident.objects.create(
            user=user, platform_category="social_media",
            date_of_occurrence="2025-06-01",
            incident_classification="doxxing",
            narrative="Bulk narrative mentioning bulk@uni.edu.ng",
            actor_involvement="stranger",
            severity_rating=3, anonymize_requested=True,
            concealment_status="granted",
        )
        buffer = generate_bulk_report(Incident.objects.filter(pk=inc.pk))
        content = buffer.read()
        decoded = pdf_text(content)
        self.assertTrue(content.startswith(b"%PDF"))
        self.assertIn(b"[REDACTED]", decoded)
        self.assertNotIn(b"bulk@uni.edu.ng", decoded)

    def test_bulk_report_shows_email_when_not_concealed(self):
        user = User.objects.create_user(
            email="visible@uni.edu.ng", password="Pass123!",
        )
        inc = Incident.objects.create(
            user=user, platform_category="social_media",
            date_of_occurrence="2025-06-01",
            incident_classification="doxxing",
            narrative="Visible narrative.",
            actor_involvement="stranger",
            severity_rating=3,
        )
        buffer = generate_bulk_report(Incident.objects.filter(pk=inc.pk))
        content = buffer.read()
        decoded = pdf_text(content)
        self.assertIn(b"visible@uni.edu.ng", decoded)
        self.assertNotIn(b"[REDACTED]", decoded)
