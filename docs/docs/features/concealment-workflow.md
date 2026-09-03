---
sidebar_position: 3
title: Concealment Workflow
---

# Concealment Workflow

The concealment system allows students to request that their identity be redacted from all exports and admin views. This is a critical privacy feature for students who fear retaliation.

## How It Works

```
User submits incident report
         │
         ▼
   Incident saved (visible to user + admin)
         │
         ▼
   User requests concealment (optional, at submission time)
         │
         ▼
   ┌─────────────────────────────────┐
   │  Admin reviews the request      │
   │  (visible on admin list/detail) │
   └─────────────────────────────────┘
         │
    ┌────┴────┐
    ▼         ▼
 GRANTED    DENIED
    │         │
    ▼         ▼
 Identity   Identity
 redacted   remains
 in all     visible
 exports    in exports
    │
    ▼
 Admin can REVOKE at any time
```

## Status Values

| Status | Description |
|--------|-------------|
| **None** | No concealment request has been made |
| **Requested** | User has requested concealment; awaiting admin review |
| **Granted** | Admin approved; identity is redacted in all exports |
| **Denied** | Admin rejected; identity remains visible |
| **Revoked** | Previously granted concealment was revoked by admin |

## Admin Interface

### List View (`/incidents/admin/`)

- **Pending badge**, shows count of pending requests; clickable to filter
- **Approve button**, grants concealment directly from the list row
- **Deny button**, denies concealment directly from the list row
- **Filters**, filter by concealment status to see all pending/granted/denied

### Detail View (`/incidents/admin/<id>/`)

- Shows full concealment status with timestamps
- Grant/Deny buttons for pending requests
- Revoke button for already-granted concealments
- Audit log entry created for every action

## Key Rules

1. **Admin decisions are sticky**, once granted or denied, the decision persists. Re-seeding data does not reset concealment status.
2. **Users cannot see their own concealment status** until it is granted (to prevent information leakage).
3. **Redacted incidents** show `[REDACTED]` in place of the reporter's name in all PDF exports and admin views.
4. **Revocation** changes the status back to "revoked" and makes the identity visible again in exports.

## PDF Export Behaviour

| Concealment Status | PDF Output |
|-------------------|------------|
| None | Full reporter identity included |
| Requested | Full reporter identity included (pending review) |
| Granted | Reporter name replaced with `[REDACTED]` |
| Denied | Full reporter identity included |
| Revoked | Full reporter identity included |

## Audit Trail

Every concealment action creates an `AuditLog` entry:

| Event Type | Description |
|-----------|-------------|
| `CONCEALMENT_REQUESTED` | User submitted a concealment request |
| `CONCEALMENT_GRANTED` | Admin approved the request |
| `CONCEALMENT_DENIED` | Admin rejected the request |
| `CONCEALMENT_REVOKED` | Admin revoked previously granted concealment |

Each entry records the timestamp, user, action summary, and a SHA-256 hash of the IP address.
