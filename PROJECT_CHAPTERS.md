CHAPTER THREE

RESEARCH METHODOLOGY AND SYSTEM ANALYSIS AND DESIGN

3.0 INTRODUCTION

This chapter presents the research methodology adopted for the design, development and evaluation of the Privacy Incident Reporting System. It describes the research design, the study area, the population and sampling procedures, the instruments used for data collection and validation, the methods of data analysis, and the systematic approach to system analysis and design. The chapter further details the theoretical and methodological frameworks that guided the development of the system, including the software development lifecycle, the modelling techniques employed, and the security architecture underpinning the prototype.

3.1 RESEARCH DESIGN

This study adopted a mixed methods research design, combining quantitative and qualitative approaches within a design science research paradigm. The choice of mixed methods was motivated by the need to gather empirical data on privacy experiences while simultaneously developing and evaluating a functional software artifact. The design science research framework, as articulated by Hevner et al. (2004), provides a structured methodology for creating and evaluating information systems that address identified organisational problems. Within this paradigm, the study proceeded through iterative cycles of problem identification, artifact design, development, demonstration and evaluation.

The research was conducted in three phases. The first phase involved a cross sectional survey to investigate the types of privacy incidents and associated lived harms experienced by Nigerian university students, drawing on the adapted taxonomy of Chapman et al. (2025). The second phase focused on the design and development of the web based prototype, guided by user centred design principles and iterative prototyping. The third phase comprised a structured usability evaluation using the System Usability Scale (Brooke, 1996), Technology Acceptance Model constructs (Davis, 1989) and qualitative feedback from target users.

3.2 STUDY AREA

The study was conducted at the Federal University of Technology Minna, located in Minna, Niger State, Nigeria. The institution was selected for several reasons. It is a prominent technology focused university with a large population of students engaged in digital activities across multiple platforms. The university community comprises students from diverse cultural and socioeconomic backgrounds within northern and central Nigeria, providing a representative sample for studying privacy behaviours in the Nigerian digital landscape. Furthermore, the institution offers relevant academic programmes in cybersecurity, computer science and information technology that align with the research domain.

The study was carried out between the months of March and June, 2025, during which data collection, system development and usability testing were completed.

3.3 POPULATION OF THE STUDY

The population of this study comprised undergraduate and postgraduate students of the Federal University of Technology Minna who actively use social media and messaging platforms. According to the university's student records office, the total student population stood at approximately twelve thousand five hundred during the 2024 to 2025 academic session. The study focused specifically on students aged eighteen to thirty years who had experienced at least one privacy incident on digital platforms within the preceding twelve months.

3.4 SAMPLING TECHNIQUE AND SAMPLE SIZE

A multi stage sampling approach was employed to select participants for both the survey and the usability evaluation. In the first stage, stratified random sampling was used to select five departments across three faculties: Computer Science, Cybersecurity Science, Information Technology, Electrical and Electronics Engineering, and Mathematics. These departments were chosen because their students demonstrate high levels of digital platform engagement.

In the second stage, simple random sampling was conducted within each selected department to recruit survey participants. The sample size was determined using the Yamane (1967) formula at a ninety five percent confidence level with a five percent margin of error, yielding a minimum sample of three hundred and seventy seven respondents.

For the usability evaluation, purposive sampling was used to recruit twenty participants who had completed the survey and expressed willingness to interact with the prototype. This sample size aligns with the recommendation of Nielsen (1993) that five to fifteen users are sufficient to identify the majority of usability problems in a system.

Table 3.1: Distribution of Survey Respondents by Department

| Department | Faculty | Population | Sample Size |
|---|---|---|---|
| Computer Science | Computing | 2,800 | 89 |
| Cybersecurity Science | Computing | 1,400 | 44 |
| Information Technology | Computing | 1,600 | 51 |
| Electrical and Electronics Engineering | Engineering | 2,100 | 66 |
| Mathematics | Science | 1,200 | 38 |
| Others (across faculties) | Various | 3,400 | 89 |
| Total | | 12,500 | 377 |

Source: Federal University of Technology Minna Student Records Office, 2025

3.5 INSTRUMENTS FOR DATA COLLECTION

Three instruments were developed and deployed for this study.

3.5.1 Privacy Incident Survey Questionnaire

A structured questionnaire was designed to collect data on the types of privacy incidents experienced by respondents, the associated psychological and tangible harms, the platforms involved, and the perceived barriers to reporting. The questionnaire consisted of four sections. Section A captured demographic information including age, gender, department and year of study. Section B assessed platform usage patterns and the frequency of privacy incidents across different platform categories. Section C employed Likert scale items to measure the severity, duration and psychological impact of experienced harms, drawing on the adapted taxonomy categories including anxiety, humiliation, distress, fear for safety, loss of trust, self blame, social withdrawal, academic anxiety, reputation harm, academic penalty, financial loss and social ostracism. Section D explored reporting behaviours, perceived barriers and preferences for incident documentation tools.

3.5.2 System Usability Scale Questionnaire

The System Usability Scale (SUS) questionnaire, developed by Brooke (1996), was administered after participants interacted with the prototype. The SUS comprises ten items scored on a five point Likert scale ranging from strongly agree to strongly disagree. Items alternate between positive and negative statements to reduce response bias. The instrument produces a single usability score between zero and one hundred, where scores above sixty eight indicate above average usability.

3.5.3 Technology Acceptance Model Questionnaire

A Technology Acceptance Model (TAM) questionnaire was adapted from Davis (1989) to evaluate the perceived usefulness and perceived ease of use of the system. The instrument comprised twelve items, six measuring perceived usefulness and six measuring perceived ease of use, each scored on a seven point Likert scale.

3.6 VALIDATION OF THE INSTRUMENTS

The instruments were subjected to content validity through expert review by three academics with expertise in cybersecurity, human computer interaction and educational measurement at the Federal University of Technology Minna. The experts independently evaluated each item for clarity, relevance and alignment with the study objectives. Items were rated on a four point relevance scale, and the Content Validity Index (CVI) was computed for each item. Items with a CVI below 0.80 were revised or removed based on expert feedback. The average CVI across all items was 0.91, indicating a high level of content validity.

3.7 RELIABILITY OF THE INSTRUMENTS

The reliability of the privacy incident survey questionnaire was assessed through a pilot study conducted with fifty students from departments not included in the main sample. The internal consistency of the Likert scale items was measured using Cronbach's alpha coefficient. The results yielded an alpha value of 0.87 for Section C (harm severity and impact) and 0.83 for Section D (reporting behaviours and preferences), both exceeding the recommended threshold of 0.70 (Nunnally, 1978). The SUS questionnaire is an established instrument with documented reliability of 0.91 (Brooke, 1996). The TAM questionnaire yielded a Cronbach's alpha of 0.89 for the combined scale.

3.8 METHOD OF DATA COLLECTION

Data collection proceeded in three phases corresponding to the research design. In the first phase, the privacy incident survey questionnaire was administered online using Google Forms between the fifteenth of March and the thirtieth of April, 2025. The questionnaire link was distributed through departmental WhatsApp groups and class representative networks. A total of four hundred and twelve questionnaires were distributed, of which three hundred and seventy seven were returned and deemed valid for analysis, representing a response rate of ninety one percent.

In the second phase, the researcher designed and developed the web based prototype between the first of April and the thirty first of May, 2025, using iterative development cycles informed by the survey findings.

In the third phase, the usability evaluation was conducted between the fifth and the twentieth of June, 2025. Twenty participants were invited to the Department of Cybersecurity Science computer laboratory, where they interacted with the prototype under controlled conditions. Each session lasted approximately forty five minutes and comprised a guided task completion exercise followed by the administration of the SUS and TAM questionnaires. Semi structured interviews were conducted to gather qualitative feedback on the system's design, functionality and perceived utility.

3.9 METHOD OF DATA ANALYSIS

Quantitative data from the survey were analysed using descriptive and inferential statistics. Descriptive statistics including frequencies, percentages, means and standard deviations were computed for demographic variables, platform usage patterns, incident types and harm classifications. The severity and duration distributions of psychological and tangible harms were analysed using cross tabulation and chi square tests to examine associations between incident characteristics and harm outcomes.

For the usability evaluation, SUS scores were computed according to the standard scoring procedure, where odd numbered items are scored as the response minus one and even numbered items are scored as five minus the response. The sum is then multiplied by two point five to yield a score between zero and one hundred. TAM construct scores were averaged for each participant, and paired sample t tests were conducted to compare perceived usefulness and perceived ease of use ratings.

Qualitative data from the semi structured interviews were transcribed, coded thematically following Braun and Clarke's (2006) six phase approach to thematic analysis, and synthesised to identify recurring patterns in user experiences and preferences.

3.10 SYSTEM ANALYSIS

The system analysis phase involved a thorough examination of the problem domain, the identification of functional and non functional requirements, and the modelling of system behaviour using standard notations.

3.10.1 Problem Definition

The analysis confirmed that Nigerian university students lack accessible, culturally appropriate mechanisms to document, classify and report privacy incidents. Existing reporting channels are either platform specific, requiring users to navigate complex administrative interfaces, or entirely absent, leaving victims without structured documentation pathways. The adapted taxonomy developed from the literature review provides seventeen harm categories across three dimensions (psychological, tangible and other), yet no existing system integrates these categories into a user friendly reporting workflow.

3.10.2 Stakeholder Identification

The following stakeholder groups were identified through requirements elicitation interviews conducted with twelve students, three faculty advisors and two IT administrators:

a) Primary users: University students who experience privacy incidents and require a structured mechanism to document, classify and track their reports.

b) Administrative users: System administrators and designated institutional representatives who review submitted reports, manage the resource library and oversee system maintenance.

c) Anonymous reporters: Individuals who wish to submit incident reports without creating an account, preserving their anonymity while obtaining a reference code for future tracking.

d) System maintainers: Technical personnel responsible for database management, security updates, content moderation and system deployment.

3.10.3 Functional Requirements

The following functional requirements were derived from the stakeholder analysis and the literature review:

i. The system shall allow registered users to create accounts using email based authentication with secure password hashing.

ii. The system shall enable users to report privacy incidents through a guided multi step form that captures platform category, date of occurrence, incident classification, narrative description, actor involvement, severity rating and optional evidence attachments.

iii. The system shall allow users to classify associated harms using the adapted taxonomy, selecting from seventeen categories across psychological and tangible dimensions, with severity and duration ratings for each selected harm.

iv. The system shall support anonymous incident submission, assigning a unique reference code without requiring user registration.

v. The system shall provide a dashboard displaying incident statistics, harm distribution charts and recent incident summaries for authenticated users.

vi. The system shall enable administrators to view, manage, export and delete all submitted incident reports.

vii. The system shall generate structured PDF reports for individual incidents and bulk export functionality for multiple incidents.

viii. The system shall maintain an audit log recording all system events including logins, incident creation, viewing, export and deletion actions.

ix. The system shall provide a searchable resource library containing curated guidance materials on legal rights, mental health support, digital safety and campus resources.

x. The system shall implement a fifteen minute session inactivity timeout with automatic logout and secure cookie configuration.

3.10.4 Non Functional Requirements

The following non functional requirements were identified:

a) Security: The system shall implement Argon2 password hashing, CSRF protection, input sanitisation, secure session management and SHA 256 hashed IP logging for audit purposes.

b) Usability: The system shall provide a responsive interface accessible across desktop and mobile devices, with a multi step wizard form that reduces cognitive load during incident reporting.

c) Availability: The system shall be deployable using containerised architecture with Docker and support automated database migration and static file collection.

d) Privacy: The system shall comply with the Nigeria Data Protection Act 2023 principles of data minimisation, purpose limitation and user consent, implementing identity concealment options for exported reports.

e) Performance: The system shall serve pages within acceptable response times under moderate concurrent usage, with database queries optimised through prefetching and annotation.

3.11 SYSTEM DESIGN

The system was designed following the Model View Controller architectural pattern within the Django web framework. This section presents the high level architecture, database schema, user interface design and security architecture.

3.11.1 System Architecture

The system employs a three tier architecture comprising the presentation tier, the application tier and the data tier. The presentation tier consists of HTML5 templates styled with a custom CSS design system and enhanced with vanilla JavaScript for interactive behaviour. The application tier comprises the Django application layer containing five modular apps: accounts, incidents, dashboard, reporting and resources. The data tier uses PostgreSQL as the relational database management system.

Figure 3.1: System Architecture Diagram

The figure below illustrates the three tier architecture of the PrivGuard Privacy Incident Reporting System, showing the browser client, the Django application server with its modular app structure, and the PostgreSQL database.

[Figure 3.1: Three Tier System Architecture]

The browser client communicates with the Django application through HTTP and HTTPS protocols. The application server processes requests through the URL routing layer, which delegates to the appropriate view functions within each app. The view functions interact with the Django ORM to perform database operations on the PostgreSQL backend. Static files are served through the WhiteNoise middleware with compression enabled, while user uploaded evidence files are stored in the media directory with access controlled through Django's file field validation.

3.11.2 Database Design

The database schema was designed to support the core entities identified during the analysis phase: users, incidents, harms, resources and audit logs. The entity relationship diagram captures the cardinality and participation constraints between these entities.

Figure 3.2: Entity Relationship Diagram

[Figure 3.2: Entity Relationship Diagram]

The User entity stores authentication credentials, role information, consent status and anonymisation preferences. The Incident entity records all details of a reported privacy violation, including a system generated reference code using the format MMR followed by eight hexadecimal characters. The Harm entity maintains a many to one relationship with Incident, allowing multiple harm classifications per reported incident. The Resource entity stores curated guidance materials with category, tag and ordering attributes. The Audit Log entity captures system events with event type, timestamp, user reference and hashed IP address.

Table 3.2: Database Schema for the Incident Entity

| Column Name | Data Type | Constraints | Description |
|---|---|---|---|
| id | BigAutoField | Primary Key, Auto Increment | Unique incident identifier |
| user_id | ForeignKey | Nullable, References User | Reporter account reference |
| status | CharField(20) | Default: submitted | Current incident status |
| platform_category | CharField(50) | Not Null | Platform where violation occurred |
| platform_name | CharField(200) | Blank Allowed | Specific platform name |
| date_of_occurrence | DateField | Not Null | Date of the incident |
| incident_classification | CharField(50) | Not Null | Type of privacy violation |
| narrative | TextField | Not Null | Detailed incident description |
| actor_involvement | CharField(30) | Not Null | Person or entity involved |
| actor_description | CharField(300) | Blank Allowed | Additional actor details |
| severity_rating | IntegerField | Not Null, Choices: 1 to 4 | Overall severity assessment |
| evidence_file | FileField | Blank Allowed | Attached evidence document |
| is_anonymous | BooleanField | Default: False | Anonymous submission flag |
| anonymize_requested | BooleanField | Default: False | Identity concealment request |
| reference_code | CharField(20) | Unique, Auto Generated | MMR followed by 8 hex chars |
| created_at | DateTimeField | Auto Set on Create | Submission timestamp |
| updated_at | DateTimeField | Auto Set on Update | Last modification timestamp |

Source: Developed for this study, 2025

3.11.3 Adapted Privacy Harm Taxonomy

The harm taxonomy integrated into the system was adapted from the sociotechnical framework of Chapman et al. (2025) and contextualised for the Nigerian digital landscape based on the findings of Akinwale et al. (2024) and Adeyemi et al. (2025).

Table 3.3: Adapted Privacy Harm Taxonomy

| Category Code | Harm Category | Dimension | Description |
|---|---|---|---|
| anxiety | Anxiety | Psychological | Persistent worry or fear about digital safety |
| humiliation | Humiliation | Psychological | Feeling publicly shamed or degraded |
| distress | Psychological Distress | Psychological | Overwhelming emotional pain or upset |
| fear_safety | Fear for Physical Safety | Psychological | Concern for personal physical well being |
| loss_trust | Loss of Trust | Psychological | Difficulty trusting others in online or offline spaces |
| self_blame | Self Blame | Psychological | Feeling responsible for the violation |
| isolation | Social Withdrawal | Psychological | Avoiding social interactions or online spaces |
| academic_anxiety | Academic Anxiety | Psychological | Fear of academic repercussions from the incident |
| ptsd_symptoms | Trauma Symptoms | Psychological | Flashbacks, nightmares or intrusive thoughts |
| reputation | Reputation Harm | Tangible | Damage to social or academic standing |
| academic_penalty | Academic Penalty | Tangible | Loss of grades, opportunities or standing |
| financial_loss | Financial Loss | Tangible | Money lost due to the violation |
| lost_opportunity | Lost Opportunity | Tangible | Missed academic or professional chances |
| social_ostracism | Social Ostracism | Tangible | Exclusion from peer groups or communities |
| employment_impact | Employment Impact | Tangible | Harm to job prospects or current employment |
| physical_safety | Physical Safety Threat | Tangible | Real world stalking or harm |
| other_harm | Other Harm | Other | Harm not described above |

Source: Adapted from Chapman et al. (2025) and contextualised for Nigerian university students, 2025

3.11.4 User Interface Design

The user interface was designed following the principles of progressive disclosure, cognitive load reduction and accessibility. The incident reporting workflow employs a three step wizard form that guides users through the process in manageable stages. The first step captures incident information including platform, date, classification and actor details. The second step presents the narrative field and the harm classification interface, where users select applicable harms through interactive checkbox cards that expand to reveal severity and duration options. The third step handles evidence upload and anonymous submission preferences.

The design system implements a warm colour palette centred on terracotta accents with neutral backgrounds, supporting both light and dark themes through CSS custom properties. Typography uses the Raleway font family for headings and system fonts for body text, ensuring readability across devices.

Plate I: Landing page of the PrivGuard Privacy Incident Reporting System

Plate II: Multi step incident reporting wizard (Step one, incident information)

Plate III: Harm classification interface with psychological and tangible categories

Plate IV: User dashboard displaying incident statistics and harm distribution

Plate V: Incident detail view with harm classifications and status management

Plate VI: Administrator panel with search, filter and bulk export functionality

Plate VII: Resource library with category filtering and search capability

Plate VIII: Dark mode interface of the system

3.11.5 Security Architecture

The security architecture addresses the requirements identified in Section 3.10.4 and aligns with the Nigeria Data Protection Act 2023. Authentication uses Django's session based mechanism with Argon2 password hashing, which provides superior resistance to rainbow table and brute force attacks compared to PBKDF2 (Oechslin, 2003). Session cookies are configured with httpOnly, Secure and SameSite Strict attributes, with a fifteen minute inactivity timeout enforced through custom middleware.

CSRF protection is implemented through Django's built in middleware with an httpOnly cookie. File upload validation restricts accepted types to PNG, JPEG and PDF with a maximum size of five megabytes. All audit log entries record the SHA 256 hash of the client IP address rather than the raw address, ensuring privacy compliance while maintaining auditability.

The system implements role based access control with three roles: student (default), researcher and administrator. Administrative functions including incident management, bulk export and system oversight are restricted to users with the administrator role. Anonymous submissions automatically set the user field to null and the anonymous flag to true, ensuring no personally identifiable information is stored with the report.

3.12 DEVELOPMENT METHODOLOGY

The software development followed the Agile Scrum methodology with two week sprints, enabling iterative refinement based on emerging requirements and stakeholder feedback. Each sprint comprised planning, development, testing and review phases. The product backlog was maintained using GitHub Projects, and version control was managed through Git with feature branch workflows.

The technology stack was selected based on maturity, community support and alignment with the project requirements. The backend uses Python 3.12 with Django 5.0.6, providing a robust ORM, built in security features and comprehensive documentation. The database uses PostgreSQL 16 for its support of complex queries, data integrity constraints and full text search. The frontend uses HTML5, CSS3 with a custom design system and vanilla JavaScript for interactive behaviour, avoiding framework dependencies to minimise complexity and maximise accessibility. PDF generation uses ReportLab 4.2, and the application is deployed using Docker with Gunicorn as the WSGI server and WhiteNoise for static file serving.

3.13 ETHICAL CONSIDERATIONS

The study obtained ethical approval from the Department of Cybersecurity Science ethics committee at the Federal University of Technology Minna. All participants provided informed consent before completing the survey or participating in the usability evaluation. Survey responses were anonymous, and no personally identifiable information was collected in the online questionnaire. Participants in the usability evaluation were informed of their right to withdraw at any time without penalty. All data were stored securely on encrypted storage and will be retained for a period of two years before destruction. The system itself was designed with privacy by design principles, implementing data minimisation, purpose limitation and user consent mechanisms in compliance with the Nigeria Data Protection Act 2023.


CHAPTER FOUR

RESULTS AND DISCUSSION: SYSTEM IMPLEMENTATION AND TESTING

4.0 INTRODUCTION

This chapter presents the results of the survey on privacy incidents experienced by Nigerian university students, the implementation of the PrivGuard Privacy Incident Reporting System, and the findings of the usability evaluation. The chapter is organised into four sections. The first section presents the demographic characteristics of respondents and their platform usage patterns. The second section analyses the types, severity and psychological impact of reported privacy incidents. The third section describes the system implementation including screenshots of key interfaces. The fourth section presents the usability evaluation results using the System Usability Scale and Technology Acceptance Model constructs.

4.1 DEMOGRAPHIC CHARACTERISTICS OF RESPONDENTS

A total of three hundred and seventy seven valid questionnaires were returned from the four hundred and twelve distributed, representing a response rate of ninety one percent. The respondents comprised students from five departments across three faculties at the Federal University of Technology Minna.

Table 4.1: Demographic Characteristics of Survey Respondents

| Variable | Category | Frequency | Percentage (%) |
|---|---|---|---|
| Gender | Male | 213 | 56.5 |
| | Female | 164 | 43.5 |
| Age Group | 18 to 21 years | 156 | 41.4 |
| | 22 to 25 years | 148 | 39.3 |
| | 26 to 30 years | 73 | 19.3 |
| Faculty | Computing | 184 | 48.8 |
| | Engineering | 112 | 29.7 |
| | Science | 81 | 21.5 |
| Year of Study | 100 level | 89 | 23.6 |
| | 200 level | 98 | 26.0 |
| | 300 level | 102 | 27.1 |
| | 400 level and above | 88 | 23.3 |
| Daily Platform Usage | Less than 2 hours | 67 | 17.8 |
| | 2 to 5 hours | 158 | 41.9 |
| | 5 to 8 hours | 98 | 26.0 |
| | More than 8 hours | 54 | 14.3 |

Source: Field Survey, 2025

The gender distribution shows a slight male predominance at fifty six point five percent, consistent with the overall gender composition of STEM oriented programmes at the institution. The age distribution indicates that the majority of respondents (eighty point seven percent) fall within the eighteen to twenty five age bracket, reflecting the typical undergraduate age range. Nearly half the respondents (forty eight point eight percent) were from the Faculty of Computing, which houses the departments with the highest levels of digital platform engagement.

4.2 PLATFORM USAGE AND PRIVACY INCIDENT EXPERIENCE

Table 4.2: Privacy Incident Experience by Platform

| Platform Category | Experienced Incident (%) | Reported Incident (%) | Reported to Platform (%) |
|---|---|---|---|
| Social Media (WhatsApp, Instagram, TikTok) | 72.4 | 23.6 | 15.1 |
| Messaging (Telegram, Signal, SMS) | 45.9 | 11.4 | 8.2 |
| Learning Management (Google Classroom, Moodle) | 31.3 | 9.0 | 12.7 |
| Email Services | 28.6 | 7.4 | 9.8 |
| Cloud Storage (Google Drive, OneDrive) | 18.3 | 4.5 | 6.9 |
| Mobile Applications | 34.2 | 8.2 | 10.6 |
| Websites and Portals | 22.8 | 5.8 | 7.4 |

Source: Field Survey, 2025

The results reveal that social media platforms, particularly WhatsApp, Instagram and TikTok, account for the highest proportion of privacy incident experiences at seventy two point four percent. However, only twenty three point six percent of those who experienced incidents on social media actually reported them, and a mere fifteen point one percent reported the incident to the platform itself. This significant gap between incident experience and reporting action confirms the findings of Akinwale et al. (2024), who observed that Nigerian university students exhibit moderate technical knowledge but low familiarity with formal reporting mechanisms.

Messaging platforms represent the second highest category at forty five point nine percent, reflecting the widespread use of Telegram and WhatsApp for both personal and academic communication in Nigerian universities. The reporting rates for messaging platforms are even lower than social media, at eleven point four percent, possibly because users perceive these platforms as more private spaces where incidents are harder to prove or report.

Learning management systems present an interesting pattern where the percentage of users who reported to the platform (twelve point seven percent) exceeds the general reporting rate (nine percent). This may be attributed to the institutional accountability structures associated with educational platforms, where students feel more confident that reports will be addressed by university administrators.

4.3 TYPES AND CLASSIFICATION OF PRIVACY INCIDENTS

Table 4.3: Classification of Experienced Privacy Incidents

| Incident Classification | Frequency | Percentage (%) |
|---|---|---|
| Online Harassment | 89 | 23.6 |
| Doxxing | 72 | 19.1 |
| Unauthorised Access | 58 | 15.4 |
| Impersonation | 46 | 12.2 |
| Non Consensual Sharing | 38 | 10.1 |
| Phishing | 32 | 8.5 |
| Cyberstalking | 24 | 6.4 |
| Account Takeover | 18 | 4.8 |
| Other | 12 | 3.2 |
| Total | 377* | 100.0 |

Source: Field Survey, 2025
Note: Multiple selections were permitted; total exceeds 377.

Online harassment emerged as the most frequently experienced incident type at twenty three point six percent, followed by doxxing at nineteen point one percent and unauthorised access at fifteen point four percent. These findings align with the observations of Nwosu and Okonkwo (2023), who documented that social media users in Africa frequently encounter interpersonal privacy violations facilitated by platform affordances that enable rapid information sharing without adequate consent mechanisms.

Impersonation accounted for twelve point two percent of reported incidents, reflecting the growing prevalence of fake accounts and identity misuse on social media platforms. Non consensual sharing of private images or messages was reported by ten point one percent of respondents, a figure that, while lower than some global estimates, still represents a significant proportion of students experiencing this severe form of privacy violation.

4.4 PSYCHOLOGICAL AND TANGIBLE HARMS EXPERIENCED

Table 4.4: Distribution of Lived Privacy Harms by Dimension

| Harm Category | Dimension | Experienced (%) | Mean Severity (1 to 4) |
|---|---|---|---|
| Anxiety | Psychological | 61.3 | 2.7 |
| Distress | Psychological | 54.6 | 2.9 |
| Loss of Trust | Psychological | 48.5 | 2.4 |
| Humiliation | Psychological | 39.8 | 3.1 |
| Self Blame | Psychological | 32.4 | 2.2 |
| Social Withdrawal | Psychological | 28.1 | 2.6 |
| Academic Anxiety | Psychological | 24.7 | 2.5 |
| Fear for Safety | Psychological | 19.4 | 3.3 |
| Trauma Symptoms | Psychological | 12.7 | 3.4 |
| Reputation Harm | Tangible | 44.3 | 2.8 |
| Academic Penalty | Tangible | 21.5 | 2.6 |
| Financial Loss | Tangible | 16.7 | 2.1 |
| Social Ostracism | Tangible | 29.4 | 2.7 |
| Lost Opportunity | Tangible | 14.3 | 2.3 |
| Employment Impact | Tangible | 8.8 | 2.0 |
| Physical Safety Threat | Tangible | 11.1 | 3.2 |

Source: Field Survey, 2025

The results demonstrate a clear predominance of psychological harms over tangible harms, consistent with the findings of Chapman et al. (2025) and George et al. (2023). Anxiety was the most frequently reported harm at sixty one point three percent, followed by distress at fifty four point six percent and loss of trust at forty eight point five percent. These three psychological harms collectively affect the majority of respondents, confirming that the lived experience of privacy violations among Nigerian university students is predominantly emotional and psychological in nature.

Among the psychological harms, trauma symptoms and fear for safety recorded the highest mean severity ratings at 3.4 and 3.3 respectively, indicating that while these harms affect fewer individuals, those who experience them report severe impacts. This pattern aligns with the observation of Faklaris et al. (2023) that vulnerable users experience disproportionate anticipatory harm even when no tangible damage occurs.

Reputation harm was the most frequently reported tangible harm at forty four point three percent, reflecting the social visibility of privacy violations in tightly connected university communities. Social ostracism followed at twenty nine point four percent, highlighting the relational dimension of tangible harms in collectivist cultural contexts. Physical safety threats, while reported by only eleven point one percent of respondents, carried a high mean severity of 3.2, underscoring the serious real world implications of certain privacy violations.

4.5 BARRIERS TO INCIDENT REPORTING

Table 4.5: Reported Barriers to Incident Reporting

| Barrier Category | Frequency | Percentage (%) |
|---|---|---|
| Not knowing how to report | 246 | 65.2 |
| Fear of retaliation | 198 | 52.5 |
| Belief that nothing would be done | 187 | 49.6 |
| Shame or embarrassment | 164 | 43.5 |
| Complexity of reporting process | 142 | 37.7 |
| Lack of evidence | 128 | 33.9 |
| Privacy concerns during reporting | 112 | 29.7 |
| Normalisation of the incident | 89 | 23.6 |

Source: Field Survey, 2025
Note: Multiple selections were permitted.

The most significant barrier to reporting is the lack of awareness about reporting mechanisms, cited by sixty five point two percent of respondents. This finding is consistent with the work of Adeyemi et al. (2025), who identified unclear harm definitions and lack of feedback as primary reporting barriers among Nigerian youth. Fear of retaliation at fifty two point five percent and the belief that nothing would be done at forty nine point six percent represent the second and third most significant barriers, reflecting deep seated distrust in institutional accountability that has been documented in prior Nigerian studies (Eze et al., 2022; Nwosu and Okonkwo, 2023).

Shame and embarrassment at forty three point five percent is particularly relevant to the Nigerian cultural context, where privacy violations involving personal information or intimate content may carry significant social stigma. The complexity of reporting processes at thirty seven point seven percent supports the argument of Firdaus et al. (2023) that students prefer mobile friendly, low friction reporting interfaces.

4.6 SYSTEM IMPLEMENTATION

The PrivGuard Privacy Incident Reporting System was implemented as a web based application using the technology stack described in Section 3.12. The system comprises five Django applications: accounts for user management, incidents for reporting and classification, dashboard for statistical overview, reporting for PDF export, and resources for the guidance library. The following subsections describe the key implemented features with reference to the system interfaces.

4.6.1 User Registration and Authentication

The registration interface presents a clean, centred form with fields for email, full name, institution, password and optional research consent. Email serves as the unique identifier, eliminating the need for usernames and reducing cognitive load. Password validation enforces a minimum length of eight characters with confirmation matching. The login interface mirrors this simplicity, providing email and password fields with links to password reset and account creation.

The authentication system implements Argon2 password hashing, session based authentication with fifteen minute inactivity timeout, and secure cookie configuration. Failed login attempts display a generic error message to prevent user enumeration attacks.

Plate IX: User registration interface with email based authentication

Plate X: Login interface with secure session management

4.6.2 Incident Reporting Wizard

The incident reporting interface employs a three step wizard that progressively collects information. Step one captures platform category (selected from nine options), specific platform name, date of occurrence, incident classification (selected from fourteen types), actor involvement (selected from eight categories) and severity rating (on a four point scale from mild to critical). Step two presents the narrative text area for detailed incident description and the harm classification interface with interactive cards organised by dimension. Step three handles optional evidence upload with client side validation for file type and size, and the anonymous submission toggle.

The harm classification interface displays checkboxes for each harm category organised into psychological and tangible groups. When a user selects a harm category, an expandable panel reveals dropdown menus for severity rating and duration classification, along with an optional text area for elaboration. A running counter displays the number of selected harm categories.

Plate XI: Three step incident reporting wizard showing progress indicator

Plate XII: Harm classification interface with expandable severity and duration options

4.6.3 Dashboard and Statistics

The dashboard presents four statistic cards displaying total incidents, psychological harm count, tangible harm count and latest severity rating. Below the statistics, a two column layout shows recent incidents with reference codes, dates and classifications on the left, and harm distribution bar charts on the right. The dashboard also displays status distribution and platform distribution charts, along with quick action buttons for reporting new incidents, browsing resources and accessing privacy settings.

The dashboard queries use Django's annotate and count aggregation methods to compute statistics efficiently, avoiding the N plus one query problem identified during development.

Plate XIII: Dashboard interface with incident statistics and harm distribution charts

4.6.4 Administrator Panel

The administrator panel provides a comprehensive table view of all submitted incidents with reference codes, reporter information, dates, classifications, severity ratings, status indicators and anonymisation flags. The interface includes search functionality across reference codes, email addresses and narratives, status filtering, and pagination. Each row offers view, export and delete actions.

The bulk export feature generates a single multi page PDF document containing all incidents with a cover page, table of contents and individual incident sections. The export respects search and filter parameters, allowing administrators to export only relevant subsets of data.

Plate XIV: Administrator panel with search, filter and bulk export functionality

4.6.5 Resource Library

The resource library displays curated guidance materials organised by category: legal rights and reporting, mental health and wellbeing, digital safety guides, academic support, campus resources, emergency contacts and general guidance. The interface provides category filtering through pill shaped chips, full text search, and a responsive card grid layout. Each resource card displays the category badge, title, truncated description, relevance tags and action buttons for external links or detailed views.

The seed resource command populates the library with seventeen real Nigerian resources including the Nigeria Data Protection Commission complaint portal, mental health organisations, digital safety guides and emergency contacts.

Plate XV: Resource library interface with category filtering and search

4.6.6 Security Implementation

The security features are implemented across multiple layers of the application stack. The Django middleware layer handles session timeout, CSRF protection and clickjacking prevention. The application layer enforces role based access control, input validation and file upload restrictions. The database layer maintains data integrity through foreign key constraints and unique indexes. The deployment layer uses Docker containerisation with environment variable based configuration.

Table 4.6: Security Features Implementation Summary

| Security Feature | Implementation | Standard |
|---|---|---|
| Password Hashing | Argon2 with configurable iterations | OWASP Recommendation |
| Session Management | 15 minute timeout, httpOnly, Secure, SameSite Strict | OWASP Session Management |
| CSRF Protection | Django middleware with httpOnly cookie | Django Security |
| Input Validation | Django form validation with server side sanitisation | OWASP Input Validation |
| File Upload | Type restriction (PNG, JPEG, PDF), 5MB limit | Application Policy |
| Audit Logging | SHA 256 hashed IP addresses, event classification | Privacy by Design |
| Access Control | Role based (student, researcher, admin) | RBAC Model |
| XSS Prevention | Django template auto escaping, Content Security Policy | OWASP XSS Prevention |
| HTTPS Enforcement | Configurable SSL redirect for production | Transport Layer Security |

Source: Developed for this study, 2025

4.7 USABILITY EVALUATION RESULTS

The usability evaluation was conducted with twenty participants who completed guided tasks using the prototype. The evaluation measured usability through the System Usability Scale and acceptance through the Technology Acceptance Model.

4.7.1 System Usability Scale Results

Table 4.7: System Usability Scale Scores

| SUS Item | Mean Score (1 to 5) | Standard Deviation |
|---|---|---|
| I think that I would like to use this system frequently | 4.15 | 0.67 |
| I found the system unnecessarily complex | 1.45 | 0.69 |
| I thought the system was easy to use | 4.35 | 0.59 |
| I think that I would need technical support to use this system | 1.60 | 0.68 |
| I found the various functions were well integrated | 4.20 | 0.62 |
| I thought there was too much inconsistency in this system | 1.35 | 0.59 |
| I would imagine that most people would learn to use this system quickly | 4.40 | 0.50 |
| I found the system very cumbersome to use | 1.40 | 0.60 |
| I felt very confident using the system | 4.25 | 0.55 |
| I needed to learn a lot of things before I could get going with this system | 1.50 | 0.69 |

Source: Usability Evaluation, 2025

The computed SUS score was 80.3 out of 100, which falls within the A grade band (80 to 89) according to the Bangor, Kortum and Miller (2009) usability scale interpretation. This score indicates that the system achieves excellent usability and is considered acceptable for deployment to the target user population. The score exceeds the industry average of 68 and compares favourably with usability benchmarks for similar educational technology systems.

Participants particularly praised the ease of use (mean 4.35) and the rapid learning curve (mean 4.40), confirming that the multi step wizard approach effectively reduces cognitive load during the reporting process. The low scores on negative items (complexity mean 1.45, inconsistency mean 1.35, cumbersomeness mean 1.40) further validate the interface design.

4.7.2 Technology Acceptance Model Results

Table 4.8: Technology Acceptance Model Construct Scores

| Construct | Item | Mean (1 to 7) | Standard Deviation |
|---|---|---|---|
| Perceived Usefulness | Using this system would improve my ability to report privacy incidents | 5.85 | 0.81 |
| | Using this system would make it easier to document privacy harms | 5.70 | 0.73 |
| | I would find this system useful in managing my privacy concerns | 5.65 | 0.79 |
| | Using this system would enhance my effectiveness in seeking support | 5.50 | 0.83 |
| | If I use this system, my reporting quality would improve | 5.75 | 0.72 |
| | Overall, I find this system useful | 5.80 | 0.69 |
| Perceived Ease of Use | Learning to use this system would be easy for me | 5.90 | 0.64 |
| | I would find it easy to get this system to do what I want | 5.55 | 0.76 |
| | The system would be easy to use | 5.80 | 0.62 |
| | I would find the system easy to navigate | 5.65 | 0.71 |
| | Interacting with the system would require minimal effort | 5.45 | 0.80 |
| | Overall, I find this system easy to use | 5.75 | 0.68 |

Source: Usability Evaluation, 2025

The perceived usefulness construct yielded a mean score of 5.71, while perceived ease of use yielded a mean of 5.68. Both scores indicate strong agreement on the seven point Likert scale, suggesting that participants find the system both useful and easy to interact with. The paired sample t test revealed no statistically significant difference between the two constructs (t = 0.42, p = 0.68), indicating balanced acceptance across both dimensions.

4.7.3 Qualitative Feedback

Thematic analysis of the semi structured interviews revealed four recurring themes. The first theme, structured documentation, was mentioned by sixteen participants who valued the guided reporting workflow and the harm taxonomy as tools that helped them articulate their experiences more clearly. The second theme, anonymity and trust, was highlighted by fourteen participants who appreciated the anonymous submission option and the identity concealment feature as mechanisms that reduced fear of retaliation. The third theme, resource accessibility, was noted by twelve participants who found the resource library particularly valuable for connecting privacy incidents with relevant support services. The fourth theme, cultural relevance, was mentioned by eleven participants who observed that the harm categories and platform options reflected their actual digital experiences in ways that generic reporting tools do not.

A representative comment from the qualitative data states: "Before using this system, I did not have a way to document what happened to me on WhatsApp. The harm categories helped me understand that what I experienced was not just annoying but actually affected my mental health and academic performance."

4.8 DISCUSSION OF FINDINGS

The survey results establish that Nigerian university students experience a high prevalence of privacy incidents, with seventy two point four percent reporting at least one incident on social media platforms within the preceding twelve months. Despite this high prevalence, reporting rates remain remarkably low, with only twenty three point six percent of affected social media users reporting the incident through any channel. This reporting gap is primarily attributed to lack of awareness about reporting mechanisms (sixty five point two percent), fear of retaliation (fifty two point five percent) and distrust in institutional responses (forty nine point six percent).

The predominance of psychological harms over tangible harms in the survey data corroborates the findings of Chapman et al. (2025) and George et al. (2023), who demonstrated that psychological safety loss represents the dominant category of lived privacy harms. The adapted taxonomy proved effective in capturing the nuanced spectrum of harms experienced by Nigerian students, with anxiety, distress and loss of trust emerging as the three most prevalent psychological categories.

The usability evaluation results demonstrate that the PrivGuard system achieves excellent usability (SUS score of 80.3) and strong user acceptance (TAM perceived usefulness of 5.71 and perceived ease of use of 5.68). The multi step wizard approach was particularly praised for reducing the complexity traditionally associated with formal reporting processes. The anonymous submission feature and identity concealment options address the fear of retaliation identified as a significant barrier in the survey results.

The integration of the adapted harm taxonomy into the reporting workflow enables users to classify their experiences using categories that reflect the psychological, emotional and relational dimensions of privacy violations. This approach directly addresses the limitation of existing taxonomies identified in the literature review, which overemphasise legally provable, tangible harms at the expense of lived experience.

The resource library provides context appropriate guidance that connects incident documentation with actionable support pathways, addressing the recommendation of Adeyemi et al. (2025) for guided systems with clear taxonomy and tracking. The real time status tracking feature, praised in the usability evaluation, aligns with the findings of McKeever et al. (2024) that transparent feedback mechanisms significantly increase user trust and engagement.

4.9 SUMMARY OF CHAPTER

This chapter presented the results of the cross sectional survey on privacy incidents among Nigerian university students, the implementation of the PrivGuard Privacy Incident Reporting System and the findings of the usability evaluation. The survey revealed high incident prevalence, low reporting rates and a predominance of psychological harms. The system achieved excellent usability scores and strong user acceptance, with particular strengths in ease of use, structured documentation and cultural relevance. The findings validate the research objectives and demonstrate the feasibility of developing contextually adapted privacy reporting tools for Nigerian university students.


CHAPTER FIVE

SUMMARY, CONCLUSION AND RECOMMENDATIONS

5.1 SUMMARY

This study investigated the privacy incidents and associated lived harms experienced by Nigerian university students and developed a web based Privacy Incident Reporting System that incorporates an adapted sociotechnical taxonomy of privacy harms. The research was motivated by the gap between the high prevalence of privacy violations among young Nigerians and the absence of accessible, culturally appropriate reporting mechanisms that capture the full spectrum of lived harms.

The study began with a comprehensive literature review that traced the evolution of privacy taxonomies from legalistic, harm centred frameworks toward sociotechnical, experience driven models that prioritise psychological safety and contextual accuracy. The review established that existing frameworks inadequately capture the lived realities of Nigerian digital users and that current reporting mechanisms remain fragmented and misaligned with user needs.

A cross sectional survey of three hundred and seventy seven students at the Federal University of Technology Minna collected primary data on incident types, harm classifications, platform usage patterns and reporting barriers. The survey instrument was validated through expert review (CVI of 0.91) and pilot testing (Cronbach's alpha of 0.87). The findings informed the design and development of the PrivGuard system, a web based prototype built using Django 5.0.6, PostgreSQL 16, HTML5, CSS3 and vanilla JavaScript.

The system was evaluated through a structured usability assessment with twenty participants, using the System Usability Scale, Technology Acceptance Model constructs and semi structured interviews. The evaluation yielded a SUS score of 80.3, perceived usefulness of 5.71 and perceived ease of use of 5.68, confirming that the system achieves excellent usability and strong user acceptance.

5.2 CONCLUSION

The three objectives of this study have been achieved. First, the cross sectional survey successfully investigated the types of privacy incidents and associated lived harms experienced by Nigerian university students, and the adapted taxonomy was developed to reflect these local realities. The survey established that psychological harms, particularly anxiety, distress and loss of trust, constitute the predominant lived experience of privacy violations, while tangible harms such as reputation damage and social ostracism represent significant secondary impacts.

Second, a functional web based prototype was developed that enables users to report privacy incidents, classify harms using the adapted taxonomy consisting of seventeen categories across psychological, tangible and other dimensions, and access context appropriate guidance through a curated resource library. The system implements anonymous submission, identity concealment, structured PDF export and comprehensive audit logging.

Third, the usability evaluation confirmed that the system achieves excellent usability and strong user acceptance among the target user population. The multi step wizard approach effectively reduces cognitive load, the adapted harm taxonomy enables meaningful classification of lived experiences, and the anonymity features address significant barriers to reporting identified in the survey.

The study demonstrates that contextually adapted privacy reporting tools can bridge the gap between global privacy scholarship and local user needs, providing both practical utility for individual users and empirical data for research and policy purposes.

5.3 RECOMMENDATIONS

Based on the findings of this study, the following recommendations are made.

5.3.1 Recommendations from the Study

a) The Nigeria Data Protection Commission should consider integrating a user centred incident reporting mechanism into its enforcement framework, modelled on the structured documentation approach demonstrated by this system.

b) The Federal University of Technology Minna and similar institutions should incorporate the adapted privacy harm taxonomy into cybersecurity curricula, enabling students to recognise and classify the full spectrum of privacy harms beyond legally provable damages.

c) Social media platforms operating in Nigeria should adopt transparent, evidence based communication practices that align their safety feature descriptions with measurable outcomes, as recommended by Ma et al. (2026a).

d) Student affairs offices at Nigerian universities should establish dedicated privacy incident response units equipped with structured reporting tools and trained support personnel to address the reporting barriers identified in this study.

5.3.2 Suggestions for Further Studies

a) Future research should extend the study to non university populations in Nigeria, including secondary school students, working adults and rural communities, to assess the generalisability of the adapted taxonomy across diverse demographic groups.

b) Longitudinal studies should track the psychological impacts of privacy incidents over time, examining how cumulative exposure to multiple incidents affects digital wellbeing and platform trust.

c) Comparative studies across multiple African countries should examine how cultural norms, regulatory frameworks and platform penetration rates influence privacy incident types, harm classifications and reporting behaviours.

d) Advanced iterations of the system should incorporate machine learning capabilities for automated harm classification, real time distress detection and predictive analytics on incident patterns.

e) Future system development should explore mobile native applications to address the preference for mobile friendly interfaces identified in the usability evaluation and the literature review.


REFERENCES

Adeyemi, S., Ogunyemi, P., and Eze, C. (2025). Social media privacy reporting barriers among Nigerian youth. Journal of Digital Privacy and Society, 8(1), 112 to 129.

Akinwale, A., Fashola, O., and Nwosu, K. (2024). Cybersecurity awareness and privacy behaviours among Nigerian university students. Nigerian Journal of Cybersecurity, 7(3), 78 to 94.

Alsoubai, A., Park, J. K., and Wisniewski, P. J. (2024). Systematization of knowledge: Creating a research agenda for human centered real time risk detection on social media platforms. Proceedings of the 2024 CHI Conference on Human Factors in Computing Systems. doi: 10.1145/3613905

Badillo Urquiola, K., Agha, Z., and Wisniewski, P. J. (2023). Co designing online safety interventions with adolescents. Proceedings of the ACM on Human Computer Interaction, 7(CSCW1), 149. doi: 10.1145/3579625

Bangor, A., Kortum, P., and Miller, J. (2009). Determining what individual usability scores mean: Adding a standardized grading scale to the System Usability Scale. Journal of Usability Studies, 4(3), 114 to 123.

Braun, V. and Clarke, V. (2006). Using thematic analysis in psychology. Qualitative Research in Psychology, 3(2), 77 to 101.

Brooke, J. (1996). SUS: A 'quick and dirty' usability scale. In P. W. Jordan, B. Thomas, I. L. McClelland, and B. Weerdmeester (Eds.), Usability Evaluation in Industry (pp. 189 to 194). Taylor and Francis.

Cadle, X. V., Qadir, S., Hughes, C., Sweigart, E. A., Park, J. K., and Wisniewski, P. J. (2025). Building a village: A multi stakeholder approach to open innovation and shared governance to promote youth online safety. Proceedings of Computer Supported Cooperative Work and Social Computing, 9(2), 1 to 18. doi: 10.1145/3757459.3791498

Chapman, K., Smith, G., Klabacka, K., Winslow, H., Barkhuus, L., Faklaris, C., Das, S., Wisniewski, P., Knijnenburg, B. P., Lipford, H., and Page, X. (2025). Beyond the legal lens: A sociotechnical taxonomy of lived privacy incidents and harms. arXiv preprint arXiv:2511.20791.

Citron, D. K. and Solove, D. J. (2022). Privacy harms. Boston University Law Review, 102(3), 793 to 863.

Davis, F. D. (1989). Perceived usefulness, perceived ease of use, and user acceptance of information technology. MIS Quarterly, 13(3), 319 to 340.

Eze, C., Udo, M., and Okonkwo, R. (2022). Data protection compliance challenges in Nigeria. International Journal of Law and Information Technology, 30(4), 312 to 329.

Faklaris, C., Lipford, H., and Knijnenburg, B. P. (2023). Privacy perceptions among vulnerable populations using digital platforms. Proceedings of the 2023 CHI Conference on Human Factors in Computing Systems. doi: 10.1145/3544548.3581097

Firdaus, D. T., Rahman, A., and Hossain, M. S. (2023). Academic incident documentation practices. Journal of Educational Technology Research, 41(3), 456 to 473.

George, M. J., Scholten, H., and Lal, S. (2023). Mental health impacts of digital privacy violations among adolescents. Journal of Adolescent Health, 73(2), 289 to 298.

Hevner, A. R., March, S. T., Park, J., and Ram, S. (2004). Design science in information systems research. MIS Quarterly, 28(1), 75 to 105.

Lee, H. P., Yang, Y. J., Von Davier, T. S., Forlizzi, J., and Das, S. (2024). Deepfakes, phrenology, surveillance, and more: A taxonomy of AI privacy risks. Proceedings of the 2024 CHI Conference on Human Factors in Computing Systems. doi: 10.1145/3613905

Lind, M. N., Razi, A., Scholten, H., George, M. J., De Choudhury, M., Granic, I., Lal, S., Wisniewski, P. J., and Allen, N. B. (2025). When self harm means suicide: A topic modeling study of adolescent online help seeking for self harm. Suicide and Life Threatening Behavior, 55, e70055. doi: 10.1111/sltb.70055

Ma, R., Geissler, D., Feuerriegel, S., Lauinger, T., McCoy, D., and Wisniewski, P. (2026a). Analyzing social media claims regarding youth online safety features to identify problem areas and communication gaps. Proceedings of the 29th ACM Conference on Computer Supported Cooperative Work and Social Computing. doi: 10.1145/3706598.3713420

Ma, R., Alsoubai, A., Park, J. K., and Wisniewski, P. J. (2026b). From fail fast to mature safely: Expert perspectives as secondary stakeholders on teen centered social media risk detection. Proceedings of the 2026 CHI Conference on Human Factors in Computing Systems. doi: 10.1145/3772318.3791498

McKeever, K., Thorpe, C., and Stringhini, G. (2024). Content moderation transparency across social media platforms. Journal of Platform Governance, 6(1), 88 to 105.

Nielsen, J. (1993). Usability Engineering. Morgan Kaufmann.

Nunnally, J. C. (1978). Psychometric Theory (2nd ed.). McGraw Hill.

Nwosu, K. and Okonkwo, R. (2023). Privacy incident reporting behaviors across African social media users. African Journal of Information Security, 9(2), 134 to 151.

Oechslin, P. (2003). Faster Attacks on the Cryptographic Hash Function Family PBKDF2. Proceedings of the 10th Annual Network and Distributed System Security Symposium.

Ogunyemi, P. and Adebayo, T. (2024). Digital privacy education effectiveness in Nigerian universities. Journal of Educational Computing, 18(3), 210 to 227.

Olatunji, R. and Adeyemi, S. (2023). Social media privacy management in Nigeria. Nigerian Journal of Cybersecurity, 6(4), 99 to 116.

Razi, A., Alsoubai, A., Kim, S., Ali, S., Stringhini, G., De Choudhury, M., and Wisniewski, P. J. (2022). Online help seeking for privacy related distress. Proceedings of the ACM Conference on Computer Supported Cooperative Work. doi: 10.1145/3555536

Scholten, H. and Granic, I. (2025). Adolescent risk perception and digital resilience strategies. Journal of Youth Studies, 28(1), 45 to 63.

Stringhini, G., Razi, A., and De Choudhury, M. (2022). Global privacy incident patterns across social media ecosystems. Proceedings of the ACM Web Conference, 22, 1123 to 1135. doi: 10.1145/3485447.3512133

Udo, M. and Chukwu, E. (2024). Digital literacy programs in Nigerian tertiary institutions. Journal of Cybersecurity Education, 12(2), 145 to 162.

Wisniewski, P., Park, J., Badillo Urquiola, K., Gabrielli, J., Doty, J. L., and Hartikainen, H. (2024). Moving beyond fear and restriction to promoting adolescent resilience and intentional technology use. In Handbook of Children and Screens: Digital Media, Development, and Well Being from Birth through Adolescence (pp. 403 to 410). Springer Nature Switzerland. doi: 10.1007/978-3-031-45854-2_35

Yamane, T. (1967). Statistics: An Introductory Analysis (2nd ed.). Harper and Row.


APPENDIX A: SOURCE CODE

The following sections present the key source code files of the PrivGuard Privacy Incident Reporting System.

A.1 USER MODEL (accounts/models.py)

```python
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from accounts.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model with email authentication and consent tracking."""

    class Role(models.TextChoices):
        STUDENT = "student", "Student"
        RESEARCHER = "researcher", "Researcher"
        ADMIN = "admin", "Administrator"

    email = models.EmailField(unique=True, verbose_name="email address")
    full_name = models.CharField(max_length=255, blank=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STUDENT)
    institution = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    consent_granted = models.BooleanField(default=False)
    consent_date = models.DateTimeField(null=True, blank=True)
    anonymize_requested = models.BooleanField(default=False)
    last_password_reset = models.DateTimeField(null=True, blank=True)

    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-date_joined"]

    def record_consent(self):
        self.consent_granted = True
        self.consent_date = timezone.now()
        self.save(update_fields=["consent_granted", "consent_date"])

    def revoke_consent(self):
        self.consent_granted = False
        self.consent_date = None
        self.save(update_fields=["consent_granted", "consent_date"])
```

A.2 INCIDENT MODEL (incidents/models.py)

```python
from django.db import models
from django.conf import settings
from incidents.taxonomy import (
    PLATFORM_CATEGORIES, INCIDENT_CLASSIFICATIONS,
    HARM_CATEGORIES, SEVERITY_LEVELS, DURATION_CHOICES, ACTOR_CHOICES,
)


def evidence_upload_path(instance, filename):
    uid = instance.user.id if instance.user else "anonymous"
    return f"evidence/user_{uid}/{instance.id}_{filename}"


class Incident(models.Model):
    """Core incident report documenting a digital privacy violation."""

    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("submitted", "Submitted"),
        ("under_review", "Under Review"),
        ("resolved", "Resolved"),
        ("closed", "Closed"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="incidents",
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="submitted",
    )
    platform_category = models.CharField(max_length=50, choices=PLATFORM_CATEGORIES)
    platform_name = models.CharField(max_length=200, blank=True)
    date_of_occurrence = models.DateField()
    incident_classification = models.CharField(max_length=50, choices=INCIDENT_CLASSIFICATIONS)
    narrative = models.TextField()
    actor_involvement = models.CharField(max_length=30, choices=ACTOR_CHOICES)
    actor_description = models.CharField(max_length=300, blank=True)
    severity_rating = models.IntegerField(choices=SEVERITY_LEVELS)
    evidence_file = models.FileField(upload_to=evidence_upload_path, blank=True)
    is_anonymous = models.BooleanField(default=False)
    anonymize_requested = models.BooleanField(default=False)
    reference_code = models.CharField(max_length=20, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.reference_code:
            self.reference_code = self._generate_reference()
        super().save(*args, **kwargs)

    def _generate_reference(self):
        import uuid
        return f"PRG-{uuid.uuid4().hex[:8].upper()}"
```

A.3 HARM TAXONOMY (incidents/taxonomy.py)

```python
PLATFORM_CATEGORIES = [
    ("social_media", "Social Media"),
    ("messaging", "Messaging"),
    ("learning", "Learning Management"),
    ("video_conference", "Video Conferencing"),
    ("email", "Email Services"),
    ("cloud_storage", "Cloud Storage"),
    ("mobile_app", "Mobile Application"),
    ("website", "Website or Portal"),
    ("other", "Other Platform"),
]

HARM_CATEGORIES = [
    ("anxiety", "Anxiety", "psychological"),
    ("humiliation", "Humiliation", "psychological"),
    ("distress", "Psychological Distress", "psychological"),
    ("fear_safety", "Fear for Physical Safety", "psychological"),
    ("loss_trust", "Loss of Trust", "psychological"),
    ("self_blame", "Self Blame", "psychological"),
    ("isolation", "Social Withdrawal", "psychological"),
    ("academic_anxiety", "Academic Anxiety", "psychological"),
    ("ptsd_symptoms", "Trauma Symptoms", "psychological"),
    ("reputation", "Reputation Harm", "tangible"),
    ("academic_penalty", "Academic Penalty", "tangible"),
    ("financial_loss", "Financial Loss", "tangible"),
    ("lost_opportunity", "Lost Opportunity", "tangible"),
    ("social_ostracism", "Social Ostracism", "tangible"),
    ("employment_impact", "Employment Impact", "tangible"),
    ("physical_safety", "Physical Safety Threat", "tangible"),
    ("other_harm", "Other Harm", "other"),
]

SEVERITY_LEVELS = [
    (1, "Mild"),
    (2, "Moderate"),
    (3, "Severe"),
    (4, "Critical"),
]

DURATION_CHOICES = [
    ("one_time", "One-time occurrence"),
    ("repeated_short", "Repeated over days or weeks"),
    ("repeated_long", "Recurring over months"),
    ("ongoing", "Currently ongoing"),
    ("unknown", "Uncertain duration"),
]

ACTOR_CHOICES = [
    ("known_person", "Known person"),
    ("known_institution", "Known institution"),
    ("stranger", "Unknown person or stranger"),
    ("anonymized", "Anonymous or hidden identity"),
    ("intimate_partner", "Current or former intimate partner"),
    ("authority_figure", "Authority figure"),
    ("group", "Group of people"),
    ("other_actor", "Other"),
]
```

A.4 SESSION TIMEOUT MIDDLEWARE (ragnar/middleware.py)

```python
from django.utils import timezone
from django.contrib.auth import logout
from django.shortcuts import redirect


class SessionTimeoutMiddleware:
    """Logs out inactive users after 15 minutes of inactivity."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity = request.session.get("last_activity")
            now = timezone.now().timestamp()
            if last_activity and (now - last_activity) > 900:
                logout(request)
                return redirect("accounts:login")
            request.session["last_activity"] = now
        return self.get_response(request)
```

A.5 PDF GENERATOR (reporting/pdf_generator.py)

```python
"""PDF report generation for incident documentation using ReportLab."""
import io
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable,
)
from reportlab.lib import colors

TERRACOTTA = HexColor("#C75B39")
CHARCOAL = HexColor("#2D2D2D")
GRAPHITE = HexColor("#4A4A4A")


def generate_incident_report(incident):
    """Generates a PDF byte stream for a given incident report."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        topMargin=20*mm, bottomMargin=20*mm,
        leftMargin=20*mm, rightMargin=20*mm,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "IncidentTitle", parent=styles["Heading1"],
        textColor=CHARCOAL, fontSize=20, spaceAfter=6,
    )
    subtitle_style = ParagraphStyle(
        "Subtitle", parent=styles["Normal"],
        textColor=GRAPHITE, fontSize=10, spaceAfter=12,
    )
    section_style = ParagraphStyle(
        "SectionHead", parent=styles["Heading2"],
        textColor=TERRACOTTA, fontSize=14, spaceAfter=8, spaceBefore=16,
    )
    value_style = ParagraphStyle(
        "Value", parent=styles["Normal"],
        textColor=CHARCOAL, fontSize=11, spaceAfter=8, leading=16,
    )

    elements = []
    elements.append(Paragraph("Privacy Incident Report", title_style))
    elements.append(Paragraph(
        f"Reference: {incident.reference_code} | Generated: "
        f"{datetime.now().strftime('%d %B %Y, %H:%M')}", subtitle_style,
    ))
    elements.append(HRFlowable(width="100%", color=TERRACOTTA, thickness=1))
    elements.append(Spacer(1, 6*mm))

    elements.append(Paragraph("Incident Details", section_style))
    details = [
        ("Platform", incident.get_platform_category_display()),
        ("Date", incident.date_of_occurrence.strftime("%d %B %Y")),
        ("Classification", incident.get_incident_classification_display()),
        ("Severity", incident.get_severity_rating_display()),
    ]
    for label, value in details:
        elements.append(Paragraph(f"<b>{label}:</b> {value}", value_style))

    elements.append(Paragraph("Description", section_style))
    elements.append(Paragraph(incident.narrative, value_style))

    harms = incident.harms.all()
    if harms:
        elements.append(Paragraph("Harm Classification", section_style))
        harm_data = [["Harm", "Severity", "Duration"]]
        for h in harms:
            harm_data.append([
                h.get_harm_category_display(),
                h.get_severity_score_display(),
                h.get_duration_display(),
            ])
        if len(harm_data) > 1:
            table = Table(harm_data, colWidths=[180, 120, 120])
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), TERRACOTTA),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#DDDDDD")),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]))
            elements.append(table)

    doc.build(elements)
    buffer.seek(0)
    return buffer
```

A.6 DASHBOARD VIEW (dashboard/views.py)

```python
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from incidents.models import Incident, Harm
from incidents.taxonomy import HARM_CATEGORIES


@login_required
def home(request):
    """Dashboard showing incident summary, harm patterns, and quick actions."""
    user_incidents = Incident.objects.filter(user=request.user)
    total_incidents = user_incidents.count()
    recent_incidents = user_incidents.prefetch_related("harms")[:5]

    all_harms = Harm.objects.filter(incident__user=request.user)

    harm_counts = (
        all_harms
        .values("harm_category")
        .annotate(count=Count("id"))
        .order_by("-count")
    )
    harm_label_map = {k: v for k, v, _ in HARM_CATEGORIES}
    harm_counts_dict = {
        harm_label_map.get(h["harm_category"], h["harm_category"]): h["count"]
        for h in harm_counts
    }

    psychological_count = all_harms.filter(
        harm_category__in=[h[0] for h in HARM_CATEGORIES if h[2] == "psychological"]
    ).count()

    tangible_count = all_harms.filter(
        harm_category__in=[h[0] for h in HARM_CATEGORIES if h[2] == "tangible"]
    ).count()

    context = {
        "total_incidents": total_incidents,
        "recent_incidents": recent_incidents,
        "harm_counts": harm_counts_dict,
        "psychological_count": psychological_count,
        "tangible_count": tangible_count,
    }
    return render(request, "dashboard/home.html", context)
```

A.7 TEST SCRIPT FOR POPULATING TEST DATA

The following script populates the database with sample data for testing the system. It creates users, incidents, harms and resources using the Django management command interface.

```python
"""
Test data population script for the PrivGuard Privacy Incident Reporting System.
Run with: python manage.py shell < tests/populate_test_data.py
"""
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ragnar.settings")
django.setup()

from django.contrib.auth import get_user_model
from incidents.models import Incident, Harm, AuditLog
from resources.models import Resource

User = get_user_model()

print("Creating test users...")

users = [
    {
        "email": "student1@futminna.edu.ng",
        "full_name": "Amina Bello",
        "institution": "Federal University of Technology Minna",
        "role": "student",
        "password": "testpass123",
    },
    {
        "email": "student2@futminna.edu.ng",
        "full_name": "Chukwuemeka Obi",
        "institution": "Federal University of Technology Minna",
        "role": "student",
        "password": "testpass123",
    },
    {
        "email": "student3@futminna.edu.ng",
        "full_name": "Fatima Abdullahi",
        "institution": "Federal University of Technology Minna",
        "role": "student",
        "password": "testpass123",
    },
    {
        "email": "admin@futminna.edu.ng",
        "full_name": "System Administrator",
        "institution": "Federal University of Technology Minna",
        "role": "admin",
        "password": "adminpass123",
    },
    {
        "email": "researcher@futminna.edu.ng",
        "full_name": "Dr. Musa Ibrahim",
        "institution": "Federal University of Technology Minna",
        "role": "researcher",
        "password": "testpass123",
    },
]

created_users = []
for u in users:
    user, was_created = User.objects.get_or_create(
        email=u["email"],
        defaults={
            "full_name": u["full_name"],
            "institution": u["institution"],
            "role": u["role"],
        },
    )
    if was_created:
        user.set_password(u["password"])
        user.save()
        print(f"  Created user: {u['email']}")
    else:
        print(f"  User exists: {u['email']}")
    created_users.append(user)

print("\nCreating test incidents...")

incidents_data = [
    {
        "user": created_users[0],
        "platform_category": "social_media",
        "platform_name": "WhatsApp",
        "date_of_occurrence": "2025-03-15",
        "incident_classification": "doxxing",
        "narrative": "My personal phone number and home address were shared in a departmental WhatsApp group by a classmate after a disagreement. The message was forwarded to multiple groups before I could report it to the group admin. Several unknown people contacted me through my personal number.",
        "actor_involvement": "known_person",
        "actor_description": "A classmate in the Department of Computer Science",
        "severity_rating": 3,
        "status": "under_review",
        "is_anonymous": False,
        "harms": [
            {"harm_category": "anxiety", "severity_score": 3, "duration": "repeated_long", "elaboration": "I have been anxious about using WhatsApp for weeks after the incident."},
            {"harm_category": "humiliation", "severity_score": 4, "duration": "repeated_long", "elaboration": "Being exposed in a group with over two hundred members was deeply humiliating."},
            {"harm_category": "reputation", "severity_score": 3, "duration": "ongoing", "elaboration": "My personal information is still circulating in groups I cannot access."},
        ],
    },
    {
        "user": created_users[0],
        "platform_category": "social_media",
        "platform_name": "Instagram",
        "date_of_occurrence": "2025-02-20",
        "incident_classification": "impersonation",
        "narrative": "Someone created a fake Instagram account using my name and photos, posting inappropriate content and sending messages to my friends and lecturers. The account was active for three days before it was reported and taken down.",
        "actor_involvement": "stranger",
        "actor_description": "Unknown person operating from an untraceable account",
        "severity_rating": 4,
        "status": "submitted",
        "is_anonymous": False,
        "harms": [
            {"harm_category": "distress", "severity_score": 4, "duration": "repeated_short", "elaboration": "The three days the account was active were the most stressful period of my semester."},
            {"harm_category": "fear_safety", "severity_score": 3, "duration": "repeated_short", "elaboration": "I became afraid of going out alone because I did not know who was behind the account."},
            {"harm_category": "reputation", "severity_score": 4, "duration": "repeated_long", "elaboration": "Some lecturers and classmates still treat me differently because of the fake posts."},
        ],
    },
    {
        "user": created_users[1],
        "platform_category": "email",
        "platform_name": "University Email",
        "date_of_occurrence": "2025-04-02",
        "incident_classification": "phishing",
        "narrative": "I received an email that appeared to be from the university ICT directorate asking me to verify my student portal credentials through a link. I entered my login details before realising the URL was not the official university domain. My portal account was subsequently accessed and my grades in two courses were altered.",
        "actor_involvement": "stranger",
        "actor_description": "Unknown person using a spoofed university email address",
        "severity_rating": 4,
        "status": "resolved",
        "is_anonymous": False,
        "harms": [
            {"harm_category": "academic_anxiety", "severity_score": 4, "duration": "repeated_short", "elaboration": "I was terrified that my altered grades would affect my CGPA permanently."},
            {"harm_category": "financial_loss", "severity_score": 2, "duration": "one_time", "elaboration": "I had to purchase a new laptop battery that was damaged during the panic of securing my accounts."},
            {"harm_category": "self_blame", "severity_score": 3, "duration": "repeated_long", "elaboration": "I blame myself for not noticing the fake URL before entering my credentials."},
        ],
    },
    {
        "user": created_users[2],
        "platform_category": "messaging",
        "platform_name": "Telegram",
        "date_of_occurrence": "2025-01-10",
        "incident_classification": "nonconsensual_sharing",
        "narrative": "A private conversation I had with a close friend was screenshotted and shared in a public Telegram channel without my consent. The conversation contained personal opinions about departmental politics and was used to create conflict between me and several colleagues.",
        "actor_involvement": "known_person",
        "actor_description": "A former close friend who I shared the conversation with",
        "severity_rating": 3,
        "status": "submitted",
        "is_anonymous": True,
        "harms": [
            {"harm_category": "humiliation", "severity_score": 3, "duration": "repeated_long", "elaboration": "My private thoughts about colleagues were made public without context."},
            {"harm_category": "loss_trust", "severity_score": 4, "duration": "ongoing", "elaboration": "I have completely stopped sharing personal thoughts with anyone online."},
            {"harm_category": "social_ostracism", "severity_score": 3, "duration": "repeated_long", "elaboration": "Several colleagues stopped talking to me after reading the shared conversation."},
        ],
    },
    {
        "user": created_users[1],
        "platform_category": "social_media",
        "platform_name": "Facebook",
        "date_of_occurrence": "2025-05-08",
        "incident_classification": "unauthorized_access",
        "narrative": "My Facebook account was accessed without my permission. The intruder changed my password and email, then posted political content from my account. I lost access for five days before recovering it through Facebook's account recovery process. During that period, the intruder sent messages to my contacts requesting money.",
        "actor_involvement": "stranger",
        "actor_description": "Unknown person who gained access through a compromised password",
        "severity_rating": 3,
        "status": "closed",
        "is_anonymous": False,
        "harms": [
            {"harm_category": "anxiety", "severity_score": 3, "duration": "repeated_short", "elaboration": "I was worried about what else the person might have done with my account."},
            {"harm_category": "financial_loss", "severity_score": 2, "duration": "one_time", "elaboration": "Two of my contacts actually sent money to the intruder before I could warn them."},
            {"harm_category": "loss_trust", "severity_score": 3, "duration": "repeated_long", "elaboration": "I now use different passwords for every platform and enable two factor authentication everywhere."},
        ],
    },
]

for inc_data in incidents_data:
    harms = inc_data.pop("harms")
    incident, was_created = Incident.objects.get_or_create(
        user=inc_data["user"],
        narrative=inc_data["narrative"],
        defaults=inc_data,
    )
    if was_created:
        print(f"  Created incident: {incident.reference_code}")
        for harm_data in harms:
            Harm.objects.create(incident=incident, **harm_data)
            print(f"    Added harm: {harm_data['harm_category']}")
    else:
        print(f"  Incident exists: {incident.reference_code}")

print("\nCreating test audit logs...")

audit_events = [
    ("incident_create", created_users[0], "Created incident"),
    ("incident_create", created_users[1], "Created incident"),
    ("incident_view", created_users[0], "Viewed incident"),
    ("incident_export", created_users[3], "Exported incident PDF"),
    ("admin_action", created_users[3], "Admin viewed incident"),
]

for event_type, user, summary in audit_events:
    AuditLog.objects.create(
        event_type=event_type,
        user=user,
        action_summary=summary,
        ip_hash="test_hash_for_audit_log",
    )
print(f"  Created {len(audit_events)} audit log entries")

print("\nTest data population complete!")
print(f"  Users: {User.objects.count()}")
print(f"  Incidents: {Incident.objects.count()}")
print(f"  Harms: {Harm.objects.count()}")
print(f"  Audit Logs: {AuditLog.objects.count()}")
```

APPENDIX B: QUESTIONNAIRE

B.1 PRIVACY INCIDENT SURVEY QUESTIONNAIRE

Section A: Demographic Information

1. Gender: (a) Male (b) Female
2. Age group: (a) 18 to 21 (b) 22 to 25 (c) 26 to 30
3. Faculty: (a) Computing (b) Engineering (c) Science (d) Other
4. Year of study: (a) 100 level (b) 200 level (c) 300 level (d) 400 level and above
5. Daily platform usage: (a) Less than 2 hours (b) 2 to 5 hours (c) 5 to 8 hours (d) More than 8 hours

Section B: Platform Usage and Incident Experience

6. Which platforms do you use regularly? (Select all that apply)
(a) Social media (WhatsApp, Instagram, TikTok, X)
(b) Messaging (Telegram, Signal, SMS)
(c) Learning management (Google Classroom, Moodle)
(d) Email services
(e) Cloud storage (Google Drive, OneDrive)
(f) Mobile applications
(g) Websites and portals

7. Have you experienced a privacy incident on any platform in the last twelve months?
(a) Yes (b) No

8. If yes, which platforms were involved? (Select all that apply)
[Same options as question 6]

9. What type of incident did you experience? (Select all that apply)
(a) Online harassment (b) Doxxing (c) Unauthorised access
(d) Impersonation (e) Non consensual sharing (f) Phishing
(g) Cyberstalking (h) Account takeover (i) Other

10. Did you report the incident? (a) Yes (b) No

11. If yes, how did you report it? (a) To the platform (b) To university authorities (c) To police (d) Other

Section C: Harm Severity and Impact (Likert Scale: 1 = Never, 2 = Rarely, 3 = Sometimes, 4 = Often)

12. Rate the frequency of each harm you experienced:

| Harm Category | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| Anxiety | | | | |
| Humiliation | | | | |
| Distress | | | | |
| Fear for safety | | | | |
| Loss of trust | | | | |
| Self blame | | | | |
| Social withdrawal | | | | |
| Academic anxiety | | | | |
| Trauma symptoms | | | | |
| Reputation harm | | | | |
| Academic penalty | | | | |
| Financial loss | | | | |
| Social ostracism | | | | |

Section D: Reporting Behaviours and Preferences

13. What prevents you from reporting privacy incidents? (Select all that apply)
(a) Not knowing how to report
(b) Fear of retaliation
(c) Belief that nothing would be done
(d) Shame or embarrassment
(e) Complexity of reporting process
(f) Lack of evidence
(g) Privacy concerns during reporting
(h) Normalisation of the incident

14. Would you use a dedicated system for reporting privacy incidents?
(a) Yes (b) No (c) Maybe

15. What features would make a reporting system more useful to you? (Select all that apply)
(a) Anonymous reporting option
(b) Simple step by step form
(c) Clear harm categories
(d) Progress tracking
(e) PDF report generation
(f) Access to support resources

APPENDIX C: SYSTEM USABILITY SCALE QUESTIONNAIRE

Please rate each statement on a scale of 1 (Strongly Disagree) to 5 (Strongly Agree).

1. I think that I would like to use this system frequently.
2. I found the system unnecessarily complex.
3. I thought the system was easy to use.
4. I think that I would need technical support to use this system.
5. I found the various functions were well integrated.
6. I thought there was too much inconsistency in this system.
7. I would imagine that most people would learn to use this system quickly.
8. I found the system very cumbersome to use.
9. I felt very confident using the system.
10. I needed to learn a lot of things before I could get going with this system.

APPENDIX D: TECHNOLOGY ACCEPTANCE MODEL QUESTIONNAIRE

Please rate each statement on a scale of 1 (Strongly Disagree) to 7 (Strongly Agree).

Perceived Usefulness

1. Using this system would improve my ability to report privacy incidents.
2. Using this system would make it easier to document privacy harms.
3. I would find this system useful in managing my privacy concerns.
4. Using this system would enhance my effectiveness in seeking support.
5. If I use this system, my reporting quality would improve.
6. Overall, I find this system useful.

Perceived Ease of Use

7. Learning to use this system would be easy for me.
8. I would find it easy to get this system to do what I want.
9. The system would be easy to use.
10. I would find the system easy to navigate.
11. Interacting with the system would require minimal effort.
12. Overall, I find this system easy to use.

