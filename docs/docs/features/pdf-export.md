---
sidebar_position: 5
title: PDF Export
---

# PDF Export

PrivGuard generates structured PDF reports for incidents using ReportLab. Reports can be exported individually or in bulk.

## Single Incident Export

Each PDF includes:

| Section | Content |
|---------|---------|
| **Header** | PrivGuard logo, reference code (`PRG-XXXXXXXX`), generation timestamp |
| **Incident Summary** | Platform, classification, date, severity rating |
| **Narrative** | The full incident description |
| **Harm Classification** | Each harm with category, severity, duration, and elaboration |
| **Evidence Summary** | File attachment details (not embedded in PDF) |
| **Support Resources** | Top 4 recommended organisations for this incident |

## Identity Redaction

When concealment is active:

- **Reporter name** → `[REDACTED]`
- **Contact information** → `[REDACTED]`
- **All personally identifiable information** → `[REDACTED]`

The reference code (`PRG-XXXXXXXX`) is always preserved, even in redacted exports, as it is not personally identifiable.

## Bulk Export

Admins can export multiple incidents as a single PDF with:

- **Table of Contents**, numbered list of all included incidents
- **Per-incident sections**, each incident as a separate section with full details
- **Redaction applied consistently**, concealed incidents are redacted throughout the bulk export

## Reference Codes

Every incident receives a unique reference code:

| Property | Value |
|----------|-------|
| Format | `PRG-XXXXXXXX` |
| Prefix | `PRG-` (PrivGuard) |
| Length | 12 characters total |
| Character set | Alphanumeric (A-Z, 0-9) |
| Uniqueness | Guaranteed system-wide |
| Generation | Automatic on incident submission |

## Text Fallback

If PDF generation fails (e.g., due to memory constraints or library issues), the system automatically falls back to a plain-text report:

```text
====================================
    PRIVGUARD INCIDENT REPORT
====================================
Reference Code: PRG-A1B2C3D4
Date: 2026-05-15
Platform: Instagram
Classification: Social media harassment
Severity: 3/4

NARRATIVE:
[incident description]

HARM CLASSIFICATION:
1. Anxiety (Severity: 3, Duration: Recurring)
2. Social Withdrawal (Severity: 2, Duration: Ongoing)

SUPPORT RESOURCES:
1. Asido Foundation - asidofoundation.org
2. She Writes Woman - shewriteswoman.org
====================================
```

## Export Access

| User Type | Can Export |
|-----------|-----------|
| Student | Own incidents only |
| Researcher | All non-concealed incidents |
| Admin | All incidents (concealed ones are redacted) |

## API

PDF export is triggered via:

```
GET /incidents/<id>/export/pdf/
GET /incidents/admin/export/bulk-pdf/
```

Both endpoints require authentication. The bulk endpoint requires admin privileges.
