---
sidebar_position: 1
title: Vercel + Neon
---

# Deploy to Vercel + Neon

This guide covers deploying PrivGuard to Vercel (serverless Django) with Neon (managed PostgreSQL).

## Prerequisites

- GitHub account with the PrivGuard repository
- Vercel account at [vercel.com](https://vercel.com)
- Neon account at [neon.tech](https://neon.tech)

## Step 1: Create a Neon Database

1. Sign up at [neon.tech](https://neon.tech)
2. Create a new project
3. Copy the connection string from the dashboard:
   ```
   postgresql://username:password@ep-xxx-yyy.region.aws.neon.tech/dbname?sslmode=require
   ```

## Step 2: Connect to Vercel

1. Go to [vercel.com/new](https://vercel.com/new)
2. Import the `trinnode/PrivGuard` repository
3. Configure:
   - **Framework Preset**: Django
   - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - **Output Directory**: `staticfiles`
   - **Install Command**: `pip install -r requirements.txt`

## Step 3: Set Environment Variables

In the Vercel dashboard → Settings → Environment Variables, add:

| Variable | Value |
|----------|-------|
| `DATABASE_URL` | Your Neon connection string |
| `DJANGO_SECRET_KEY` | Generate: `python -c "import secrets; print(secrets.token_urlsafe(48))"` |
| `DJANGO_DEBUG` | `False` |
| `DJANGO_ALLOWED_HOSTS` | `your-app.vercel.app` |
| `SESSION_COOKIE_SECURE` | `True` |
| `CSRF_COOKIE_SECURE` | `True` |
| `SECURE_SSL_REDIRECT` | `True` |

:::tip
Set all variables for the **Production** environment, not just Preview or Development.
:::

## Step 4: Apply Migrations

After the first deployment, run migrations against Neon:

```bash
# Option 1: Pull env locally and run
vercel env pull .env.local
source .venv/bin/activate
python manage.py migrate
python manage.py seed_resources

# Option 2: Run via Vercel CLI
vercel run python manage.py migrate
```

## Step 5: Verify

1. Visit `https://your-app.vercel.app`
2. You should see the PrivGuard dashboard
3. Log in with your admin credentials
4. Check that `/admin/` works
5. Verify that `/resources/` shows 27 organisations

## Updating

Every push to `main` triggers automatic deployment:

```bash
git push origin main
# Vercel automatically rebuilds and deploys
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `DJANGO_ALLOWED_HOSTS error` | Add your Vercel domain to `DJANGO_ALLOWED_HOSTS` |
| `Database connection refused` | Verify `DATABASE_URL` is correct and Neon project is active |
| `Static files not loading` | Ensure `python manage.py collectstatic --noinput` runs in build command |
| `CSRF verification failed` | Set `CSRF_COOKIE_SECURE=True` and `SESSION_COOKIE_SECURE=True` |
| `502 Bad Gateway` | Check `vercel.json` function timeout; increase `maxDuration` if needed |
