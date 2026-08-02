from django.test import TestCase
from django.contrib.auth import get_user_model
from incidents.models import Incident, Harm, AuditLog
from incidents.taxonomy import HARM_CATEGORIES

User = get_user_model()


class UserModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@student.edu.ng",
            password="testpass123",
            full_name="Test Student",
        )

    def test_user_creation(self):
        self.assertEqual(self.user.email, "test@student.edu.ng")
        self.assertTrue(self.user.check_password("testpass123"))
        self.assertFalse(self.user.consent_granted)

    def test_consent_toggle(self):
        self.user.record_consent()
        self.assertTrue(self.user.consent_granted)
        self.assertIsNotNone(self.user.consent_date)

        self.user.revoke_consent()
        self.assertFalse(self.user.consent_granted)
        self.assertIsNone(self.user.consent_date)

    def test_email_uniqueness(self):
        with self.assertRaises(Exception):
            User.objects.create_user(
                email="test@student.edu.ng",
                password="anotherpass",
            )


class IncidentModelTests(TestCase):
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
        self.assertTrue(incident.reference_code.startswith("PRG-"))
        self.assertEqual(incident.user, self.user)
        self.assertEqual(incident.harms.count(), 0)

    def test_reference_code_generation(self):
        i1 = Incident.objects.create(
            user=self.user,
            platform_category="email",
            date_of_occurrence="2025-01-01",
            incident_classification="phishing",
            narrative="Test",
            actor_involvement="stranger",
            severity_rating=2,
        )
        i2 = Incident.objects.create(
            user=self.user,
            platform_category="email",
            date_of_occurrence="2025-01-01",
            incident_classification="phishing",
            narrative="Test",
            actor_involvement="stranger",
            severity_rating=2,
        )
        self.assertNotEqual(i1.reference_code, i2.reference_code)


class HarmModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="t@t.com", password="pass")
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
        self.assertEqual(harm.get_harm_category_display(), "Anxiety - Persistent worry or fear about digital safety")

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


class AuditLogTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="admin@r.com", password="pass")

    def test_audit_log_creation(self):
        log = AuditLog.objects.create(
            event_type="login",
            user=self.user,
            action_summary="User logged in",
            ip_hash="abc123",
        )
        self.assertEqual(log.event_type, "login")
        self.assertEqual(str(log), f"Login - {log.timestamp.strftime('%Y-%m-%d %H:%M')}")
