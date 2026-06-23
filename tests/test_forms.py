from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.forms import RegistrationForm, LoginForm
from incidents.forms import IncidentForm

User = get_user_model()


class RegistrationFormTests(TestCase):
    def test_valid_registration(self):
        form = RegistrationForm(data={
            "email": "newstudent@uni.edu.ng",
            "full_name": "New Student",
            "institution": "University of Ibadan",
            "password1": "securepass123",
            "password2": "securepass123",
        })
        self.assertTrue(form.is_valid())

    def test_mismatched_passwords(self):
        form = RegistrationForm(data={
            "email": "student@uni.edu.ng",
            "password1": "password123",
            "password2": "different123",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_short_password(self):
        form = RegistrationForm(data={
            "email": "student@uni.edu.ng",
            "password1": "short",
            "password2": "short",
        })
        self.assertFalse(form.is_valid())

    def test_duplicate_email(self):
        User.objects.create_user(email="existing@uni.edu.ng", password="testpass123")
        form = RegistrationForm(data={
            "email": "existing@uni.edu.ng",
            "password1": "testpass123",
            "password2": "testpass123",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)


class IncidentFormTests(TestCase):
    def test_valid_incident(self):
        form = IncidentForm(data={
            "platform_category": "social_media",
            "date_of_occurrence": "2025-09-15",
            "incident_classification": "doxxing",
            "narrative": "My personal details were shared online.",
            "actor_involvement": "known_person",
            "severity_rating": 3,
        })
        self.assertTrue(form.is_valid())

    def test_missing_required_fields(self):
        form = IncidentForm(data={})
        self.assertFalse(form.is_valid())
        required_fields = ["platform_category", "date_of_occurrence",
                          "incident_classification", "narrative",
                          "actor_involvement", "severity_rating"]
        for field in required_fields:
            self.assertIn(field, form.errors)
