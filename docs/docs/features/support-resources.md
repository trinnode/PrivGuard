---
sidebar_position: 4
title: Support Resources
---

# Support Resources

PrivGuard includes a library of **27 real Nigerian organisations** that provide support for privacy violations, mental health, legal aid, and digital safety.

## How Resources Are Matched

Resources are automatically recommended based on:

1. **Incident Classification** — the type of privacy violation (e.g., sextortion → NAPTIP)
2. **Harm Categories** — the harms reported (e.g., anxiety → Asido Foundation)
3. **Platform** — the platform where the incident occurred

The `Resource.recommended_for(incident, limit=4)` method returns the top 4 most relevant resources for any given incident.

## Resource Categories

| Category | Focus |
|----------|-------|
| **Legal** | Data protection law, cybercrime prosecution, legal aid |
| **Mental Health** | Counselling, psychological support, crisis intervention |
| **Digital Safety** | Digital rights, online safety, platform-specific guidance |
| **Law Enforcement** | Cybercrime investigation, police reporting |
| **Civic** | Advocacy, community support, policy engagement |

## Featured Organisations

### Data Protection & Legal

| Organisation | Contact | Focus |
|-------------|---------|-------|
| Nigeria Data Protection Commission (NDPC) | [ndpc.gov.ng](https://ndpc.gov.ng) | Data protection regulation |
| Digital Society Africa | [digitalsociety.africa](https://digitalsociety.africa) | Digital rights |
| Paradigm Initiative | [paradigmhq.org](https://paradigmhq.org) | Digital rights and inclusion |
| Enough is Enough Nigeria | [eieNigeria.org](https://eieNigeria.org) | Civic engagement |

### Law Enforcement

| Organisation | Contact | Focus |
|-------------|---------|-------|
| NPF-National Cybercrime Centre (NCCC) | 0800-CYBER (29237) | Cybercrime investigation |
| National Agency for the Prohibition of Trafficking in Persons (NAPTIP) | 6274 (Toll-free) | Human trafficking and exploitation |

### Mental Health

| Organisation | Contact | Focus |
|-------------|---------|-------|
| Asido Foundation | [asidofoundation.org](https://asidofoundation.org) | Mental health support |
| She Writes Woman | [shewriteswoman.org](https://shewriteswoman.org) | Women's mental health |
| Men Against Violence (MANI) | — | Gender-based violence |

### Digital Safety

| Organisation | Contact | Focus |
|-------------|---------|-------|
| Nigeria Computer Society | [ncs.org.ng](https://ncs.org.ng) | ICT advocacy |
| Centre for Information Technology and Development (CITAD) | [citad.org](https://citad.org) | IT development |

## Admin Management

Administrators can manage resources through the admin panel:

- **Add new resources** — with title, description, category, contact info, incident types, and harm categories
- **Edit existing resources** — update contact information, descriptions, or relevance tags
- **Deactivate resources** — hide resources that are no longer active

## Resource Fields

| Field | Description |
|-------|-------------|
| `title` | Organisation name |
| `category` | Legal, Mental Health, Digital Safety, Law Enforcement, Civic |
| `description` | What the organisation does |
| `website` | URL to the organisation's website |
| `contact_phone` | Phone number (displayed as clickable `tel:` link) |
| `contact_email` | Email address |
| `incident_types` | Comma-separated list of incident classifications this resource addresses |
| `harm_categories` | Comma-separated list of harm categories this resource addresses |
| `is_active` | Whether the resource is currently visible |
| `priority` | Display ordering (lower = higher priority) |

## Seeding Resources

```bash
# Seed all 27 resources
python manage.py seed_resources

# Resources are idempotent — running again updates existing entries
```
