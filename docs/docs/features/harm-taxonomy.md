---
sidebar_position: 2
title: Harm Taxonomy
---

# Harm Taxonomy

The harm taxonomy is adapted from academic research on digital privacy harms among university students. It provides a structured framework for classifying the negative outcomes of privacy violations.

## Overview

| Domain | Categories |
|--------|-----------|
| Psychological | 9 categories |
| Tangible | 7 categories |
| Other | 1 category |
| **Total** | **17 categories** |

## Psychological Harms

| # | Category | Description |
|---|----------|-------------|
| 1 | **Anxiety** | Persistent worry or nervousness about the privacy violation |
| 2 | **Humiliation** | Embarrassment or shame from exposure of private information |
| 3 | **Distress** | Emotional suffering caused by the privacy incident |
| 4 | **Fear for Safety** | Concern about physical safety following a privacy breach |
| 5 | **Loss of Trust** | Diminished trust in people, platforms, or institutions |
| 6 | **Self-blame** | Internalized guilt or responsibility for the incident |
| 7 | **Social Withdrawal** | Avoidance of social interactions due to the incident |
| 8 | **Academic Anxiety** | Worry about academic consequences of the privacy violation |
| 9 | **Trauma Symptoms** | Post-incident psychological effects (flashbacks, hypervigilance) |

## Tangible Harms

| # | Category | Description |
|---|----------|-------------|
| 1 | **Reputation Harm** | Damage to personal or professional reputation |
| 2 | **Academic Penalty** | Negative academic consequences (suspension, grade impact) |
| 3 | **Financial Loss** | Monetary loss resulting from the privacy incident |
| 4 | **Lost Opportunity** | Missed opportunities due to the privacy violation |
| 5 | **Social Ostracism** | Exclusion from social groups or communities |
| 6 | **Employment Impact** | Adverse effects on job prospects or current employment |
| 7 | **Physical Safety Threat** | Risk of physical harm due to exposed personal information |

## Other

| # | Category | Description |
|---|----------|-------------|
| 1 | **Other** | Harms that do not fit the above categories |

## Severity Levels

Each harm is rated on a 4-point severity scale:

| Level | Label | Description |
|-------|-------|-------------|
| 1 | Minor | Minimal impact, easily recoverable |
| 2 | Moderate | Noticeable impact requiring some effort to address |
| 3 | Significant | Serious impact affecting daily life or wellbeing |
| 4 | Severe | Critical impact requiring immediate intervention |

## Duration Classification

| Value | Description |
|-------|-------------|
| One-time | Single occurrence with no ongoing effects |
| Recurring | Repeated incidents over time |
| Ongoing | Continuous or persistent impact |
| Unknown | Unable to determine duration |

## Incident Classifications

The system recognises 14 incident types:

| Classification | Description |
|---------------|-------------|
| Social media harassment | Bullying, threats, or abuse on social platforms |
| Data breach | Unauthorised access to personal data |
| Doxxing | Publication of private personal information |
| Sextortion | Threats to release intimate content |
| Non-consensual intimate image sharing | Distribution of intimate images without consent |
| Account compromise | Unauthorised access to user accounts |
| Phishing | Deceptive attempts to obtain credentials |
| Identity theft | Use of personal information for impersonation |
| Location tracking | Unauthorised monitoring of physical location |
| Spyware/surveillance | Installation of monitoring software |
| Impersonation | Posing as someone else online |
| Blackmail | Threats to reveal information for gain |
| Workplace monitoring | Surveillance by employers beyond legal bounds |
| Academic surveillance | Monitoring by educational institutions |

## Platform Categories

| Platform |
|----------|
| Instagram |
| Twitter/X |
| TikTok |
| WhatsApp |
| Facebook |
| Snapchat |
| Telegram |
| Other Social Media |
| Non-Social Platform |

## How Harms Are Seeded

When demo data is generated via `populate_users_data`, harms are automatically assigned to incidents based on:

1. **Platform** — certain platforms are associated with higher rates of specific harms
2. **Classification** — different incident types produce different harm profiles
3. **Severity** — higher-severity incidents produce more harm categories

The seeding distribution ensures a realistic spread across all 17 categories while maintaining consistency with the academic taxonomy.
