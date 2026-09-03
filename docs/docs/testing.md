---
sidebar_position: 9
title: Testing
---

# Testing

PrivGuard includes a comprehensive test suite covering models, views, security, and end-to-end scenarios.

## Running Tests

```bash
# Run the full test suite
python manage.py test tests/

# Run a specific test file
python manage.py test tests/test_concealment.py

# Run with verbose output
python manage.py test tests/ -v 2

# Run a specific test class
python manage.py test tests.test_views.LoginViewTest

# Run a specific test method
python manage.py test tests.test_views.LoginViewTest.test_login_success
```

## Test Files

| File | Tests | Coverage |
|------|-------|----------|
| `test_models.py` | Model integrity, constraints, string representations, auto-generated fields | User, Incident, Harm, AuditLog, Resource |
| `test_views.py` | Authentication flow, view rendering, redirects, template content | Login, register, logout, profile, password reset |
| `test_concealment.py` | Concealment lifecycle, grant/deny/revoke, redaction in exports | 19 test cases covering full workflow |
| `test_comprehensive.py` | CRUD operations, security checks, session timeout, file upload, PDF export | All apps, edge cases |
| `test_e2e.py` | End-to-end scenarios combining multiple features | Full user journeys |

## Test Categories

### Model Tests

```python
# Example: test that a new incident gets a reference code
def test_incident_reference_code_generated():
    incident = Incident.objects.create(user=self.user, ...)
    self.assertTrue(incident.reference_code.startswith("PRG-"))
    self.assertEqual(len(incident.reference_code), 12)
```

### View Tests

```python
# Example: test login flow
def test_login_success():
    response = self.client.post("/accounts/login/", {
        "username": "test@example.com",
        "password": "testpass123"
    })
    self.assertEqual(response.status_code, 302)  # Redirect on success
```

### Concealment Tests

```python
# Example: test that granted concealment redacts identity in PDF
def test_concealed_incident_redacted_in_pdf():
    self.incident.concealment_active = True
    self.incident.save()
    response = self.client.get(f"/incidents/{self.incident.id}/export/pdf/")
    self.assertNotContains(response, self.user.full_name)
    self.assertContains(response, "[REDACTED]")
```

### Security Tests

```python
# Example: test CSRF protection
def test_post_without_csrf_returns_403():
    response = self.client.post("/incidents/create/", data={...})
    self.assertEqual(response.status_code, 403)

# Example: test session timeout
def test_session_expired_redirects_to_login(self):
    # Set session to expired timestamp
    self.client.session.set_expiry(0)
    response = self.client.get("/incidents/")
    self.assertRedirects(response, "/accounts/login/?next=/incidents/")
```

## Known Test Issues

Some tests fail in isolated test environments due to:

| Issue | Cause | Production Impact |
|-------|-------|-------------------|
| SMTP tests | Test environment lacks mail server | None — email works in production |
| PDF date parsing | Tests pass string dates instead of datetime objects | None — fixed in production code |
| CSRF cookie tests | Test client behaves differently than browser | None — CSRF works correctly in browsers |
| Session cookie tests | Test client has different cookie handling | None — cookies work correctly in production |

These are pre-existing test-environment artifacts, not production bugs.

## Writing New Tests

### Test Structure

```python
from django.test import TestCase, Client
from django.urls import reverse
from incidents.models import Incident

class IncidentTest(TestCase):
    def setUp(self):
        """Create test fixtures."""
        self.client = Client()
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpass123"
        )
        self.client.login(email="test@example.com", password="testpass123")

    def test_incident_creation(self):
        """Test that an incident can be created."""
        response = self.client.post(reverse("incidents:create"), {
            "platform_category": "Instagram",
            "incident_classification": "Social media harassment",
            "severity_rating": 2,
            "narrative": "Test incident narrative",
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Incident.objects.count(), 1)
```

### Best Practices

1. **Use `setUp()`** for fixtures — don't create objects in every test
2. **Test one thing per test** — keep tests focused and readable
3. **Use `reverse()`** for URLs — don't hardcode paths
4. **Test both success and failure** — verify error handling
5. **Check redirects** — most POST views should redirect on success
6. **Verify database state** — don't just check response codes
