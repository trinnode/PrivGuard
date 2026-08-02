# PrivGuard Architecture

## Component Diagram

```mermaid
graph TD
    Client[Browser] -->|HTTP| Nginx[Gunicorn/Nginx]
    Nginx --> Django[Django Application]
    
    subgraph Django Apps
        Accounts[Accounts App]
        Incidents[Incidents App]
        Resources[Resources App]
        Reporting[Reporting App]
        Dashboard[Dashboard App]
    end
    
    Django --> DB[(PostgreSQL)]
    Django --> FS[File System / Media]
    Django --> SMTP[Email Service]
    
    Accounts --> User[User Model]
    Incidents --> Incident[Incident Model]
    Incidents --> Harm[Harm Model]
    Incidents --> Audit[Audit Log]
    Resources --> Resource[Resource Model]
    Reporting --> PDF[ReportLab PDF]
    Dashboard --> Stats[Aggregation]
    
    User --> Incidents
    Incident --> Harm
```

## Database Schema

```mermaid
erDiagram
    User ||--o{ Incident : reports
    Incident ||--o{ Harm : classifies
    User ||--o{ AuditLog : triggers
    
    User {
        int id PK
        string email UK
        string password
        string full_name
        string role
        string institution
        bool consent_granted
        datetime consent_date
        datetime date_joined
    }
    
    Incident {
        int id PK
        int user_id FK
        string reference_code UK
        string platform_category
        string platform_name
        date date_of_occurrence
        string incident_classification
        text narrative
        string actor_involvement
        string actor_description
        int severity_rating
        file evidence_file
        bool is_anonymous
        datetime created_at
    }
    
    Harm {
        int id PK
        int incident_id FK
        string harm_category
        int severity_score
        string duration
        text elaboration
    }
    
    Resource {
        int id PK
        string title
        string category
        text description
        string external_link
        string relevance_tags
        bool is_visible
        int order
    }
    
    AuditLog {
        int id PK
        string event_type
        datetime timestamp
        int user_id FK
        text action_summary
        string ip_hash
    }
```

## Security Architecture

- **Authentication:** Django session-based with Argon2 password hashing
- **Session:** 15-minute inactivity timeout, httpOnly + Secure + SameSite Strict cookies
- **CSRF:** Django middleware with httpOnly cookie
- **File Upload:** Type validation (PNG/JPEG/PDF), 5MB max, stored outside web root
- **Audit:** SHA-256 IP hashing, event classification, tamper-evident logging
- **HTTPS:** Enforced via middleware, TLS required in production
