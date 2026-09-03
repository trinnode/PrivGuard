---
sidebar_position: 2
title: Configuration
---

# Configuration

PrivGuard is configured through environment variables in a `.env` file at the project root.

## Environment Variables

### Django Core

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DJANGO_SECRET_KEY` | Cryptographic secret key for sessions, CSRF tokens, and signatures | Auto-generated in dev | **Production** |
| `DJANGO_DEBUG` | Enable/disable debug mode | `True` | No |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated list of allowed hostnames | `localhost,127.0.0.1` | **Production** |
| `DJANGO_DEV_PORT` | Development server port | `8000` | No |

### Database

#### Option A: Individual Variables (Local Development)

| Variable | Description | Default |
|----------|-------------|---------|
| `DB_NAME` | PostgreSQL database name | `ragnar_db` |
| `DB_USER` | PostgreSQL username | `ragnar_user` |
| `DB_PASSWORD` | PostgreSQL password | `ragnar_pass` |
| `DB_HOST` | PostgreSQL host | `localhost` |
| `DB_PORT` | PostgreSQL port | `5432` |

#### Option B: Connection URL (Vercel / Neon / Managed Services)

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | Full PostgreSQL connection string, e.g. `postgresql://user:pass@host:5432/dbname` |

When `DATABASE_URL` is set, it takes precedence over individual `DB_*` variables.

### File Upload

| Variable | Description | Default |
|----------|-------------|---------|
| `UPLOADTHING_TOKEN` | UploadThing API token | — |
| `UPLOADTHING_SECRET` | UploadThing secret key | — |
| `UPLOADTHING_CDN_URL` | UploadThing CDN base URL | `https://utfs.io/f` |

If no UploadThing token is configured, files are stored locally in `media/evidence/`.

### Email (Optional)

| Variable | Description | Default |
|----------|-------------|---------|
| `EMAIL_HOST` | SMTP server hostname | `smtp.gmail.com` |
| `EMAIL_PORT` | SMTP server port | `587` |
| `EMAIL_HOST_USER` | SMTP username | — |
| `EMAIL_HOST_PASSWORD` | SMTP password / app password | — |
| `EMAIL_USE_TLS` | Enable TLS encryption | `True` |

### Security (Production)

| Variable | Description | Default |
|----------|-------------|---------|
| `SESSION_COOKIE_SECURE` | Require HTTPS for session cookies | `False` |
| `CSRF_COOKIE_SECURE` | Require HTTPS for CSRF cookies | `False` |
| `SECURE_SSL_REDIRECT` | Redirect all HTTP requests to HTTPS | `False` |

:::tip Production Checklist
Set these before deploying to production:
```bash
DJANGO_DEBUG=False
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_SSL_REDIRECT=True
DJANGO_ALLOWED_HOSTS=your-domain.com
DJANGO_SECRET_KEY=<generate-a-strong-64-char-key>
DATABASE_URL=postgresql://user:pass@host:5432/dbname
```
:::

---

## Generating a Secret Key

```bash
# Option 1: Python
python -c "import secrets; print(secrets.token_urlsafe(48))"

# Option 2: Django
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## Database Setup

### Creating the Database

```bash
# PostgreSQL CLI
sudo -u postgres psql -c "CREATE USER ragnar_user WITH PASSWORD 'ragnar_pass';"
sudo -u postgres psql -c "CREATE DATABASE ragnar_db OWNER ragnar_user;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE ragnar_db TO ragnar_user;"
```

### Running Migrations

```bash
python manage.py makemigrations accounts incidents resources
python manage.py migrate
```

### Seeding Data

```bash
# Seed 27 support resources
python manage.py seed_resources

# Seed demo data (254 students + incidents) — skip on live databases
python manage.py populate_users_data --fresh
```

---

## Vercel Configuration

For Vercel deployment, set all environment variables through the Vercel dashboard:

1. Go to your project → Settings → Environment Variables
2. Add each variable for the `Production` environment
3. Set `DATABASE_URL` to your Neon / managed PostgreSQL connection string
4. Ensure `DJANGO_DEBUG=False` and all cookie security flags are `True`

The `vercel.json` is already configured with the correct build commands and function timeout.

---

## Docker Configuration

Docker Compose reads `.env` automatically:

```bash
# The docker-compose.yml uses these variables:
# DB_NAME, DB_USER, DB_PASSWORD → PostgreSQL container
# DJANGO_SECRET_KEY, DJANGO_DEBUG → Django container
# DATABASE_URL → Optional override

docker compose up -d --build
docker compose exec web python manage.py migrate --noinput
```
