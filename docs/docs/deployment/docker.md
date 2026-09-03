---
sidebar_position: 2
title: Docker
---

# Deploy with Docker

PrivGuard includes a multi-stage `Dockerfile` and `docker-compose.yml` for containerised deployment.

## Quick Start

```bash
# Build and start all services
docker compose up -d --build

# Apply migrations
docker compose exec web python manage.py migrate --noinput

# Seed support resources
docker compose exec web python manage.py seed_resources

# Create admin account
docker compose exec web python manage.py createsuperuser

# View logs
docker compose logs -f web

# Stop services
docker compose down
```

## Docker Compose Services

| Service | Image | Purpose |
|---------|-------|---------|
| `web` | Built from `Dockerfile` | Django application + Gunicorn |
| `db` | `postgres:16` | PostgreSQL database |

## Dockerfile (Multi-Stage)

```dockerfile
# Stage 1: Build
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . .
RUN python manage.py collectstatic --noinput
CMD ["gunicorn", "ragnar.wsgi:application", "--bind", "0.0.0.0:8000"]
```

## Environment Variables

Create a `.env` file in the project root:

```bash
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=ragnar_db
DB_USER=ragnar_user
DB_PASSWORD=ragnar_pass
DB_HOST=db
DB_PORT=5432
```

:::note
In Docker Compose, the database host is `db` (the service name), not `localhost`.
:::

## Data Persistence

The PostgreSQL data is persisted in a Docker volume:

```bash
# Volume name is derived from the project directory
docker volume ls | grep postgres
```

To back up the database:

```bash
docker compose exec db pg_dump -U ragnar_user ragnar_db > backup.sql
```

To restore:

```bash
cat backup.sql | docker compose exec -T db psql -U ragnar_user ragnar_db
```

## Production Considerations

| Setting | Development | Production |
|---------|-------------|------------|
| `DEBUG` | `True` | `False` |
| `DB_HOST` | `localhost` | `db` (Compose) or managed service |
| `ALLOWED_HOSTS` | `localhost` | Your domain |
| SSL | No | Behind reverse proxy (Nginx/Caddy) |

### Adding Nginx (Optional)

For production, add an Nginx reverse proxy:

```yaml
# Add to docker-compose.yml
services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./staticfiles:/app/staticfiles
    depends_on:
      - web
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `db` service won't start | Check port 5432 is not in use: `lsof -i :5432` |
| `web` can't connect to `db` | Ensure `DB_HOST=db` in `.env` |
| Static files 404 | Run `docker compose exec web python manage.py collectstatic --noinput` |
| Permission denied | Run with `sudo` or add your user to the `docker` group |
