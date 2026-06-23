from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from incidents.models import Incident

User = get_user_model()


class LandingPageTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_landing_page_status(self):
        response = self.client.get(reverse("landing"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "landing.html")


class AuthenticationFlowTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse("accounts:register")
        self.login_url = reverse("accounts:login")

    def test_registration_page_loads(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)

    def test_successful_registration(self):
        response = self.client.post(self.register_url, {
            "email": "student@uni.edu.ng",
            "full_name": "Test Student",
            "institution": "University of Lagos",
            "password1": "securepass123",
            "password2": "securepass123",
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(email="student@uni.edu.ng").exists())

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


class IncidentFlowTests(TestCase):
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

    def test_create_incident(self):
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


class DashboardTests(TestCase):
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
