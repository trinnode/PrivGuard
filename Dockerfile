FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --user --no-compile -r requirements.txt


FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH=/root/.local/bin:$PATH

WORKDIR /app

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    libpq-dev && \
    rm -rf /var/lib/apt/lists/*

COPY --from=builder /root/.local /root/.local

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "ragnar.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120"]
