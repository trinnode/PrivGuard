#!/usr/bin/env bash
# =============================================================================
# PrivGuard One-Shot Setup Script (version-aware)
#
# Handles environment & version edge cases:
#   * Linux families: Debian/Ubuntu (apt), Fedora/RHEL (dnf/yum),
#     Arch (pacman), SUSE (zypper) - correct package names for each
#   * macOS via Homebrew
#   * Windows ONLY through a POSIX shell (Git Bash / MSYS2 / WSL);
#     venvs there use Scripts/ instead of bin/
#   * pip feature detection (--break-system-packages only on pip >= 23)
#   * Python >= 3.10 required (Django 5+ baseline); offers upgrade paths
#   * Falls back to compiling native wheels (psycopg2 / Pillow) by first
#     installing the required C headers & compilers if a binary wheel
#     is unavailable for your platform/Python combo
#
# Usage:
#   bash setup.sh          # interactive
#   bash setup.sh --yes    # skip confirmation prompts
# =============================================================================

set -euo pipefail

# ------------------------------------------------------------------ colours --
if [[ -t 1 ]]; then
    BOLD="\033[1m"; GREEN="\033[32m"; YELLOW="\033[33m"; RED="\033[31m"
    CYAN="\033[36m"; RESET="\033[0m"
else
    BOLD=""; GREEN=""; YELLOW=""; RED=""; CYAN=""; RESET=""
fi

step() { printf "\n${BOLD}${CYAN}==> %s${RESET}\n" "$*"; }
info() { printf "${CYAN}  - %s${RESET}\n" "$*"; }
ok()   { printf "${GREEN}  ✔ %s${RESET}\n" "$*"; }
warn() { printf "${YELLOW}  ! %s${RESET}\n" "$*"; }
fail() { printf "${RED}  ✘ ERROR: %s${RESET}${RESET}\n" "$*" >&2; exit 1; }

ASSUME_YES=false
[[ "${1:-}" == "--yes" ]] && ASSUME_YES=true

confirm() {
    $ASSUME_YES && return 0
    read -r -p "$1 [y/N] " answer
    [[ "$answer" =~ ^[Yy]$ ]]
}

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

cat <<'BANNER'
=====================================================
   PrivGuard - Privacy Incident Reporting System
       One-Shot Environment Setup (v2)
=====================================================
BANNER

# ------------------------------------------------------- 1. environment -----
step "1/8 Detecting environment"

RAW_UNAME="$(uname -s)"
case "$RAW_UNAME" in
    Linux*)               AUTO_ENV="linux" ;;
    Darwin*)              AUTO_ENV="macos" ;;
    MINGW*|MSYS*|CYGWIN*) AUTO_ENV="windows" ;;
    *)                    AUTO_ENV="unknown" ;;
esac

OS_FAMILY=""
if [[ "$AUTO_ENV" == "linux" ]] && [[ -r /etc/os-release ]]; then
    # shellcheck disable=SC1091
    . /etc/os-release
    case "${ID:-}" in
        ubuntu|debian|linuxmint|pop|raspbian) OS_FAMILY="debian" ;;
        fedora|rhel|centos|rocky|almalinux|amzn|ol) OS_FAMILY="rhel" ;;
        arch|manjaro|endeavouros)                   OS_FAMILY="arch" ;;
        opensuse*|sles)                             OS_FAMILY="suse" ;;
        *)
            case "${ID_LIKE:-}" in
                *debian*) OS_FAMILY="debian" ;;
                *fedora*|*rhel*|*centos*) OS_FAMILY="rhel" ;;
                *arch*) OS_FAMILY="arch" ;;
                *suse*) OS_FAMILY="suse" ;;
                *)      OS_FAMILY="unknown" ;;
            esac
            ;;
    esac
elif [[ "$AUTO_ENV" == "macos" ]]; then
    OS_FAMILY="brew"
fi
[[ -n "$OS_FAMILY" ]] && info "Package family: ${BOLD}${OS_FAMILY:-unknown}${RESET}"

echo ""
echo "  Which environment is this?"
echo "    1) Linux"
echo "    2) Windows (Git Bash / MSYS2 / WSL only - .sh needs a POSIX shell)"
echo "    3) macOS"
read -r -p "  Enter choice [1/2/3] (Enter = auto-detect '$AUTO_ENV'): " ENV_CHOICE

case "$ENV_CHOICE" in
    1) ENV="linux" ;;
    2) ENV="windows" ;;
    3) ENV="macos" ;;
    "") ENV="$AUTO_ENV" ;;
    *) warn "Unknown choice - using auto-detection."; ENV="$AUTO_ENV" ;;
esac

case "$ENV" in
    linux)   ok "Environment: Linux ($OS_FAMILY)" ;;
    windows) ok "Environment: Windows (POSIX shell)" ;;
    macos)   ok "Environment: macOS" ;;
    *)       fail "Unrecognised environment '$ENV'. Use a bash-compatible shell." ;;
esac

# ------------------------------------------------ privilege + pkg manager ---
SUDO=""
if [[ "$(id -u)" -ne 0 ]] && command -v sudo >/dev/null 2>&1; then
    SUDO="sudo"
fi

detect_pkg_mgr() {
    for mgr in apt-get dnf yum pacman zypper brew; do
        command -v "$mgr" >/dev/null 2>&1 && { echo "$mgr"; return 0; }
    done
    return 1
}

PKG_MGR="$(detect_pkg_mgr || true)"

# Map a GENERIC name to the right one for this distro family/version.
map_pkg() {
    local generic="$1"
    case "$generic" in
        python3)
            case "$OS_FAMILY" in debian) echo "python3";; rhel) echo "python3";; arch) echo "python";; suse) echo "python3";; *) echo "python3";; esac ;;
        python3-pip)
            case "$OS_FAMILY" in debian) echo "python3-pip";; rhel) echo "python3-pip";; arch) echo "python-pip";; suse) echo "python3-pip";; *) echo "python3-pip";; esac ;;
        python3-venv)
            case "$OS_FAMILY" in debian) echo "python3-venv";; rhel) echo "python3";; arch) echo "python";; suse) echo "python3-venv";; *) echo "python3-venv";; esac ;;
        python3-dev)
            case "$OS_FAMILY" in
                debian) echo "python3-dev";;
                rhel)   echo "python3-devel";;
                arch)   # Arch ships headers inside 'python' itself
                        if pacman -Qi python >/dev/null 2>&1; then echo ""; else echo "python"; fi ;;
                suse)   echo "python3-devel";;
                *)      echo "python3-dev";;
            esac ;;
        postgresql)
            case "$OS_FAMILY" in
                debian) # Debian 12+/Ubuntu 22.04+: metapackage 'postgresql' exists everywhere recent
                        echo "postgresql" ;;
                rhel)   # RHEL9/Fedora name the server explicitly; fall back sensibly
                        if command -v dnf >/dev/null 2>&1 && dnf list available postgresql-server >/dev/null 2>&1; then
                            echo "postgresql-server"
                        else
                            echo "postgresql"
                        fi ;;
                arch)   echo "postgresql" ;;
                suse)   echo "postgresql-server" ;;
                *)      echo "postgresql" ;;
            esac ;;
        git) echo "git" ;;
        *)   echo "$generic" ;;
    esac
}

pkg_install() {
    local generic="$1" real
    real="$(map_pkg "$generic")"
    [[ -z "$real" ]] && { warn "'$generic' needs no separate package here."; return 0; }

    case "$OS_FAMILY" in
        debian)
            $SUDO apt-get update -y >/dev/null 2>&1 || true
            $SUDO DEBIAN_FRONTEND=noninteractive apt-get install -y "$real" \
                || fail "apt could not install '$real'. Install it manually and re-run."
            ;;
        rhel)
            $SUDO dnf install -y "$real" 2>/dev/null \
                || $SUDO yum install -y "$real" \
                || fail "dnf/yum could not install '$real'."
            ;;
        arch)
            $SUDO pacman -Sy --noconfirm --needed "$real" \
                || fail "pacman could not install '$real'."
            ;;
        suse)
            $SUDO zypper install -y "$real" \
                || fail "zypper could not install '$real'."
            ;;
        brew)
            brew install "$real" || fail "brew could not install '$real'."
            ;;
        *)
            fail "No supported package manager found. Install '$real' manually."
            ;;
    esac
}

# --------------------------------------------------- 2. python toolchain ----
step "2/8 Checking & installing Python toolchain"

py_major_minor() { "$1" -c 'import sys; print(f"{sys.version_info[0]}.{sys.version_info[1]}")'; }

PY_BIN=""
for candidate in python3 python; do
    if command -v "$candidate" >/dev/null 2>&1; then
        if "$candidate" -c 'import sys; sys.exit(0 if sys.version_info >= (3,10) else 1)' 2>/dev/null; then
            PY_BIN="$candidate"; break
        fi
    fi
done

if [[ -z "$PY_BIN" ]]; then
    warn "Python >= 3.10 not found."
    if confirm "Attempt automatic installation of a suitable Python?"; then
        case "$OS_FAMILY" in
            debian)
                # Ubuntu <=20.04 ships 3.8; deadsnakes provides modern interpreters.
                $SUDO apt-get update -y >/dev/null 2>&1 || true
                $SUDO DEBIAN_FRONTEND=noninteractive apt-get install -y software-properties-common || true
                $SUDO add-apt-repository -y ppa:deadsnakes/ppa || true
                $SUDO DEBIAN_FRONTEND=noninteractive apt-get install -y "python3.12" "python3.12-venv" "python3.12-distutils" \
                    || fail "Could not install python3.12. Install Python >= 3.10 manually."
                PY_BIN="$(command -v python3.12)"
                ;;
            rhel)
                pkg_install python3.12 || pkg_install python3.11 || pkg_install python3 \
                    || fail "Install Python >= 3.10 manually."
                PY_BIN="$(command -v python3.12 || command -v python3.11 || command -v python3)"
                ;;
            arch)  pkg_install python; PY_BIN="$(command -v python)" ;;
            suse)  pkg_install python312 || pkg_install python3; PY_BIN="$(command -v python3.12 || command -v python3)" ;;
            brew)  pkg_install python@3.12; PY_BIN="$(command -v python3.12 || command -v python3)" ;;
            *)     fail "Install Python >= 3.10 manually, then re-run this script." ;;
        esac
    else
        fail "Cannot continue without Python >= 3.10 (Django 5 requirement)."
    fi
fi
ok "Python $(py_major_minor "$PY_BIN") at $(command -v "$PY_BIN")"

# --- pip (feature-detect --break-system-packages; irrelevant inside venv,
#     but checked so any bare pip calls never crash on old pip versions) ---
if ! "$PY_BIN" -m pip --version >/dev/null 2>&1; then
    warn "pip missing - bootstrapping..."
    if "$PY_BIN" -m ensurepip --version >/dev/null 2>&1; then
        "$PY_BIN" -m ensurepip --upgrade || true
    fi
    if ! "$PY_BIN" -m pip --version >/dev/null 2>&1; then
        pkg_install python3-pip || fail "Could not provision pip automatically."
    fi
fi
ok "pip $($("$PY_BIN" -m pip --version 2>/dev/null | awk '{print $2}'))"

# --- venv module ---
if ! "$PY_BIN" -c "import venv" >/dev/null 2>&1; then
    warn "venv module missing (common on Debian/Ubuntu minimal installs)."
    pkg_install python3-venv || fail "venv still unavailable. Install 'python3-venv' manually."
fi
ok "venv module available"

# --- git (optional) ---
if command -v git >/dev/null 2>&1; then
    ok "git present: $(git --version)"
else
    if confirm "git not found. Install it?"; then
        pkg_install git
        ok "Installed $(git --version)"
    else
        warn "Skipping git - you won't be able to pull updates."
    fi
fi

# --- PostgreSQL ---
PG_PRESENT=false
if command -v psql >/dev/null 2>&1; then
    PG_PRESENT=true
    ok "PostgreSQL client: $(psql --version | awk '{print $3}')"
else
    if confirm "PostgreSQL not found. Install server + client now?"; then
        pkg_install postgresql
        case "$OS_FAMILY" in
            debian)
                $SUDO systemctl enable --now postgresql 2>/dev/null || $SUDO service postgresql start || true
                ;;
            rhel)
                if command -v postgresql-setup >/dev/null 2>&1; then
                    $SUDO postgresql-setup --initdb || true
                fi
                $SUDO systemctl enable --now postgresql || true
                ;;
            arch)
                if [[ ! -d /var/lib/postgres/data ]]; then
                    $SUDO -u postgres initdb -D /var/lib/postgres/data || true
                fi
                $SUDO systemctl enable --now postgresql || true
                ;;
            suse)
                $SUDO systemctl enable --now postgresql || true
                ;;
            brew)
                brew services start postgresql || true
                ;;
        esac
        PG_PRESENT=true
        ok "PostgreSQL service started"
    else
        warn "Skipped. Ensure DATABASE_URL or DB_* values in .env point somewhere reachable."
    fi
fi

# ------------------------------------------------- 3. virtual environment ---
step "3/8 Creating virtual environment"

VENV_DIR="$PROJECT_DIR/.venv"
if [[ -d "$VENV_DIR" ]]; then
    ok "Reusing existing virtualenv: $VENV_DIR"
else
    "$PY_BIN" -m venv "$VENV_DIR" || fail "venv creation failed."
    ok "Created $VENV_DIR"
fi

# Edge case: Windows venvs use Scripts/, POSIX use bin/.
if [[ -x "$VENV_DIR/bin/python" ]]; then
    VENV_PY="$VENV_DIR/bin/python"
    ACTIVATE_PATH="$VENV_DIR/bin/activate"
else
    VENV_PY="$VENV_DIR/Scripts/python.exe"
    [[ -x "$VENV_PY" ]] || VENV_PY="$VENV_DIR/Scripts/python"
    ACTIVATE_PATH="$VENV_DIR/Scripts/activate"
fi
[[ -x "$VENV_PY" ]] || fail "Virtualenv interpreter not found at either bin/ or Scripts/."

ok "Interpreter: $("$VENV_PY" --version) -> $VENV_PY"

pip_supports() {
    "$VENV_PY" -m pip install --help 2>/dev/null | grep -q -- "$1"
}

# --------------------------------------------- 4. python dependencies -------
step "4/8 Installing latest Python dependencies"

"$VENV_PY" -m pip install --upgrade --quiet pip setuptools wheel
echo ""

DEPS=(django psycopg2-binary gunicorn whitenoise python-decouple dj-database-url reportlab pillow argon2-cffi)

install_with_fallback() {
    local dep="$1"
    info "Installing latest: $dep"
    if "$VENV_PY" -m pip install --upgrade --quiet "$dep"; then
        return 0
    fi

    # Edge case: binary wheel unavailable for this Python/platform ->
    # install compiler toolchain + C headers, then retry (source build).
    warn "'$dep' failed - installing native build tools and retrying from source..."
    case "$OS_FAMILY" in
        debian) $SUDO DEBIAN_FRONTEND=noninteractive apt-get install -y build-essential python3-dev libpq-dev libjpeg-dev zlib1g-dev >/dev/null ;;
        rhel)   $SUDO dnf install -y gcc gcc-c++ python3-devel libpq-devel libjpeg-turbo-devel zlib-devel >/dev/null 2>&1 || $SUDO yum install -y gcc python3-devel libpq-devel libjpeg-devel zlib-devel >/dev/null ;;
        arch)   $SUDO pacman -Sy --noconfirm --needed base-devel libjpeg-turbo zlib postgresql-libs >/dev/null ;;
        suse)   $SUDO zypper install -y -t pattern devel_basis >/dev/null 2>&1; $SUDO zypper install -y gcc python3-devel libpq-devel libjpeg-devel zlib-devel >/dev/null ;;
        brew)   xcode-select --install 2>/dev/null || true; brew install libpq jpeg-turbo 2>/dev/null || true ;;
        windows) ;;
    esac

    "$VENV_PY" -m pip install --upgrade --quiet "$dep" \
        || fail "Still failing after build-tool installation. Install '$dep' manually."
}

for dep in "${DEPS[@]}"; do
    install_with_fallback "$dep"
done
echo ""
ok "Core dependency versions now installed:"
"$VENV_PY" -m pip show django psycopg2-binary reportlab pillow argon2-cffi gunicorn whitenoise python-decouple dj-database-url 2>/dev/null \
    | grep -E "^(Name|Version):" | paste - - | sed 's/^/    /'

# ------------------------------------------------------------ 5. env file ---
step "5/8 Preparing environment variables"

if [[ -f ".env" ]]; then
    ok ".env already exists - leaving untouched"
else
    if [[ -f ".env.example" ]]; then
        cp .env.example .env
        ok "Copied .env.example -> .env"
        warn "Set DJANGO_SECRET_KEY, DATABASE_URL / DB_* and UploadThing tokens before production."
        if confirm "Open .env for editing now?"; then
            "${EDITOR:-vi}" .env || true
        fi
    else
        warn ".env.example not found - writing a minimal .env"
        SECRET="$("$VENV_PY" -c 'import secrets; print(secrets.token_urlsafe(48))')"
        cat > .env <<ENVEOF
DJANGO_SECRET_KEY=$SECRET
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=ragnar_db
DB_USER=ragnar_user
DB_PASSWORD=ragnar_pass
DB_HOST=localhost
DB_PORT=5432
UPLOADTHING_TOKEN=
UPLOADTHING_SECRET=
UPLOADTHING_CDN_URL=https://utfs.io/f
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
EMAIL_USE_TLS=True
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
SECURE_SSL_REDIRECT=False
ENVEOF
        ok "Minimal .env written"
    fi
fi

# --------------------------------------------------------- 6. migrations ----
step "6/8 Applying database migrations"

"$VENV_PY" manage.py check || fail "Django configuration check failed. Review .env and retry."
ok "Configuration check passed"

"$VENV_PY" manage.py makemigrations --noinput || warn "makemigrations: nothing to do or skipped."
"$VENV_PY" manage.py migrate --noinput || fail "Migrations failed. Verify database credentials in .env."
ok "Migrations applied"

if confirm "Seed the Support Resources library (27 entries)?"; then
    "$VENV_PY" manage.py seed_resources || warn "seed_resources failed - rerun later."
fi

if confirm "Populate demo data (254 students + incidents)? Skip on live databases!"; then
    if confirm "--fresh will DELETE existing incidents/students first. Continue?"; then
        "$VENV_PY" manage.py populate_users_data --fresh \
            || warn "populate_users_data failed - rerun once the DB is reachable."
    fi
fi

if confirm "Create a superuser account now?"; then
    "$VENV_PY" manage.py createsuperuser || warn "Superuser creation skipped - run it manually later."
fi

# ---------------------------------------------------------- 7. run server ---
step "7/8 Starting development server"

PORT="${DJANGO_DEV_PORT:-8000}"

# -------------------------------------------------------- 8. next steps -----
cat <<NEXTSTEPS

=====================================================
  ${GREEN}Setup complete!${RESET}
=====================================================

  Server starting at:  ${BOLD}http://127.0.0.1:${PORT}/${RESET}
  Admin panel:         ${BOLD}http://127.0.0.1:${PORT}/admin/${RESET}

  To run again later, activate the virtualenv FIRST:
$( [[ "$ENV" == "windows" ]] \
    && echo "      source .venv/Scripts/activate      # Windows (Git Bash)" \
    || echo "      source .venv/bin/activate         # Linux / macOS" )

      python manage.py runserver                    # start server
      python manage.py createsuperuser               # add admin
      python manage.py seed_resources                # re-seed resources
      python manage.py populate_users_data --fresh   # rebuild demo data
      python manage.py test tests                    # test suite

  Seeded default admin (only if you populated demo data):
      admin@futminna.edu.ng / admin123

  Press Ctrl+C to stop the server.
=====================================================
NEXTSTEPS

exec "$VENV_PY" manage.py runserver "0.0.0.0:${PORT}"
