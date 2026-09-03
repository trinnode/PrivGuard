---
sidebar_position: 1
title: Introduction
---

# PrivGuard — Privacy Incident Reporting System

PrivGuard is a web-based platform built for Nigerian university students to **document digital privacy violations**, classify associated psychological and tangible harms using an adapted academic taxonomy, access context-appropriate guidance, and export structured reports.

## Why PrivGuard?

Digital privacy violations are a growing concern among university students in Nigeria. Students face harassment on social media, data breaches, doxxing, sextortion, and non-consensual sharing of intimate images — yet there are few accessible, structured avenues for documenting these incidents and understanding their impact.

PrivGuard addresses this gap by providing:

- **A guided incident reporting process** that helps students document what happened, where, when, and who was involved
- **A harm classification system** adapted from academic research, covering 17 categories across psychological, tangible, and "other" domains
- **A support resource library** of 27 real Nigerian organisations that students can contact for help
- **PDF export** with unique reference codes that can be shared with authorities, counsellors, or legal advisors
- **Privacy by design** — students can request identity concealment, and all data is secured with industry-standard protections

## Key Concepts

| Concept | Description |
|---------|-------------|
| **Incident** | A documented privacy violation (e.g., social media harassment, data breach) |
| **Harm** | A specific negative outcome caused by the incident, classified into 17 categories |
| **Taxonomy** | The academic classification system used to categorise incidents and harms |
| **Concealment** | A privacy feature that redacts the reporter's identity in exports |
| **Reference Code** | A unique `PRG-XXXXXXXX` identifier assigned to each incident |
| **Resource** | A support organisation matched to the incident type and harm profile |

## System Architecture (High Level)

```
Browser ──► Django 5.0 ──► PostgreSQL
                │
                ├── Templates (HTML/CSS/JS)
                ├── PDF Engine (ReportLab)
                ├── File Upload (UploadThing / local)
                └── Audit Log (SHA-256 IP hash)
```

## Who Is This For?

- **Students** — Document privacy violations and get connected to support
- **Researchers** — Study patterns in digital privacy harms among university populations
- **Administrators** — Review reports, manage concealment requests, and monitor trends
- **Counsellors** — Use structured incident data to provide targeted support

## Quick Links

- [Installation Guide](./installation) — Set up PrivGuard locally
- [Configuration](./configuration) — Environment variables and database setup
- [Architecture](./architecture) — Detailed system design and database schema
- [Harm Taxonomy](./features/harm-taxonomy) — The 17-category classification system
- [Deployment](./deployment/vercel) — Deploy to production
