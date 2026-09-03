---
sidebar_position: 6
title: Security
---

# Security

PrivGuard implements industry-standard security measures to protect user data and ensure privacy.

## Authentication & Passwords

| Feature | Implementation |
|---------|---------------|
| Password hashing | Argon2id (via `argon2-cffi`) with automatic algorithm upgrade |
| Password policy | Minimum 8 characters, enforced at registration |
| Session management | Django session framework with 15-minute inactivity timeout |
| Session expiry | Automatic logout when session times out |

## Session Timeout

The `SessionTimeoutMiddleware` enforces a 15-minute inactivity window:

1. Each authenticated request resets the timeout timer
2. If no request is made within 15 minutes, the session expires
3. The user is redirected to the login page with a "session expired" message
4. CSRF token is preserved across the redirect to prevent form resubmission issues

## CSRF Protection

All forms include Django's CSRF middleware:

- **Cookie**: `httponly=True`, `samesite=strict`
- **Token**: Unique per session, validated on every POST request
- **Header**: Also accepted via `X-CSRFToken` header for AJAX requests

## Cookie Security

| Cookie | `httponly` | `samesite` | `Secure` |
|--------|-----------|------------|----------|
| Session | Yes | Strict | Configurable |
| CSRF | Yes | Strict | Configurable |
| Analytics | Yes | Strict | Yes |

In production, set:
```bash
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

## HTTPS Enforcement

```bash
SECURE_SSL_REDIRECT=True  # Redirects all HTTP to HTTPS
```

When enabled, all non-HTTPS requests are automatically redirected to HTTPS. This should be enabled in production behind a reverse proxy (Nginx, Caddy) or on managed platforms (Vercel, Railway).

## Input Validation

| Check | Implementation |
|-------|---------------|
| XSS prevention | Django template auto-escaping on all user content |
| SQL injection | Django ORM parameterised queries (no raw SQL) |
| File upload validation | MIME type checking, 100 KB size limit |
| Clickjacking | `X-Frame-Options: DENY` header |
| Content-Type sniffing | `X-Content-Type-Options: nosniff` header |

## File Upload Security

| Rule | Value |
|------|-------|
| Maximum size | 100 KB (`MAX_UPLOAD_SIZE = 100 * 1024`) |
| Allowed types | PNG, JPEG, PDF |
| Storage location | `media/evidence/` (outside web root) |
| Naming | Randomised to prevent path traversal |

## Audit Logging

Every significant action is logged in the `AuditLog` model:

| Event Type | Description |
|-----------|-------------|
| `LOGIN` | User authenticated successfully |
| `LOGOUT` | User logged out |
| `INCIDENT_CREATED` | New incident report submitted |
| `INCIDENT_UPDATED` | Incident modified |
| `INCIDENT_EXPORTED` | PDF exported |
| `CONCEALMENT_REQUESTED` | Concealment request submitted |
| `CONCEALMENT_GRANTED` | Admin approved concealment |
| `CONCEALMENT_DENIED` | Admin denied concealment |
| `CONCEALMENT_REVOKED` | Admin revoked concealment |
| `ACCOUNT_DELETED` | User account deleted |

Each entry records:
- **Timestamp** — when the event occurred
- **User** — who performed the action
- **Event type** — categorised from the list above
- **Action summary** — human-readable description
- **IP hash** — SHA-256 hash of the user's IP address (not the raw IP)

## Data Isolation

- Users can only see their own incidents (unless they are admin)
- Admin views show all incidents but conceal identities when concealment is active
- PDF exports respect concealment status at generation time
- The `populate_users_data` command creates isolated, non-overlapping demo data

## Deployment Security

| Setting | Development | Production |
|---------|-------------|------------|
| `DEBUG` | `True` | `False` |
| `SECURE_SSL_REDIRECT` | `False` | `True` |
| `SESSION_COOKIE_SECURE` | `False` | `True` |
| `CSRF_COOKIE_SECURE` | `False` | `True` |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | Your domain |
| `SECRET_KEY` | Auto-generated | Strong, unique key |

## Security Checklist for Production

- [ ] `DJANGO_DEBUG=False`
- [ ] Strong, unique `DJANGO_SECRET_KEY` (48+ characters)
- [ ] `SESSION_COOKIE_SECURE=True`
- [ ] `CSRF_COOKIE_SECURE=True`
- [ ] `SECURE_SSL_REDIRECT=True`
- [ ] `DJANGO_ALLOWED_HOSTS` set to your domain(s)
- [ ] PostgreSQL credentials are strong and unique
- [ ] File uploads are disabled or properly validated
- [ ] Admin panel is behind authentication
- [ ] Default admin password has been changed
