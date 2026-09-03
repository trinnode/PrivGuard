<p align="center">
  <img src="static/images/logo.svg" alt="PrivGuard" width="100">
</p>

<h1 align="center">PrivGuard</h1>

<p align="center">
  <strong>Privacy Incident Reporting System for Nigerian University Students</strong>
</p>

<p align="center">
  A web-based platform that enables university students to document digital privacy violations, classify associated psychological and tangible harms using an adapted academic taxonomy, access context-appropriate guidance, and export structured reports.
</p>

<p align="center">
  <a href="#quick-start">Quick Start</a> ·
  <a href="#features">Features</a> ·
  <a href="#documentation">Documentation</a> ·
  <a href="#deployment">Deployment</a> ·
  <a href="#testing">Testing</a>
</p>

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python 3.10+ / Django 5.0 |
| **Database** | PostgreSQL 14+ (via `psycopg2-binary` + `dj-database-url`) |
| **Frontend** | HTML5, CSS3 (custom dark/light design system), vanilla JavaScript |
| **PDF Export** | ReportLab with per-incident identity redaction |
| **Authentication** | Django session management, Argon2 password hashing (PBKDF2 fallback) |
| **File Upload** | UploadThing (cloud) with local `MEDIA_ROOT` fallback |
| **Static Files** | WhiteNoise with gzip/brotli compression |
| **Deployment** | Docker (multi-stage), Gunicorn, Vercel (serverless) |
| **Documentation** | Docusaurus 3 |

---

## Features

### Core

- **Incident Reporting** — Multi-step guided form with a 17-category taxonomy for classifying psychological and tangible harms
- **Harm Classification** — 9 psychological, 7 tangible, and 1 "other" harm categories with severity ratings (1–4) and duration classification
- **Evidence Upload** — File attachment support via UploadThing cloud storage or local filesystem fallback (max 100 KB)
- **PDF Export** — Structured PDF reports with unique `PRG-XXXXXXXX` reference codes, per-incident identity redaction, and bulk export with table of contents

### Privacy & Security

- **Concealment Workflow** — Users can request identity concealment; admins review and grant or deny requests (granted = redacted in exports, denied = visible)
- **Session Timeout** — Automatic logout after 15 minutes of inactivity
- **CSRF Protection** — All forms protected with cross-site request forgery tokens
- **Secure Cookies** — `httponly`, `samesite`, configurable `Secure` flag
- **Argon2 Hashing** — Industry-standard password hashing with automatic algorithm upgrade
- **Audit Logging** — SHA-256 IP hashing, event tracking for all system actions (login, report, export, concealment)
- **Input Sanitization** — XSS prevention on all user-supplied content

### User Experience

- **Dark / Light Mode** — Full theme toggle with system-preference detection
- **Mobile Responsive** — Optimized for smartphones and tablets
- **Autosave** — Local storage draft preservation with explicit user consent
- **Distress Keyword Detection** — Flags reports containing indicators of acute distress
- **Low-Literacy Navigation** — Clear language, minimal jargon, contextual help text

### Admin

- **Admin Dashboard** — Overview of reported incidents, harm patterns, severity distribution
- **7-Filter Search** — Filter by status, concealment state, classification, platform, severity, and date range
- **Concealment Management** — Grant, deny, or revoke concealment requests directly from the list view or detail page
- **Support Resource Library** — 27 curated Nigerian organizations with contact info, incident-type matching, and harm-based recommendations

---

## Quick Start

### Prerequisites

| Requirement | Linux | macOS | Windows |
|------------|-------|-------|---------|
| Python 3.10+ | `sudo apt install python3 python3-pip python3-venv` | `brew install python@3.12` | [python.org/downloads](https://python.org/downloads) |
| PostgreSQL 14+ | `sudo apt install postgresql postgresql-contrib` | `brew install postgresql && brew services start postgresql` | [postgresql.org/download](https://postgresql.org/download) |
| Git | `sudo apt install git` | `brew install git` | [git-scm.com](https://git-scm.com) |

> **Windows users:** Run all commands inside **Git Bash**, **WSL**, or **MSYS2**. The `.sh` script and Django management commands require a POSIX-compatible shell.

### One-Shot Setup (Recommended)

The `setup.sh` script detects your environment, installs all dependencies, creates a virtual environment, applies migrations, and starts the server:

```bash
git clone https://github.com/trinnode/PrivGuard.git
cd PrivGuard
bash setup.sh          # interactive mode
bash setup.sh --yes    # accept all defaults (non-interactive)
```

The script handles:
- Auto-detection of Linux distribution family (Debian/Ubuntu/Kali, Fedora/RHEL, Arch, openSUSE), macOS, or Windows
- Version-pinned package names on Debian (`python3.11-venv`, `python3.12-venv`, etc.)
- `ensurepip` unavailable → `--without-pip` → `get-pip.py` → `virtualenv` fallback chain
- Binary wheel failures → automatic installation of C build headers → source compilation
- POSIX `bin/` vs Windows `Scripts/` venv layout detection

### Manual Setup

#### Linux (Debian / Ubuntu / Kali)

```bash
# Install Python and venv (version-pinned for your Python)
sudo apt update
sudo apt install python3.12 python3.12-venv python3.12-dev python3-pip

# Install PostgreSQL
sudo apt install postgresql postgresql-contrib
sudo systemctl enable --now postgresql

# Create database
sudo -u postgres psql -c "CREATE USER ragnar_user WITH PASSWORD 'ragnar_pass';"
sudo -u postgres psql -c "CREATE DATABASE ragnar_db OWNER ragnar_user;"

# Clone and set up
git clone https://github.com/trinnode/PrivGuard.git
cd PrivGuard
python3.12 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your database credentials

# Run migrations
python manage.py migrate

# Seed support resources
python manage.py seed_resources

# Create admin account
python manage.py createsuperuser

# Start server
python manage.py runserver
```

#### Linux (Fedora / RHEL / CentOS)

```bash
# Install Python and venv
sudo dnf install python3.12 python3.12-virtualenv python3.12-devel

# Install PostgreSQL
sudo dnf install postgresql-server
sudo postgresql-setup --initdb
sudo systemctl enable --now postgresql

# Create database
sudo -u postgres psql -c "CREATE USER ragnar_user WITH PASSWORD 'ragnar_pass';"
sudo -u postgres psql -c "CREATE DATABASE ragnar_db OWNER ragnar_user;"

# Clone and set up
git clone https://github.com/trinnode/PrivGuard.git
cd PrivGuard
python3.12 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py seed_resources
python manage.py createsuperuser
python manage.py runserver
```

#### Linux (Arch / Manjaro)

```bash
# Install Python and PostgreSQL
sudo pacman -S python python-pip postgresql

# Initialise PostgreSQL
sudo -u postgres initdb -D /var/lib/postgres/data
sudo systemctl enable --now postgresql

# Create database
sudo -u postgres psql -c "CREATE USER ragnar_user WITH PASSWORD 'ragnar_pass';"
sudo -u postgres psql -c "CREATE DATABASE ragnar_db OWNER ragnar_user;"

# Clone and set up
git clone https://github.com/trinnode/PrivGuard.git
cd PrivGuard
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py seed_resources
python manage.py createsuperuser
python manage.py runserver
```

#### macOS

```bash
# Install Python and PostgreSQL via Homebrew
brew install python@3.12 postgresql
brew services start postgresql

# Create database
createdb ragnar_db
psql ragnar_db -c "CREATE USER ragnar_user WITH PASSWORD 'ragnar_pass';"
psql ragnar_db -c "GRANT ALL PRIVILEGES ON DATABASE ragnar_db TO ragnar_user;"

# Clone and set up
git clone https://github.com/trinnode/PrivGuard.git
cd PrivGuard
python3.12 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py seed_resources
python manage.py createsuperuser
python manage.py runserver
```

#### Windows (Git Bash / WSL)

```bash
# Ensure Python 3.10+ is installed and in PATH
python --version   # should print 3.10+

# Clone and set up
git clone https://github.com/trinnode/PrivGuard.git
cd PrivGuard
python -m venv .venv
source .venv/Scripts/activate   # Note: Windows uses Scripts/, not bin/
pip install --upgrade pip
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env — use DATABASE_URL or DB_* variables pointing to your PostgreSQL instance

# Run migrations
python manage.py migrate

# Seed and start
python manage.py seed_resources
python manage.py createsuperuser
python manage.py runserver
```

### Docker Deployment

```bash
# Build and start all services (PostgreSQL + Django)
docker compose up -d --build

# Apply migrations inside the container
docker compose exec web python manage.py migrate --noinput

# Seed resources
docker compose exec web python manage.py seed_resources

# Create admin
docker compose exec web python manage.py createsuperuser

# View logs
docker compose logs -f web

# Stop
docker compose down
```

---

## Environment Variables

All variables are set in the `.env` file at the project root.

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DJANGO_SECRET_KEY` | Django cryptographic secret key | Auto-generated in development | **Production** |
| `DJANGO_DEBUG` | Enable/disable debug mode | `True` | No |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated allowed hostnames | `localhost,127.0.0.1` | **Production** |
| `DJANGO_DEV_PORT` | Development server port | `8000` | No |
| `DB_NAME` | PostgreSQL database name | `ragnar_db` | Local dev |
| `DB_USER` | PostgreSQL username | `ragnar_user` | Local dev |
| `DB_PASSWORD` | PostgreSQL password | `ragnar_pass` | Local dev |
| `DB_HOST` | PostgreSQL host | `localhost` | Local dev |
| `DB_PORT` | PostgreSQL port | `5432` | Local dev |
| `DATABASE_URL` | Full PostgreSQL connection string (overrides DB_*) | — | Vercel / Neon |
| `UPLOADTHING_TOKEN` | UploadThing API token | — | Optional |
| `UPLOADTHING_SECRET` | UploadThing secret key | — | Optional |
| `UPLOADTHING_CDN_URL` | UploadThing CDN base URL | `https://utfs.io/f` | Optional |
| `EMAIL_HOST` | SMTP server host | `smtp.gmail.com` | Optional |
| `EMAIL_PORT` | SMTP server port | `587` | Optional |
| `EMAIL_HOST_USER` | SMTP username | — | Optional |
| `EMAIL_HOST_PASSWORD` | SMTP password / app password | — | Optional |
| `EMAIL_USE_TLS` | Enable TLS for email | `True` | Optional |
| `SESSION_COOKIE_SECURE` | Require HTTPS for session cookies | `False` | **Production** |
| `CSRF_COOKIE_SECURE` | Require HTTPS for CSRF cookies | `False` | **Production** |
| `SECURE_SSL_REDIRECT` | Redirect HTTP to HTTPS | `False` | **Production** |

> **Production tip:** Set `DJANGO_DEBUG=False`, `SESSION_COOKIE_SECURE=True`, `CSRF_COOKIE_SECURE=True`, `SECURE_SSL_REDIRECT=True`, and use a `DATABASE_URL` pointing to a managed PostgreSQL instance (e.g., Neon, Railway, Supabase).

---

## Project Structure

```
PrivGuard/
├── accounts/                    # Authentication, registration, profile
│   ├── models.py                # Custom User model (email auth, roles, consent)
│   ├── views.py                 # Login, register, logout, profile, password reset
│   ├── forms.py                 # Registration and profile forms
│   ├── decorators.py            # Role-based access control
│   └── middleware.py             # Session timeout enforcement
│
├── incidents/                   # Core incident reporting system
│   ├── models.py                # Incident, Harm, AuditLog models
│   ├── views.py                 # CRUD, admin dashboard, PDF export
│   ├── forms.py                 # Incident form with harm inline sets
│   ├── taxonomy.py              # 17-category harm taxonomy, platform/classification enums
│   ├── urls.py                  # Incident URL routing
│   ├── management/commands/
│   │   ├── populate_users_data.py   # Synthetic student data generator (254 students)
│   │   └── seed_resources.py        # 27 Nigerian support resources seeder
│   └── templatetags/
│       └── incident_extras.py   # Custom template filters
│
├── resources/                   # Support resource library
│   ├── models.py                # Resource model with incident-type & harm matching
│   ├── views.py                 # Resource listing, detail, recommendation
│   ├── management/commands/
│   └── seed_resources.py        # Resource seeder (called from populate or standalone)
│
├── reporting/                   # PDF export engine
│   ├── views.py                 # Single + bulk PDF generation
│   ├── pdf_generator.py         # ReportLab document assembly
│   └── text_fallback.py         # Plain-text fallback on PDF failure
│
├── dashboard/                   # User dashboard with statistics
│   ├── views.py                 # Dashboard stats, harm distribution, severity breakdown
│   └── templatetags/
│       └── dashboard_extras.py  # Custom template filters
│
├── ragnar/                      # Django project configuration
│   ├── settings.py              # All Django settings (security, DB, apps, etc.)
│   ├── urls.py                  # Root URL configuration
│   └── wsgi.py / asgi.py        # WSGI/ASGI entry points
│
├── templates/                   # All HTML templates (app-namespaced)
│   ├── base.html                # Base layout with dark mode, nav, footer
│   ├── accounts/                # Login, register, profile, password reset
│   ├── incidents/               # Incident CRUD, admin views, detail pages
│   ├── resources/               # Resource listing and detail
│   ├── reporting/               # PDF download page
│   ├── dashboard/               # User dashboard
│   └── 404.html                 # Custom error page
│
├── static/                      # Frontend assets
│   ├── css/main.css             # Full design system (dark/light, responsive)
│   ├── js/main.js               # Theme toggle, autosave, form helpers
│   ├── images/logo.svg          # Application logo
│   └── images/favicon.svg       # Browser tab icon
│
├── tests/                       # Test suite (7 files, 60+ test cases)
│   ├── test_models.py           # Model integrity and constraints
│   ├── test_views.py            # Authentication flow and view rendering
│   ├── test_concealment.py      # Concealment lifecycle (request → grant → redact)
│   ├── test_comprehensive.py    # CRUD, security, session, upload, PDF, URL tests
│   ├── test_e2e.py              # End-to-end scenario tests
│   ├── test_runner.py           # Custom test runner configuration
│   └── conftest.py              # Shared pytest fixtures
│
├── docs/                        # Docusaurus documentation source
│   ├── docs/                    # Markdown documentation pages
│   ├── src/                     # Docusaurus React components
│   └── static/                  # Docusaurus static assets
│
├── setup.sh                     # One-shot cross-platform setup script
├── Dockerfile                   # Multi-stage production build
├── docker-compose.yml           # PostgreSQL + Django services
├── docker/entrypoint.sh         # Container startup script
├── vercel.json                  # Vercel serverless configuration
├── railway.json                 # Railway deployment configuration
├── requirements.txt             # Python dependencies (pinned)
├── .env.example                 # Environment variable template
└── manage.py                    # Django management entry point
```

---

## Harm Taxonomy

The taxonomy is adapted from academic research on digital privacy harms among university students.

### Psychological Harms (9 categories)

| # | Harm | Description |
|---|------|-------------|
| 1 | Anxiety | Persistent worry or nervousness about privacy violation |
| 2 | Humiliation | Embarrassment or shame from exposure of private information |
| 3 | Distress | Emotional suffering caused by the privacy incident |
| 4 | Fear for Safety | Concern about physical safety following a privacy breach |
| 5 | Loss of Trust | Diminished trust in people, platforms, or institutions |
| 6 | Self-blame | Internalized guilt or responsibility for the incident |
| 7 | Social Withdrawal | Avoidance of social interactions due to the incident |
| 8 | Academic Anxiety | Worry about academic consequences of the privacy violation |
| 9 | Trauma Symptoms | Post-incident psychological effects (flashbacks, hypervigilance) |

### Tangible Harms (7 categories)

| # | Harm | Description |
|---|------|-------------|
| 1 | Reputation Harm | Damage to personal or professional reputation |
| 2 | Academic Penalty | Negative academic consequences (suspension, grade impact) |
| 3 | Financial Loss | Monetary loss resulting from the privacy incident |
| 4 | Lost Opportunity | Missed opportunities due to the privacy violation |
| 5 | Social Ostracism | Exclusion from social groups or communities |
| 6 | Employment Impact | Adverse effects on job prospects or current employment |
| 7 | Physical Safety Threat | Risk of physical harm due to exposed personal information |

### Other (1 category)

| # | Harm | Description |
|---|------|-------------|
| 1 | Other | Harms that do not fit the above categories |

### Severity Levels

| Level | Label | Description |
|-------|-------|-------------|
| 1 | Minor | Minimal impact, easily recoverable |
| 2 | Moderate | Noticeable impact requiring some effort to address |
| 3 | Significant | Serious impact affecting daily life or wellbeing |
| 4 | Severe | Critical impact requiring immediate intervention |

### Incident Classifications

The system recognises 14 incident types across digital platforms, including: social media harassment, data breaches, doxxing, sextortion, non-consensual intimate image sharing, account compromise, phishing, identity theft, location tracking, spyware/surveillance, impersonation, blackmail, workplace monitoring, and academic surveillance.

### Platform Categories

Instagram, Twitter/X, TikTok, WhatsApp, Facebook, Snapchat, Telegram, Other Social Media, Non-Social Platform.

---

## Concealment Workflow

```
User submits incident report
         │
         ▼
   Status: DRAFT ──► Status: SUBMITTED
         │
         ▼
   User requests concealment (optional)
         │
         ▼
   Status: PENDING ──► Admin reviews
         │                │
         ▼                ▼
   ┌──────────────┐  ┌──────────────┐
   │   GRANTED    │  │    DENIED    │
   │ Redacted in  │  │  Visible in  │
   │ all exports  │  │ all exports  │
   └──────────────┘  └──────────────┘
         │
         ▼
   Admin can REVOKE at any time
```

**Key rules:**
- Granting/denying is **sticky** — admin decisions persist across re-seeds
- Concealed incidents show `[REDACTED]` in all PDF exports and admin views
- Users cannot see their own concealment status until it is granted
- The pending-count badge on the admin list is clickable and filters to pending requests

---

## Support Resources

PrivGuard includes a library of **27 real Nigerian organisations** providing support for privacy violations, including:

| Organisation | Focus Area |
|-------------|------------|
| Nigeria Data Protection Commission (NDPC) | Data protection regulation |
| NPF-National Cybercrime Centre (NCCC) | Cybercrime investigation |
| National Agency for the Prohibition of Trafficking in Persons (NAPTIP) | Human trafficking and exploitation |
| Men Against Violence (MANI) | Gender-based violence |
| Asido Foundation | Mental health support |
| She Writes Woman | Women's mental health |
| Digital Society Africa | Digital rights |
| Paradigm Initiative | Digital rights and inclusion |
| Enough is Enough Nigeria | Civic engagement |

Resources are matched to incidents based on **incident classification** and **harm categories**, providing context-appropriate recommendations on every incident detail page.

---

## Security

| Feature | Implementation |
|---------|---------------|
| Password hashing | Argon2id (with PBKDF2 fallback) |
| Session timeout | 15 minutes of inactivity |
| CSRF protection | Django CSRF middleware on all forms |
| Secure cookies | `httponly`, `samesite=strict`, configurable `Secure` |
| SSL redirect | Configurable via `SECURE_SSL_REDIRECT` |
| Input sanitisation | XSS prevention on all user content |
| Audit logging | SHA-256 IP hashing, 10 event types |
| File validation | MIME type checking, 100 KB size limit |
| SQL injection | Django ORM parameterised queries |
| Clickjacking | `X-Frame-Options: DENY` |

---

## Testing

```bash
# Run the full test suite
python manage.py test tests/

# Run a specific test file
python manage.py test tests/test_concealment.py

# Run with verbose output
python manage.py test tests/ -v 2
```

The test suite covers:
- Model integrity and constraint validation
- Full authentication flow (register, login, logout, password reset)
- Incident CRUD with multi-harm creation
- Admin dashboard and concealment workflow
- PDF export with identity redaction
- Session timeout enforcement
- CSRF and security header validation
- UploadThing integration
- Template rendering and URL resolution

---

## Deployment

### Vercel + Neon (Recommended)

```bash
# 1. Push to GitHub
git remote add origin https://github.com/trinnode/PrivGuard.git
git push -u origin main

# 2. Connect to Vercel
# - Import repository at vercel.com/new
# - Framework: Django
# - Build command: pip install -r requirements.txt && python manage.py collectstatic --noinput
# - Output directory: staticfiles

# 3. Set environment variables on Vercel
DATABASE_URL=postgresql://user:pass@ep-xxx.region.aws.neon.tech/ragnar_db
DJANGO_SECRET_KEY=<generate-a-strong-key>
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=your-app.vercel.app
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_SSL_REDIRECT=True

# 4. Create a Neon database at neon.tech
# 5. Apply migrations and seed data
vercel env pull .env.local
python manage.py migrate
python manage.py seed_resources
python manage.py populate_users_data --fresh  # optional: demo data
```

### Docker (Production)

```bash
# Build and start
docker compose up -d --build

# Apply migrations
docker compose exec web python manage.py migrate --noinput

# Collect static files
docker compose exec web python manage.py collectstatic --noinput

# View logs
docker compose logs -f web

# Stop
docker compose down
```

---

## API Reference

> **Note:** The current implementation uses Django template rendering. REST API endpoints are reserved for future expansion at `/api/v1/`.

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

This project is developed for academic research purposes as part of a study on digital privacy violations among Nigerian university students. All synthetic data used in demonstrations is randomly generated and does not represent real individuals.

---

<p align="center">
  Built with care for privacy, security, and student wellbeing.
</p>
