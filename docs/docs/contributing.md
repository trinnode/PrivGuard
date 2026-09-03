---
sidebar_position: 10
title: Contributing
---

# Contributing

Contributions to PrivGuard are welcome. This guide covers the development workflow.

## Development Setup

```bash
# Clone the repository
git clone https://github.com/trinnode/PrivGuard.git
cd PrivGuard

# Run the setup script
bash setup.sh

# Or set up manually (see Installation guide)
```

## Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

Branch naming conventions:
- `feature/`, new features
- `fix/`, bug fixes
- `docs/`, documentation changes
- `refactor/`, code refactoring
- `test/`, adding or updating tests

### 2. Make Changes

- Follow the existing code style
- Keep functions small and focused
- Add docstrings to new functions
- Write tests for new functionality

### 3. Run Tests

```bash
python manage.py test tests/ -v 2
```

### 4. Commit

```bash
git add .
git commit -m "feat: add description of your change"
```

Commit message conventions:
- `feat:`, new feature
- `fix:`, bug fix
- `docs:`, documentation change
- `refactor:`, code refactoring
- `test:`, adding/updating tests
- `chore:`, maintenance tasks

### 5. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then open a Pull Request on GitHub.

## Code Style

- **Python**: Follow PEP 8
- **Templates**: Use 4-space indentation
- **CSS**: Use the existing design system variables
- **JavaScript**: Use vanilla JS (no frameworks)

## Project Conventions

| Convention | Standard |
|-----------|----------|
| Reference codes | `PRG-XXXXXXXX` format |
| Date format | ISO 8601 (`YYYY-MM-DD`) |
| Time format | 24-hour (`HH:MM:SS`) |
| Database | PostgreSQL (no SQLite in production) |
| Password hashing | Argon2id |
| Session timeout | 15 minutes |

## Architecture Decisions

- **Server-rendered**, Django templates, no SPA framework
- **No REST API**, current implementation is template-based; API endpoints reserved at `/api/v1/`
- **Single database**, PostgreSQL only; no SQLite in production
- **File uploads**, UploadThing cloud with local fallback
- **PDF generation**, ReportLab (not WeasyPrint or wkhtmltopdf)

## Reporting Issues

Open an issue on [GitHub Issues](https://github.com/trinnode/PrivGuard/issues) with:

1. **Description**, what happened vs. what you expected
2. **Steps to reproduce**, exact steps to trigger the issue
3. **Environment**, OS, Python version, browser
4. **Screenshots**, if applicable
5. **Logs**, relevant error messages

## License

This project is developed for academic research purposes. Contributions should respect the privacy-first design philosophy.
