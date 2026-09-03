---
sidebar_position: 1
title: Incident Reporting
---

# Incident Reporting

PrivGuard provides a multi-step guided form for documenting digital privacy violations. Each incident is classified with a structured taxonomy and assigned a unique reference code.

## Creating an Incident

### Step 1: Platform & Classification

| Field | Options |
|-------|---------|
| **Platform Category** | Instagram, Twitter/X, TikTok, WhatsApp, Facebook, Snapchat, Telegram, Other Social Media, Non-Social Platform |
| **Platform Name** | Free-text field for the specific platform or service |
| **Incident Classification** | Social media harassment, Data breach, Doxxing, Sextortion, Non-consensual intimate image sharing, Account compromise, Phishing, Identity theft, Location tracking, Spyware/surveillance, Impersonation, Blackmail, Workplace monitoring, Academic surveillance |

### Step 2: Incident Details

| Field | Description |
|-------|-------------|
| **Date of Occurrence** | When the incident happened |
| **Narrative** | Detailed description of what happened (free-text) |
| **Actor Involvement** | Who was involved (known person, anonymous, institution, etc.) |
| **Actor Description** | Additional details about the actor |
| **Severity Rating** | 1 (Minor) to 4 (Severe) |

### Step 3: Harm Classification

Users select one or more harm categories and rate each:

- **Harm Category**, one of 17 categories (9 psychological, 7 tangible, 1 other)
- **Severity Score**, 1 to 4 for each selected harm
- **Duration**, one-time, recurring, ongoing, or unknown
- **Elaboration**, optional free-text explanation

### Step 4: Evidence & Privacy

| Field | Description |
|-------|-------------|
| **Evidence File** | Upload supporting evidence (max 100 KB; PNG, JPEG, or PDF) |
| **Anonymous Submission** | Toggle to hide identity from other users |
| **Concealment Request** | Request identity redaction in all exports |

### Step 5: Review & Submit

Users review all entered information before final submission.

## Reference Codes

Every incident receives a unique reference code in the format `PRG-XXXXXXXX`, where `XXXXXXXX` is an 8-character alphanumeric string. This code:

- Is generated automatically on submission
- Appears on all PDF exports
- Can be used to look up the incident in admin panels
- Is unique across the entire system

## Incident Lifecycle

```
DRAFT → SUBMITTED → UNDER REVIEW → RESOLVED
                                    → CLOSED
```

| Status | Description |
|--------|-------------|
| **Draft** | Incident saved but not yet submitted |
| **Submitted** | Incident awaiting admin review |
| **Under Review** | Admin is actively reviewing the incident |
| **Resolved** | Issue has been addressed |
| **Closed** | Incident closed without resolution |

## Viewing Incidents

### User View

Users can see their own incidents at `/incidents/`. Each incident shows:
- Reference code and status
- Platform and classification
- Severity rating with visual indicator
- Harm categories applied
- Evidence attachment (if any)
- Concealment status badge

### Admin View

Admins see all incidents at `/incidents/admin/` with:
- **7-filter search**, status, concealment, classification, platform, severity, date range
- **Newest-first ordering**, most recent incidents appear first
- **Approve/Deny buttons**, directly in the list rows for concealment requests
- **Clickable pending badge**, filters to pending concealment requests
- **Recommended Support**, context-appropriate resources on the detail page

## Autosave

Incident forms are automatically saved to the browser's local storage as the user types. This prevents data loss from:

- Browser crashes
- Network interruptions
- Accidental navigation away

Autosave is enabled by default and can be disabled in user preferences.

## Distress Keyword Detection

The system monitors incident narratives for keywords associated with acute distress (e.g., self-harm, suicidal ideation). When detected, the incident is flagged for priority review and the user is presented with immediate support resources.
