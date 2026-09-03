---
sidebar_position: 3
title: Manual Deployment
---

# Manual Deployment

This guide covers deploying PrivGuard manually on a Linux server without Docker.

## Prerequisites

- Ubuntu 22.04+ / Debian 12+ / Fedora 38+ / RHEL 9+
- Python 3.10+
- PostgreSQL 14+
- Nginx (for reverse proxy)
- Git

## Step 1: Install System Packages

### Ubuntu / Debian

```bash
sudo apt update
sudo apt install -y python3.12 python3.12-venv python3.12-dev \
    postgresql postgresql-contrib nginx git gcc libpq-dev
```

### Fedora / RHEL

```bash
sudo dnf install -y python3.12 python3.12-devel \
    postgresql-server nginx git gcc gcc-c++ libpq-devel
sudo postgresql-setup --initdb
sudo systemctl enable --now postgresql
```

## Step 2: Create Database

```bash
sudo -u postgres psql -c "CREATE USER privguard WITH PASSWORD 'strong-password-here';"
sudo -u postgres psql -c "CREATE DATABASE privguard_db OWNER privguard;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE privguard_db TO privguard;"
```

## Step 3: Deploy Application

```bash
# Create deployment directory
sudo mkdir -p /var/www/privguard
sudo chown $USER:$USER /var/www/privguard

# Clone repository
git clone https://github.com/trinnode/PrivGuard.git /var/www/privguard
cd /var/www/privguard

# Create virtual environment
python3.12 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Configure environment
cp .env.example .env
```

Edit `.env`:

```bash
DJANGO_SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(48))")
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=your-domain.com,your-server-ip
DB_NAME=privguard_db
DB_USER=privguard
DB_PASSWORD=strong-password-here
DB_HOST=localhost
DB_PORT=5432
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_SSL_REDIRECT=True
```

## Step 4: Apply Migrations

```bash
python manage.py migrate --noinput
python manage.py seed_resources
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

## Step 5: Configure Gunicorn

Create `/var/www/privguard/gunicorn.conf.py`:

```python
bind = "127.0.0.1:8000"
workers = 3
timeout = 120
accesslog = "/var/log/privguard/access.log"
errorlog = "/var/log/privguard/error.log"
```

Create a systemd service:

```bash
sudo tee /etc/systemd/system/privguard.service << 'EOF'
[Unit]
Description=PrivGuard Gunicorn
After=network.target postgresql.service

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/privguard
ExecStart=/var/www/privguard/.venv/bin/gunicorn ragnar.wsgi:application -c gunicorn.conf.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable --now privguard
```

## Step 6: Configure Nginx

```bash
sudo tee /etc/nginx/sites-available/privguard << 'EOF'
server {
    listen 80;
    server_name your-domain.com your-server-ip;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /var/www/privguard;
    }
    location /media/ {
        root /var/www/privguard;
    }
    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
EOF

sudo ln -s /etc/nginx/sites-available/privguard /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

## Step 7: SSL with Certbot (Optional)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

## Updating

```bash
cd /var/www/privguard
source .venv/bin/activate
git pull origin main
pip install -r requirements.txt
python manage.py migrate --noinput
python manage.py collectstatic --noinput
sudo systemctl restart privguard
```

## Monitoring

```bash
# Check service status
sudo systemctl status privguard

# View logs
sudo journalctl -u privguard -f
sudo tail -f /var/log/privguard/access.log
```
