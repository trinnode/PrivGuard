# Project Report Corrections

Reference: `RAGNER FYB PROJECT COMPLETE.md`

Below is every text change to make, ordered **from the abstract to the end**.
Each item gives: **where to go** (page/section + exact old text), **what to replace with** (new text).
Skip the embedded base-64 images, only prose is revised.

---

## 1. DECLARATION (Line 33)

**Where:**
```
RAGNER

\[Matriculation Number\]
```
**Replace with:**
```
FWANSHACK, EMMANUEL

2021/1/COMPLETE
```

---

## 2. CERTIFICATION (Line 43)

**Where:**
> …by: **RAGNER, \[Other Names\]**, (**\[Registration Number\])**, meets the…

**Replace with:**
> …by: **FWANSHACK, EMMANUEL**, (2021/1/COMPLETE), meets the…

---

## 3. ABSTRACT (Line 70)

**Where:**
> …comprising literature review, empirical data collection from **250 students** aged 18 to 30, system design and implementation using Python Django and PostgreSQL, and usability evaluation with **240-250 participants**.

**Replace with:**
> …comprising literature review, empirical data collection from **254 students** aged 18 to 30, system design and implementation using Python Django and PostgreSQL, and usability evaluation with **20 participants**.

**Where (same paragraph):**
> …The functional prototype enables structured incident documentation, harm classification, and access to context appropriate guidance.

**Replace with:**
> …The functional prototype enables structured incident documentation, harm classification, per-incident identity concealment with admin approval, evidence upload via UploadThing, and access to a context appropriate guidance resource library.

---

## 4. CHAPTER ONE, 1.1 Background / 1.3 / 1.6 (Lines 273-279, 316-329, 319-335)

**Where (Line 279, last paragraph of 1.1):**
> …This project responds to these gaps by developing a web based Privacy Incident Reporting System integrated with an adapted sociotechnical taxonomy of lived privacy harms tailored for Nigerian university students.

**Replace with:**
> …This project, rebranded as **PrivGuard**, responds to these gaps by developing a web based Privacy Incident Reporting System integrated with an adapted sociotechnical taxonomy of lived privacy harms tailored for Nigerian university students. All system-generated reference codes now use the prefix `PRG-`.

---

## 5. CHAPTER THREE, 3.5.2 Database Design / Taxonomy (Lines 520-553)

**Where (Line 520):**
> The Harm entity maintains a relationship with the Incident entity, allowing multiple harm classifications per reported incident.

**Replace with:**
> The Harm entity maintains a relationship with the Incident entity, allowing multiple harm classifications per reported incident. The Incident entity also records a `concealment_status` (none / requested / granted / revoked) and an `anonymize_requested` flag used to apply per-report identity concealment after an administrator approves the request.

**Where (Table 3.2, Line 541-553):** the table lists 9 categories, but the live system uses 17 (seeded from 15). Replace the table with the full adapted taxonomy from `incidents/taxonomy.py`:

| **Category Code** | **Harm Category** | **Dimension** |
| --- | --- | --- |
| anxiety | Anxiety | Psychological |
| humiliation | Humiliation | Psychological |
| distress | Psychological Distress | Psychological |
| fear_safety | Fear for Physical Safety | Psychological |
| loss_trust | Loss of Trust | Psychological |
| self_blame | Self-Blame | Psychological |
| isolation | Social Withdrawal | Psychological |
| academic_anxiety | Academic Anxiety | Psychological |
| ptsd_symptoms | Trauma Symptoms | Psychological |
| reputation | Reputation Harm | Tangible |
| academic_penalty | Academic Penalty | Tangible |
| financial_loss | Financial Loss | Tangible |
| lost_opportunity | Lost Opportunity | Tangible |
| social_ostracism | Social Ostracism | Tangible |
| employment_impact | Employment Impact | Tangible |
| physical_safety | Physical Safety Threat | Tangible |
| other_harm | Other Harm | Other |

Then update the in-text "15 categories, 2 domains" claims to read **"17 categories across three dimensions (psychological, tangible, and other; 15 of which are seeded per report)"**:

- Line 812: `Yes (15 categories, 2 domains)` → `Yes (17 categories, 3 dimensions)`
- Line 845: `15 categories, 2 domains (adapted)` → `17 categories, 3 dimensions (adapted)`
- Line 853: `The taxonomy's 15 harm categories across psychological and tangible domains` → `The taxonomy's 17 harm categories across psychological, tangible, and other dimensions`

---

## 6. CHAPTER THREE, 3.5.3 User Interface / 3.6 Technology (Lines 555, 567)

**Where (Line 567):**
> The frontend uses HTML5, CSS3 with a custom design system…

**Add after it:**
> The application is deployed on Vercel using a PostgreSQL (Neon) serverless database. Evidence files larger than 100 KB are rejected; uploads are stored via UploadThing when a token is configured, otherwise to local MEDIA_ROOT for development.

---

## 7. CHAPTER THREE, 3.7.1 Testing Environment Table 3.3 (Line 577)

**Where (the Staging table):**
| **Component** | **Specification** |
|---|---|
| Database | PostgreSQL 16, shared buffer 256 MB |
| ... | ... |

**Replace with:**
| **Component** | **Specification** |
|---|---|
| Application Server | Gunicorn 22.0.0, 3 workers, pre-fork |
| Database | PostgreSQL 16 (Neon serverless pooler) |
| Compute | 2 vCPU, 4 GB RAM |
| Storage | 50 GB SSD |
| Network | 1 Gbps internal, 100 Mbps external |

---

## 8. CHAPTER THREE, 3.8 Security & 3.5.3 (Lines 508-510)

**Where (Line 510):**
> The `MAX_UPLOAD_SIZE` setting (5 MB) and `ALLOWED_UPLOAD_TYPES` whitelist are enforced…

**Replace with:**
> The `MAX_UPLOAD_SIZE` setting (**100 KB**) and `ALLOWED_UPLOAD_TYPES` whitelist (`image/png`, `image/jpeg`, `application/pdf`) are enforced…

---

## 9. CHAPTER FOUR, 4.3.3 Dashboard (Line 673)

**Where:**
> The dashboard presents statistic cards displaying total incidents, psychological harm counts, and tangible harm counts.

**Replace with:**
> The dashboard presents statistic cards displaying total incidents, psychological harm counts, and tangible harm counts, plus a pending-concealment badge for administrators.

---

## 10. CHAPTER FOUR, 4.3.4 Resource Library (Lines 680-681)

**Where:**
> The resource library displays curated guidance materials organised by category. The interface provides category filtering, full text search, and a responsive card grid layout. Each resource card displays the category badge, title, description, and action buttons for external links.

**Replace with:**
> The resource library displays **27 curated support resources** organised by category (legal rights, mental health, digital safety, academic support, campus resources, emergency contacts). The interface provides category filtering, full text search, and a responsive card grid layout. Each resource card displays the category badge, title, description, a displayed contact phone number, and action buttons for external links. **Incident detail pages show a recommended-support panel of up to four resources** matched to that incident's classification and harm categories.

---

## 11. CHAPTER FOUR, 4.3.2 Incident Reporting (Line 661) + 4.3.1 (Line 653)

**Where (Line 653):**
> …The authentication system enforces strict password policies and implements session timeout mechanisms to protect user accounts.

**Replace with:**
> …The authentication system enforces strict password policies, implements 15-minute session timeout enforcement, and supports per incident identity concealment. Concealment requests are set to `requested` on submission and only redact reporter identity in exported PDFs after an administrator grants the request.

**Where (Line 661):**
> The first step captures platform details and incident classification. The second step presents the narrative text area and the harm classification interface with interactive cards organised by dimension. The third step handles evidence upload and anonymous submission preferences.

**Replace with:**
> The first step captures platform details and incident classification. The second step presents the narrative text area and the harm classification interface with interactive cards organised by dimension. The third step handles evidence upload (via UploadThing or local storage) and anonymous submission preferences, including an optional identity-concealment request that is pending administrator approval.

---

## 12. CHAPTER FOUR, 4.5.4 Comparisons / Tables 4.5 & 4.6 (Lines 809-827, 845)

All rows that name the system as **Mamoru** must become **PrivGuard**. Specifically:

- Line 809: `| **Feature / Capability** | **Mamoru** | …` → `| **Feature / Capability** | **PrivGuard** | …`
- Line 828: `…Mamoru occupies a distinct niche…` → `…PrivGuard occupies a distinct niche…`
- Line 830: `…the Mamoru system…` → `…the PrivGuard system…`
- Line 832: `…the Mamoru system in terms of…` → `…the PrivGuard system in terms of…`
- Line 845: `| **Mamoru (This Study)** | …` → `| **PrivGuard (This Study)** | …`
- Line 851: `…Mamoru (this study)…` → `…PrivGuard (this study)…`
- Line 853: `…Mamoru is the first system…` → `…PrivGuard is the first system…`
- Line 855/857/859: `Mamoru` → `PrivGuard`
- Line 869: `Mamoru's admin interface` → `PrivGuard's admin interface`
- Line 871: `Mamoru operates as a standalone system` → `PrivGuard operates as a standalone system`
- Line 873: `the current architecture supports up to 50 concurrent users` stays (this study used Locust)
- Line 881: two more occurrences of `Mamoru` → `PrivGuard`

In the comparison tables (Table 4.5), replace every **Mamoru** header cell with **PrivGuard** (lines 809, 828, 830, 832, 851, 853, 855, 857, 859, 869, 871, 873, and the two in 881). Also update Table 4.6:

- Line 845 `| **Mamoru (This Study)** | … | 377 survey + 20 usability participants | … 15 categories, 2 domains (adapted) |` → `| **PrivGuard (This Study)** | … | 254 incident reports + 20 usability participants | … 17 categories, 3 dimensions (adapted) |`

In the comparison tables, update the **Privacy incident focus** row, the **Digital privacy harm taxonomy** row to read `Yes (15 categories, 2 domains)` (it already says 15 categories, keep), and the **No API Integrations** row to reflect the new local resource library:

- Add a row under Table 4.5 features:
  `| **Local support resource library** | Yes (27 Nigerian orgs) | No | No | No | No |`

---

## 13. CHAPTER FIVE, 5.1 / 5.2 (Lines 889-893)

**Where (Line 893):**
> …The system implements anonymous submission, identity concealment, structured report export, and comprehensive audit logging.

**Replace with:**
> …The system implements anonymous submission, admin-approved identity concealment, UploadThing evidence storage, structured PDF report export, a 27-organization Nigerian support resource library with incident-matched recommendations, and comprehensive audit logging.

---

## 14. CHAPTER FIVE, 5.3 Recommendations (Line 903-907)

**Where (around Line 903, recommendation #5):**
> **5\. Database Connection Pooling:** The current architecture experienced connection timeouts…

**Add a new recommendation before #5:**
> **5\. Serverless Storage for Evidence:** Evidence uploads are stored via UploadThing on the Vercel deployment to keep serverless functions stateless and respect the 100 KB cap per file. Local MEDIA_ROOT is retained only for development.

---

## 15. References / citations

No reference-text changes are required. The bibliography stays as is; only the in-text callouts to "Mamoru" inside the report body are renamed to "PrivGuard" (covers the remaining three in-text mentions in Chapter 5 and the Figure 4.6 / Section 3.12 callouts).

---

## Quick verification checklist

After applying the above:

- [ ] `grep -c "Mamoru" "RAGNER FYB PROJECT COMPLETE.md"` returns **0**
- [ ] Abstract sample figures read **254 students** and **20 usability participants**
- [ ] `MAX_UPLOAD_SIZE` discussion reads **100 KB**
- [ ] Hide/show: 27 Nigerian resources + recommended-support panel mentioned
- [ ] Per-incident concealment described as **requested → admin grant/deny → active**
- [ ] Reference-code prefix stated as **`PRG-`**

