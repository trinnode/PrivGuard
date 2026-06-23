# RAGNER - Privacy Incident Reporting System

A web-based privacy incident reporting system for Nigerian university students. Users can document digital privacy violations, classify associated psychological and tangible harms using an adapted academic taxonomy, access context-appropriate guidance, and export structured reports.

## Tech Stack

- **Backend:** Python / Django 5.0
- **Database:** PostgreSQL
- **Frontend:** HTML5, CSS3 (custom design system), vanilla JavaScript
- **PDF Export:** ReportLab
- **Authentication:** Django session management with Argon2 password hashing
- **Deployment:** Docker, Gunicorn, WhiteNoise

## Features

- **Incident Reporting:** Guided form with taxonomy-based harm classification (psychological and tangible harms)
- **Dashboard:** Overview of reported incidents, harm patterns, and severity distribution
- **Resource Library:** Categorized support resources for legal, mental health, and digital safety guidance
- **PDF Export:** Structured PDF reports with unique reference codes, text fallback on failure
- **Security:** NDPA-compliant, session timeout (15 min inactivity), CSRF protection, secure cookies, input sanitization
- **Autosave:** Local storage draft preservation with user consent
- **Edge Case Handling:** Distress keyword detection, network interruption recovery, low-literacy navigation support
- **Audit Logging:** SHA-256 IP hashing, event tracking for all system actions

## Quick Start

### Prerequisites

- Python 3.12+
- PostgreSQL 16+
- Docker (optional)

### Local Development

```bash
# Clone the repository
git clone <repo-url>
cd ragnar

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
# Edit .env with your database credentials

# Run migrations
python manage.py makemigrations accounts incidents resources
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### Docker Deployment

```bash
docker-compose up -d
```

### Environment Variables

| Variable | Description | Default |
|---|---|---|
| `DJANGO_SECRET_KEY` | Django secret key | (required in production) |
| `DJANGO_DEBUG` | Debug mode | `False` |
| `DB_NAME` | PostgreSQL database name | `ragnar_db` |
| `DB_USER` | Database user | `ragnar_user` |
| `DB_PASSWORD` | Database password | `ragnar_pass` |
| `DB_HOST` | Database host | `localhost` |
| `DB_PORT` | Database port | `5432` |

## Project Structure

```
ragnar/
├── accounts/          # Authentication, registration, profile management
├── dashboard/         # User dashboard with statistics and harm overview
├── incidents/         # Incident reporting, taxonomy, harm classification
├── reporting/         # PDF export and text fallback generation
├── resources/         # Support resource library
├── ragnar/            # Django project configuration
├── templates/         # All HTML templates (app-namespaced)
├── static/            # CSS, JS, SVG assets
├── tests/             # Unit and integration tests
├── docker/            # Deployment scripts
└── docker-compose.yml # Production-ready Docker setup
```

## To rebuild and deploy: 

``` docker compose down && docker compose up -d --build && docker compose exec web python manage.py migrate --noinput ```

## Harm Taxonomy

The taxonomy is adapted from academic research on digital privacy harms and classifies violations into:

- **Psychological Harms:** Anxiety, humiliation, distress, fear for safety, loss of trust, self-blame, social withdrawal, academic anxiety, trauma symptoms
- **Tangible Harms:** Reputation harm, academic penalty, financial loss, lost opportunity, social ostracism, employment impact, physical safety threat

Each harm is rated by severity (1-4) and duration classification.

## API Reference

Future API expansion endpoints are reserved at `/api/v1/`. Current implementation relies solely on Django template rendering.

## Testing

```bash
python manage.py test tests/
```

## License

This project is developed for academic research purposes as part of a study on digital privacy violations among Nigerian university students.
