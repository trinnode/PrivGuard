#!/usr/bin/env bash
# =============================================================================
# PrivGuard One-Shot Setup Script (v3 — cross-platform, version-pinned)
#
# What this script handles:
#   * Linux families: Debian/Ubuntu/Kali (apt), Fedora/RHEL (dnf/yum),
#     Arch (pacman), openSUSE (zypper) — correct, VERSION-PINNED packages
#   * macOS via Homebrew
#   * Windows ONLY through POSIX shell (Git Bash / MSYS2 / WSL)
#   * Debian's python3.XX-venv / python3.XX-pip / python3.XX-dev naming
#   * ensurepip stripped by distros — falls back to virtualenv wrapper
#   * Python >= 3.10 required (Django 5+ baseline)
#   * Binary wheel failures → installs C headers + compilers → retries source
#
# Usage:
#   bash setup.sh          # interactive (prompts at each decision point)
#   bash setup.sh --yes    # accept all defaults (fully non-interactive)
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
fail() { printf "${RED}  ✘ ERROR: %s${RESET}\n" "$*" >&2; exit 1; }

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
       One-Shot Environment Setup (v3)
=====================================================
BANNER

# ==================================================== 1. ENVIRONMENT ========
step "1/8 Detecting environment"

RAW_UNAME="$(uname -s)"
case "$RAW_UNAME" in
    Linux*)                AUTO_ENV="linux" ;;
    Darwin*)               AUTO_ENV="macos" ;;
    MINGW*|MSYS*|CYGWIN*)  AUTO_ENV="windows" ;;
    *)                     AUTO_ENV="unknown" ;;
esac

# Identify the Linux distribution family (used everywhere for package mapping)
OS_FAMILY=""
DISTRO_ID=""
DISTRO_ID_LIKE=""
if [[ "$AUTO_ENV" == "linux" ]] && [[ -r /etc/os-release ]]; then
    # shellcheck disable=SC1091
    . /etc/os-release
    DISTRO_ID="${ID:-}"
    DISTRO_ID_LIKE="${ID_LIKE:-}"
    case "$DISTRO_ID" in
        ubuntu|debian|kali|linuxmint|pop|raspbian|parrot) OS_FAMILY="debian" ;;
        fedora|rhel|centos|rocky|almalinux|amzn|ol)       OS_FAMILY="rhel" ;;
        arch|manjaro|endeavouros|garuda)                   OS_FAMILY="arch" ;;
        opensuse*|sles)                                    OS_FAMILY="suse" ;;
        *)
            case "$DISTRO_ID_LIKE" in
                *debian*)     OS_FAMILY="debian" ;;
                *fedora*|*rhel*|*centos*) OS_FAMILY="rhel" ;;
                *arch*)       OS_FAMILY="arch" ;;
                *suse*)       OS_FAMILY="suse" ;;
                *)            OS_FAMILY="unknown" ;;
            esac ;;
    esac
elif [[ "$AUTO_ENV" == "macos" ]]; then
    OS_FAMILY="brew"
fi

echo "  Auto-detected: ${BOLD}${AUTO_ENV}${RESET} (family: ${BOLD}${OS_FAMILY:-unknown}${RESET})"
echo ""
echo "  Which environment is this?"
echo "    1) Linux"
echo "    2) Windows (Git Bash / MSYS2 / WSL only — .sh requires a POSIX shell)"
echo "    3) macOS"
read -r -p "  Enter choice [1/2/3] (Enter = auto-detect '$AUTO_ENV'): " ENV_CHOICE

case "$ENV_CHOICE" in
    1) ENV="linux" ;;
    2) ENV="windows" ;;
    3) ENV="macos" ;;
    "") ENV="$AUTO_ENV" ;;
    *) warn "Unknown choice — using auto-detection."; ENV="$AUTO_ENV" ;;
esac

case "$ENV" in
    linux|macos|windows) ok "Environment: $ENV ($OS_FAMILY)" ;;
    *) fail "Unrecognised environment '$ENV'. Use a POSIX-compatible shell (bash/zsh)." ;;
esac

# ==================================================== PRIVILEGE / PKG MGR ===

SUDO=""
if [[ "$(id -u)" -ne 0 ]] && command -v sudo >/dev/null 2>&1; then
    SUDO="sudo"
fi

pkg_install() {
    # Raw package-name installer — call AFTER map_pkg for versioned names.
    local pkg="$1"
    [[ -z "$pkg" ]] && return 0
    case "$OS_FAMILY" in
        debian)
            $SUDO apt-get update -y >/dev/null 2>&1 || true
            $SUDO DEBIAN_FRONTEND=noninteractive apt-get install -y "$pkg" ;;
        rhel)
            $SUDO dnf install -y "$pkg" 2>/dev/null || $SUDO yum install -y "$pkg" ;;
        arch)
            $SUDO pacman -Sy --noconfirm --needed "$pkg" ;;
        suse)
            $SUDO zypper install -y "$pkg" ;;
        brew)
            brew install "$pkg" ;;
        *)
            fail "No supported package manager found. Install '$pkg' manually." ;;
    esac
}

# ==================================================== 2. PYTHON TOOLCHAIN ===
step "2/8 Checking & installing Python"

py_major_minor() {
    "$1" -c 'import sys; print(f"{sys.version_info[0]}.{sys.version_info[1]}")'
}

py_version_tag() {
    # Returns just the minor: "3.11", "3.12", etc.
    "$1" -c 'import sys; print(f"{sys.version_info[0]}.{sys.version_info[1]}")'
}

# --- find a usable Python >= 3.10 ---
PY_BIN=""
for candidate in python3.13 python3.12 python3.11 python3.10 python3 python; do
    if command -v "$candidate" >/dev/null 2>&1; then
        if "$candidate" -c 'import sys; sys.exit(0 if sys.version_info >= (3,10) else 1)' 2>/dev/null; then
            PY_BIN="$candidate"; break
        fi
    fi
done

# --- install one if nothing found ---
if [[ -z "$PY_BIN" ]]; then
    warn "Python >= 3.10 not found on this system."
    if confirm "Attempt automatic installation?"; then
        case "$OS_FAMILY" in
            debian)
                $SUDO apt-get update -y >/dev/null 2>&1 || true
                # Try every versioned Python we know of, newest first.
                for ver in python3.13 python3.12 python3.11 python3.10; do
                    verpkg="${ver}"
                    $SUDO DEBIAN_FRONTEND=noninteractive apt-get install -y "$verpkg" 2>/dev/null \
                        && { PY_BIN="$(command -v "$ver")"; break; }
                done
                # If the distro repo has no modern Python, try deadsnakes (Ubuntu/Pop only)
                if [[ -z "$PY_BIN" ]]; then
                    $SUDO DEBIAN_FRONTEND=noninteractive apt-get install -y software-properties-common 2>/dev/null || true
                    $SUDO add-apt-repository -y ppa:deadsnakes/ppa 2>/dev/null || true
                    $SUDO DEBIAN_FRONTEND=noninteractive apt-get update -y >/dev/null 2>&1 || true
                    for ver in python3.13 python3.12 python3.11 python3.10; do
                        $SUDO DEBIAN_FRONTEND=noninteractive apt-get install -y "$ver" 2>/dev/null \
                            && { PY_BIN="$(command -v "$ver")"; break; }
                    done
                fi
                ;;
            rhel)
                for ver in python3.13 python3.12 python3.11 python3.10; do
                    pkg_install "$ver" 2>/dev/null \
                        && { PY_BIN="$(command -v "$ver")"; break; }
                done
                ;;
            arch)  pkg_install python; PY_BIN="$(command -v python)" ;;
            suse)
                for ver in python313 python312 python311 python310; do
                    pkg_install "$ver" 2>/dev/null \
                        && { PY_BIN="$(command -v "${ver:0:6}.${ver:6}")"; break; }
                done
                [[ -z "$PY_BIN" ]] && { pkg_install python3; PY_BIN="$(command -v python3)"; } ;;
            brew)
                pkg_install python@3.12
                PY_BIN="$(command -v python3.12 || command -v python3)" ;;
            *)
                fail "Install Python >= 3.10 manually, then re-run this script." ;;
        esac
    fi
    [[ -z "$PY_BIN" ]] && fail "Cannot continue without Python >= 3.10 (Django 5+ requirement)."
fi

PY_TAG="$(py_version_tag "$PY_BIN")"
ok "Python $($PY_BIN --version) at $(command -v "$PY_BIN") (version tag: $PY_TAG)"

# ==================================================== VERSION-PINNED PKGS ====
# On Debian/Kali/Ubuntu, many Python support packages are version-pinned:
#   python3.11-venv, python3.11-pip, python3.11-dev, etc.
# Other distros (RHEL/Fedora/Arch/macOS) bundle them inside the main python
# package or use a generic name. This section detects the right names.

DEB_PY_PKG=""   # e.g. python3.11
DEB_VENV_PKG="" # e.g. python3.11-venv
DEB_PIP_PKG=""  # e.g. python3.11-pip
DEB_DEV_PKG=""  # e.g. python3.11-dev

if [[ "$OS_FAMILY" == "debian" ]]; then
    DEB_PY_PKG="python${PY_TAG}"
    DEB_VENV_PKG="python${PY_TAG}-venv"
    DEB_PIP_PKG="python${PY_TAG}-distutils"  # distutils covers pip bootstrapping
    DEB_DEV_PKG="python${PY_TAG}-dev"
    info "Debian-family detected: will use versioned packages ($DEB_VENV_PKG, etc.)"
fi

# pip version detection (for flags that only exist on newer pips)
pip_has_flag() {
    "$VENV_PY" -m pip install --help 2>/dev/null | grep -q -- "$1"
}

# ==================================================== 3. VIRTUAL ENVIRONMENT ==
step "3/8 Creating virtual environment"

VENV_DIR="$PROJECT_DIR/.venv"

# --- 3a. Ensure the venv MODULE is available before attempting creation ---
ensure_venv_module() {
    # Quick check: can we import venv at all?
    if "$PY_BIN" -c "import venv" 2>/dev/null; then
        return 0
    fi

    warn "Python venv module is not available."

    case "$OS_FAMILY" in
        debian)
            info "On Debian/Kali/Ubuntu, venv lives in a version-pinned package."
            info "Installing ${BOLD}${DEB_VENV_PKG}${RESET}..."
            pkg_install "$DEB_VENV_PKG" && return 0
            # Fallback: also try the generic name
            pkg_install python3-venv 2>/dev/null && return 0
            ;;
        rhel|arch|suse)
            # On these distros, venv is built into the main python package.
            # If it's missing, re-installing the python package may help.
            info "Re-installing Python to recover the venv module..."
            pkg_install "$DEB_PY_PKG" 2>/dev/null && return 0
            ;;
        brew)
            info "macOS Homebrew: reinstalling Python with venv support..."
            brew reinstall "python@${PY_TAG}" 2>/dev/null && return 0
            brew reinstall python@3.12 2>/dev/null && return 0
            ;;
        windows)
            info "Windows/MSYS2: installing python3-venv..."
            pacman -S --noconfirm python3-venv 2>/dev/null \
                || pacman -S --noconfirm msys/python 2>/dev/null \
                || true
            ;;
    esac

    # Final check after install attempt
    if "$PY_BIN" -c "import venv" 2>/dev/null; then
        return 0
    fi

    return 1
}

# --- 3b. Attempt venv creation with full retry chain ---
create_venv() {
    local venv_python="$1" venv_dir="$2"

    # Strategy 1: straight python -m venv
    info "Attempting: $venv_python -m venv $venv_dir"
    if "$venv_python" -m venv "$venv_dir" 2>/dev/null; then
        return 0
    fi
    warn "python -m venv failed (ensurepip may be unavailable)."

    # Strategy 2: python -m venv --without-pip → then bootstrap pip manually
    info "Retrying with --without-pip flag..."
    rm -rf "$venv_dir" 2>/dev/null || true
    if "$venv_python" -m venv --without-pip "$venv_dir" 2>/dev/null; then
        info "venv created without pip — bootstrapping pip via get-pip.py..."
        # Determine venv python path
        local vp
        if [[ -x "$venv_dir/bin/python" ]]; then vp="$venv_dir/bin/python"; else vp="$venv_dir/Scripts/python"; fi
        curl -sS https://bootstrap.pypa.io/get-pip.py | "$vp" 2>/dev/null && return 0
        warn "get-pip.py bootstrap failed."
    fi
    rm -rf "$venv_dir" 2>/dev/null || true

    # Strategy 3: install virtualenv as a universal fallback
    info "Falling back to virtualenv (third-party venv manager)..."
    if "$venv_python" -m pip install --quiet virtualenv 2>/dev/null; then
        "$venv_python" -m virtualenv "$venv_dir" 2>/dev/null && return 0
    fi

    # Strategy 4: try installing virtualenv at system level via package manager
    info "Trying system-level virtualenv install..."
    case "$OS_FAMILY" in
        debian) pkg_install python3-virtualenv 2>/dev/null || pkg_install virtualenv 2>/dev/null ;;
        rhel)   pkg_install python3-virtualenv 2>/dev/null ;;
        arch)   pkg_install python-virtualenv 2>/dev/null ;;
        brew)   brew install virtualenv 2>/dev/null ;;
    esac
    if command -v virtualenv >/dev/null 2>&1; then
        virtualenv "$venv_dir" 2>/dev/null && return 0
    fi

    return 1
}

# --- 3c. Pre-install the venv module (critical on Debian) ---
ensure_venv_module \
    || warn "Could not auto-install the venv module. Attempting venv creation anyway..."

# --- 3d. Detect existing venv or create new one ---
if [[ -d "$VENV_DIR" ]] && [[ -x "$VENV_DIR/bin/python" || -x "$VENV_DIR/Scripts/python" || -x "$VENV_DIR/Scripts/python.exe" ]]; then
    ok "Reusing existing virtualenv: $VENV_DIR"
else
    rm -rf "$VENV_DIR" 2>/dev/null || true
    create_venv "$PY_BIN" "$VENV_DIR" \
        || fail \
"venv creation failed on all strategies. You must fix this manually:

  ${BOLD}Step 1 — install the versioned venv package:${RESET}
    Debian/Kali/Ubuntu:  sudo apt install ${DEB_VENV_PKG:-python3.XX-venv}
    Fedora/RHEL:         sudo dnf install python3
    Arch:                sudo pacman -S python
    openSUSE:            sudo zypper install python3

  ${BOLD}Step 2 — recreate the venv:${RESET}
    $PY_BIN -m venv $VENV_DIR

  ${BOLD}Step 3 — re-run this script:${RESET}
    bash setup.sh
"
fi

# --- 3e. Locate the venv interpreter (POSIX bin/ vs Windows Scripts/) ---
if [[ -x "$VENV_DIR/bin/python" ]]; then
    VENV_PY="$VENV_DIR/bin/python"
    VENV_PIP="$VENV_DIR/bin/pip"
elif [[ -x "$VENV_DIR/Scripts/python.exe" ]]; then
    VENV_PY="$VENV_DIR/Scripts/python.exe"
    VENV_PIP="$VENV_DIR/Scripts/pip.exe"
elif [[ -x "$VENV_DIR/Scripts/python" ]]; then
    VENV_PY="$VENV_DIR/Scripts/python"
    VENV_PIP="$VENV_DIR/Scripts/pip"
else
    fail \
"Virtualenv exists but its interpreter was not found.

  Expected locations:
    Linux/macOS:  $VENV_DIR/bin/python
    Windows:      $VENV_DIR/Scripts/python.exe

  Fix: delete the venv and re-run this script:
    rm -rf $VENV_DIR && bash setup.sh
"
fi

ok "Virtualenv interpreter: $("$VENV_PY" --version) at $VENV_PY"

# Ensure pip is available inside the venv (some --without-pip installs leave it out)
if ! "$VENV_PY" -m pip --version >/dev/null 2>&1; then
    warn "pip not available inside venv — bootstrapping..."
    if [[ -f "$VENV_DIR/bin/activate" ]]; then
        # POSIX activate always sets up PATH correctly
        # shellcheck disable=SC1091
        source "$VENV_DIR/bin/activate" && pip install --upgrade pip 2>/dev/null \
            || "$VENV_PY" -m ensurepip --upgrade 2>/dev/null \
            || true
    fi
    # Last resort: get-pip.py
    if ! "$VENV_PY" -m pip --version >/dev/null 2>&1; then
        info "Bootstrapping pip via get-pip.py..."
        curl -sS https://bootstrap.pypa.io/get-pip.py | "$VENV_PY" 2>/dev/null \
            || fail "Could not install pip inside the virtualenv."
    fi
    ok "pip bootstrapped: $("$VENV_PY" -m pip --version | head -1)"
else
    ok "pip available: $("$VENV_PY" -m pip --version | head -1)"
fi

# ==================================================== 4. PYTHON DEPS ========
step "4/8 Installing latest Python dependencies"

"$VENV_PY" -m pip install --upgrade --quiet pip setuptools wheel 2>/dev/null || true
echo ""

DEPS=(django psycopg2-binary gunicorn whitenoise python-decouple dj-database-url reportlab pillow argon2-cffi)

install_dep() {
    local dep="$1"
    info "Installing latest: $dep"

    # First attempt: binary wheel (fast, no compiler needed)
    if "$VENV_PY" -m pip install --upgrade --quiet "$dep" 2>/dev/null; then
        return 0
    fi

    # Second attempt: install native build tools, then retry from source
    warn "  Binary wheel unavailable for $dep — installing build tools..."

    case "$OS_FAMILY" in
        debian)
            # Use version-pinned dev headers on Debian
            local devpkg="${DEB_DEV_PKG:-python3-dev}"
            $SUDO apt-get update -y >/dev/null 2>&1 || true
            $SUDO DEBIAN_FRONTEND=noninteractive apt-get install -y \
                build-essential "$devpkg" libpq-dev libjpeg-dev zlib1g-dev 2>/dev/null || true
            ;;
        rhel)
            $SUDO dnf install -y \
                gcc gcc-c++ python3-devel libpq-devel libjpeg-turbo-devel zlib-devel 2>/dev/null \
                || $SUDO yum install -y \
                gcc gcc-c++ python3-devel libpq-devel libjpeg-devel zlib-devel 2>/dev/null || true
            ;;
        arch)
            $SUDO pacman -Sy --noconfirm --needed \
                base-devel libjpeg-turbo zlib postgresql-libs 2>/dev/null || true
            ;;
        suse)
            $SUDO zypper install -y -t pattern devel_basis 2>/dev/null || true
            $SUDO zypper install -y \
                gcc python3-devel libpq-devel libjpeg-devel zlib-devel 2>/dev/null || true
            ;;
        brew)
            xcode-select --install 2>/dev/null || true
            brew install libpq jpeg-turbo 2>/dev/null || true
            ;;
        windows)
            info "Windows: ensure gcc/mingw is in PATH if this step fails."
            ;;
    esac

    if "$VENV_PY" -m pip install --upgrade --quiet --no-binary :all: "$dep" 2>/dev/null; then
        return 0
    fi

    # Final attempt: allow pip to pick whatever works
    if "$VENV_PY" -m pip install --upgrade --quiet "$dep" 2>/dev/null; then
        return 0
    fi

    fail \
"Failed to install '$dep' after multiple attempts.

  ${BOLD}Manual fix:${RESET}
    1. Ensure you have a C compiler: gcc --version
    2. Install dev headers for your distro (see output above)
    3. Re-run: bash setup.sh
"
}

for dep in "${DEPS[@]}"; do
    install_dep "$dep"
done
echo ""

ok "All dependencies installed:"
"$VENV_PY" -m pip show django psycopg2-binary reportlab pillow argon2-cffi \
    gunicorn whitenoise python-decouple dj-database-url 2>/dev/null \
    | grep -E "^(Name|Version):" | paste - - | sed 's/^/    /' || true

# ==================================================== 5. ENV FILE ===========
step "5/8 Preparing environment variables"

if [[ -f ".env" ]]; then
    ok ".env already exists — leaving untouched"
else
    if [[ -f ".env.example" ]]; then
        cp .env.example .env
        ok "Copied .env.example -> .env"
        warn "Edit .env to set DJANGO_SECRET_KEY, DATABASE_URL / DB_*, UploadThing tokens before production."
        if confirm "Open .env for editing now?"; then
            "${EDITOR:-vi}" .env || true
        fi
    else
        warn ".env.example not found — writing a minimal .env"
        SECRET="$("$VENV_PY" -c 'import secrets; print(secrets.token_urlsafe(48))' 2>/dev/null || head -c 48 /dev/urandom | base64)"
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

# ==================================================== 6. MIGRATIONS =========
step "6/8 Applying database migrations"

"$VENV_PY" manage.py check || fail "Django config check failed. Review .env and retry."
ok "Configuration check passed"

"$VENV_PY" manage.py makemigrations --noinput 2>/dev/null || warn "makemigrations: nothing to do."
"$VENV_PY" manage.py migrate --noinput \
    || fail "Migration failed. Verify DATABASE_URL / DB_* credentials in .env and that PostgreSQL is running."
ok "Migrations applied"

if confirm "Seed the Support Resources library (27 entries)?"; then
    "$VENV_PY" manage.py seed_resources || warn "seed_resources failed — rerun later."
fi

if confirm "Populate demo data (254 students + incidents)? Skip on live databases!"; then
    if confirm "--fresh will DELETE existing incidents/students. Continue?"; then
        "$VENV_PY" manage.py populate_users_data --fresh \
            || warn "populate_users_data failed — rerun once the DB is reachable."
    fi
fi

if confirm "Create a superuser account now?"; then
    "$VENV_PY" manage.py createsuperuser || warn "Superuser creation skipped."
fi

# ==================================================== 7. DOCUMENTATION ======
step "7/9 Setting up documentation site"

if command -v node >/dev/null 2>&1 && command -v npm >/dev/null 2>&1; then
    if confirm "Install Docusaurus documentation site (requires Node.js)?"; then
        if [[ -d "docs/node_modules" ]]; then
            ok "Docusaurus dependencies already installed"
        else
            info "Installing Docusaurus dependencies..."
            (cd docs && npm install --no-audit --no-fund 2>/dev/null) \
                && ok "Docusaurus dependencies installed" \
                || warn "npm install failed — docs site not set up"
        fi
        if [[ -d "docs/node_modules" ]]; then
            info "Building documentation site..."
            (cd docs && npm run build 2>/dev/null) \
                && ok "Documentation built in docs/build/" \
                || warn "Documentation build failed"
        fi
    fi
else
    warn "Node.js not found — skipping documentation setup"
    info "To set up docs later: install Node.js 18+, then run 'cd docs && npm install && npm run build'"
fi

# ==================================================== 8. START SERVER =======
step "8/9 Starting development server"

PORT="${DJANGO_DEV_PORT:-8000}"

# ==================================================== 8. SUMMARY ============
cat <<NEXTSTEPS

=====================================================
  ${GREEN}Setup complete!${RESET}
=====================================================

  Server starting at:  ${BOLD}http://127.0.0.1:${PORT}/${RESET}
  Admin panel:         ${BOLD}http://127.0.0.1:${PORT}/admin/${RESET}

  To run again later, activate the virtualenv FIRST:
$( [[ "$ENV" == "windows" ]] \
    && echo "      source .venv/Scripts/activate      # Windows (Git Bash/WSL)" \
    || echo "      source .venv/bin/activate         # Linux / macOS" )

      python manage.py runserver                    # start server
      python manage.py createsuperuser               # add admin
      python manage.py seed_resources                # re-seed resources
      python manage.py populate_users_data --fresh   # rebuild demo data
      python manage.py test tests                    # run tests

  Seeded default admin (only if you populated demo data):
      admin@futminna.edu.ng / admin123

  Documentation site:
      cd docs && npm run serve     # preview docs locally at http://localhost:3000

  Press Ctrl+C to stop the server.
=====================================================
NEXTSTEPS

exec "$VENV_PY" manage.py runserver "0.0.0.0:${PORT}"
