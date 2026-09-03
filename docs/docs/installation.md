---
sidebar_position: 1
title: Installation
---

# Installation

PrivGuard runs on **Linux**, **macOS**, and **Windows** (via Git Bash / WSL). This guide covers every installation method.

## Prerequisites

| Requirement | Minimum Version | Purpose |
|------------|----------------|---------|
| Python | 3.10+ | Backend runtime |
| PostgreSQL | 14+ | Database |
| Git | Any | Source control |
| Node.js | 18+ | Documentation site (optional) |

## One-Shot Setup (Recommended)

The `setup.sh` script handles everything automatically:

```bash
git clone https://github.com/trinnode/PrivGuard.git
cd PrivGuard
bash setup.sh          # interactive, prompts at each decision
bash setup.sh --yes    # non-interactive, accepts all defaults
```

### What the script does

1. **Detects your environment**, Linux (Debian/Fedora/Arch/openSUSE), macOS, or Windows
2. **Installs system packages**, Python, pip, venv, PostgreSQL, git (version-pinned on Debian)
3. **Creates an isolated virtual environment** at `.venv/`
4. **Installs the latest Python dependencies**, falls back to source compilation if binary wheels are unavailable
5. **Prepares `.env`**, copies from `.env.example` or generates a minimal config
6. **Applies database migrations**, creates all tables
7. **Seeds support resources**, 27 Nigerian organisations
8. **Starts the development server**, `http://127.0.0.1:8000`

### Edge cases handled

| Scenario | How it's handled |
|----------|-----------------|
| `ensurepip` unavailable (Kali/Debian) | Installs version-pinned `python3.XX-venv`, falls back to `--without-pip` + `get-pip.py`, then `virtualenv` |
| Binary wheel unavailable | Installs C build headers (`libpq-dev`, `python3-dev`, `build-essential`), retries source compilation |
| Windows `Scripts/` vs POSIX `bin/` | Auto-detects venv layout and uses the correct path |
| Old Python (< 3.10) | Offers automatic upgrade via deadsnakes PPA (Ubuntu), dnf (Fedora), Homebrew (macOS) |
| No package manager found | Prints the exact manual command to run |

---

## Manual Installation

### Linux, Debian / Ubuntu / Kali

```bash
# Install Python and version-pinned venv
sudo apt update
sudo apt install python3.12 python3.12-venv python3.12-dev python3-pip

# Install PostgreSQL
sudo apt install postgresql postgresql-contrib
sudo systemctl enable --now postgresql

# Create database and user
sudo -u postgres psql -c "CREATE USER ragnar_user WITH PASSWORD 'ragnar_pass';"
sudo -u postgres psql -c "CREATE DATABASE ragnar_db OWNER ragnar_user;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE ragnar_db TO ragnar_user;"

# Clone and set up
git clone https://github.com/trinnode/PrivGuard.git
cd PrivGuard
python3.12 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env, set DB_HOST, DB_NAME, DB_USER, DB_PASSWORD

# Apply migrations
python manage.py migrate

# Seed support resources
python manage.py seed_resources

# Create admin account
python manage.py createsuperuser

# Start server
python manage.py runserver
```

:::tip
On Kali Linux, use `python3.11-venv` or `python3.12-venv` depending on your installed Python version. The generic `python3-venv` package may not exist.
:::

### Linux, Fedora / RHEL / CentOS

```bash
# Install Python
sudo dnf install python3.12 python3.12-devel python3.12-virtualenv

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

### Linux, Arch / Manjaro

```bash
# Install Python and PostgreSQL
sudo pacman -S python python-pip postgresql

# Initialise PostgreSQL data directory
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

### macOS

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

### Windows (Git Bash / WSL)

```bash
# Ensure Python 3.10+ is installed and in PATH
python --version

# Clone
git clone https://github.com/trinnode/PrivGuard.git
cd PrivGuard

# Create venv, Windows uses Scripts/ not bin/
python -m venv .venv
source .venv/Scripts/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env, set DATABASE_URL or DB_* variables

# Apply migrations and seed
python manage.py migrate
python manage.py seed_resources
python manage.py createsuperuser
python manage.py runserver
```

:::caution
Windows users **must** use Git Bash, WSL, or MSYS2. The native Windows `cmd.exe` and PowerShell do not support `.sh` scripts or POSIX path conventions.
:::

---

## Verifying the Installation

After starting the server, open `http://127.0.0.1:8000` in your browser. You should see:

1. **Dashboard**, with statistics cards (all zero initially)
2. **Login**, click "Login" and use your superuser credentials
3. **Admin Panel**, at `/admin/` (if you are a superuser)
4. **Resources**, at `/resources/` (if you ran `seed_resources`)

### Default Admin Account

If you ran `populate_users_data --fresh` during setup:

| Field | Value |
|-------|-------|
| Email | `admin@futminna.edu.ng` |
| Password | `admin123` |
| Role | Superuser + Staff |

:::warning
Change the default admin password immediately in production environments.
:::
