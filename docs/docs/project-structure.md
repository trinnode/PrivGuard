---
sidebar_position: 2
title: Project Structure
---

# Project Structure

```
PrivGuard/
├── accounts/                    # Authentication and user management
│   ├── __init__.py
│   ├── admin.py                 # Admin panel registration
│   ├── apps.py                  # App configuration
│   ├── decorators.py            # Role-based access control decorators
│   ├── forms.py                 # Registration and profile forms
│   ├── middleware.py             # Session timeout enforcement
│   ├── models.py                # Custom User model
│   ├── urls.py                  # Account URL routing
│   └── views.py                 # Login, register, logout, profile, password reset
│
├── incidents/                   # Core incident reporting system
│   ├── __init__.py
│   ├── admin.py                 # Admin panel registration
│   ├── apps.py                  # App configuration
│   ├── forms.py                 # Incident form with harm inline sets
│   ├── models.py                # Incident, Harm, AuditLog models
│   ├── taxonomy.py              # 17-category harm taxonomy, platform/classification enums
│   ├── urls.py                  # Incident URL routing
│   ├── views.py                 # CRUD, admin dashboard, PDF export
│   ├── management/
│   │   └── commands/
│   │       ├── populate_users_data.py   # Synthetic student data generator
│   │       └── seed_resources.py        # Resource seeder
│   └── templatetags/
│       └── incident_extras.py   # Custom template filters
│
├── resources/                   # Support resource library
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py                # Resource model with recommendation engine
│   ├── urls.py
│   └── views.py                 # Resource listing, detail, recommendation
│
├── reporting/                   # PDF export engine
│   ├── __init__.py
│   ├── apps.py
│   ├── pdf_generator.py         # ReportLab document assembly
│   ├── text_fallback.py         # Plain-text fallback on PDF failure
│   ├── urls.py
│   └── views.py                 # Single + bulk PDF generation
│
├── dashboard/                   # User dashboard
│   ├── __init__.py
│   ├── apps.py
│   ├── urls.py
│   ├── views.py                 # Dashboard stats, harm distribution
│   └── templatetags/
│       └── dashboard_extras.py
│
├── ragnar/                      # Django project configuration
│   ├── __init__.py
│   ├── settings.py              # All Django settings
│   ├── urls.py                  # Root URL configuration
│   ├── wsgi.py                  # WSGI entry point
│   └── asgi.py                  # ASGI entry point
│
├── templates/                   # All HTML templates
│   ├── base.html                # Base layout (dark mode, nav, footer)
│   ├── 404.html                 # Custom error page
│   ├── accounts/
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── profile.html
│   │   └── password_reset*.html  # Password reset flow (5 templates)
│   ├── incidents/
│   │   ├── create.html          # Multi-step incident creation wizard
│   │   ├── detail.html          # Incident detail with harm list
│   │   ├── edit.html            # Edit incident
│   │   ├── list.html            # User's incident list
│   │   ├── admin_list.html      # Admin dashboard with filters
│   │   └── admin_detail.html    # Admin incident detail with grant/deny
│   ├── resources/
│   │   ├── list.html            # Resource library
│   │   └── detail.html          # Resource detail with contact info
│   ├── reporting/
│   │   └── export.html          # PDF download page
│   └── dashboard/
│       └── home.html            # User dashboard
│
├── static/                      # Frontend assets
│   ├── css/main.css             # Full design system (dark/light, responsive)
│   ├── js/main.js               # Theme toggle, autosave, form helpers
│   ├── images/logo.svg          # Application logo
│   └── images/favicon.svg       # Browser tab icon
│
├── tests/                       # Test suite
│   ├── test_models.py           # Model integrity and constraints
│   ├── test_views.py            # Authentication flow and view rendering
│   ├── test_concealment.py      # Concealment lifecycle tests
│   ├── test_comprehensive.py    # CRUD, security, session, upload, PDF tests
│   ├── test_e2e.py              # End-to-end scenario tests
│   ├── test_runner.py           # Custom test runner
│   └── conftest.py              # Shared pytest fixtures
│
├── media/                       # User-uploaded files (gitignored)
│   └── evidence/                # Incident evidence files
│
├── docs/                        # Docusaurus documentation
│   ├── docs/                    # Markdown documentation pages
│   ├── src/                     # Docusaurus React components
│   ├── docusaurus.config.js
│   ├── sidebars.js
│   └── package.json
│
├── docker/                      # Deployment scripts
│   └── entrypoint.sh            # Container startup (migrate, collectstatic, gunicorn)
│
├── setup.sh                     # One-shot cross-platform setup script
├── Dockerfile                   # Multi-stage production build
├── docker-compose.yml           # PostgreSQL + Django services
├── vercel.json                  # Vercel serverless configuration
├── railway.json                 # Railway deployment
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variable template
├── .gitignore                   # Git ignore rules
└── manage.py                    # Django management entry point
```

## Key Files

| File | Purpose |
|------|---------|
| `ragnar/settings.py` | All Django configuration — security, database, apps, middleware, static files |
| `incidents/taxonomy.py` | Defines all enums: harm categories, platforms, classifications, severity levels |
| `incidents/models.py` | Core data models — Incident, Harm, AuditLog, with concealment logic |
| `incidents/views.py` | All incident CRUD, admin dashboard, PDF export triggers |
| `resources/models.py` | Resource model with `recommended_for()` classmethod |
| `setup.sh` | Cross-platform environment setup with version-aware package installation |
| `requirements.txt` | Pinned Python dependencies |
| `Dockerfile` | Multi-stage production build (Python 3.12, Gunicorn) |
