"""Adapted harm taxonomy for digital privacy violations in Nigerian university contexts."""

PLATFORM_CATEGORIES = [
    ("social_media", "Social Media (WhatsApp, Twitter, Instagram, TikTok)"),
    ("messaging", "Messaging (Telegram, Signal, SMS)"),
    ("learning", "Learning Management (Google Classroom, Moodle, Blackboard)"),
    ("video_conference", "Video Conferencing (Zoom, Google Meet, Teams)"),
    ("email", "Email Services"),
    ("cloud_storage", "Cloud Storage (Google Drive, OneDrive)"),
    ("mobile_app", "Mobile Application"),
    ("website", "Website / Portal"),
    ("other", "Other Platform"),
]

INCIDENT_CLASSIFICATIONS = [
    ("unauthorized_access", "Unauthorized Access - Someone accessed your account or device without permission"),
    ("doxxing", "Doxxing - Personal information shared publicly without consent"),
    ("impersonation", "Impersonation - Someone pretending to be you online"),
    ("nonconsensual_sharing", "Non-Consensual Sharing - Private images or messages shared without permission"),
    ("cyberstalking", "Cyberstalking - Repeated unwanted digital attention or surveillance"),
    ("harassment", "Online Harassment - Abusive, threatening, or degrading messages"),
    ("doxxing_threat", "Doxxing Threat - Threat to expose personal information"),
    ("revenge_porn", "Non-Consensual Intimate Image Distribution"),
    ("phishing", "Phishing - Fraudulent attempt to obtain your personal information"),
    ("account_takeover", "Account Takeover - Someone took control of your account"),
    ("data_breach", "Data Breach - Your data was exposed through a platform breach"),
    ("surveillance", "Surveillance - Being monitored without knowledge or consent"),
    ("outing", "Outing - Private identity or status revealed without consent"),
    ("other", "Other violation not listed here"),
]

HARM_CATEGORIES = [
    # Psychological harms
    ("anxiety", "Anxiety - Persistent worry or fear about digital safety", "psychological"),
    ("humiliation", "Humiliation - Feeling publicly shamed or degraded", "psychological"),
    ("distress", "Psychological Distress - Overwhelming emotional pain or upset", "psychological"),
    ("fear_safety", "Fear for Physical Safety - Concern for personal physical well-being", "psychological"),
    ("loss_trust", "Loss of Trust - Difficulty trusting others in online or offline spaces", "psychological"),
    ("self_blame", "Self-Blame - Feeling responsible for the violation", "psychological"),
    ("isolation", "Social Withdrawal - Avoiding social interactions or online spaces", "psychological"),
    ("academic_anxiety", "Academic Anxiety - Fear of academic repercussions from the incident", "psychological"),
    ("ptsd_symptoms", "Trauma Symptoms - Flashbacks, nightmares, or intrusive thoughts", "psychological"),

    # Tangible harms
    ("reputation", "Reputation Harm - Damage to social or academic standing", "tangible"),
    ("academic_penalty", "Academic Penalty - Loss of grades, opportunities, or standing", "tangible"),
    ("financial_loss", "Financial Loss - Money lost due to the violation", "tangible"),
    ("lost_opportunity", "Lost Opportunity - Missed academic or professional chances", "tangible"),
    ("social_ostracism", "Social Ostracism - Exclusion from peer groups or communities", "tangible"),
    ("employment_impact", "Employment Impact - Harm to job prospects or current employment", "tangible"),
    ("physical_safety", "Physical Safety Threat - Real-world stalking or harm", "tangible"),
    ("other_harm", "Other harm not described above", "other"),
]

SEVERITY_LEVELS = [
    (1, "Mild - Noticeable but manageable impact"),
    (2, "Moderate - Significant impact on daily life"),
    (3, "Severe - Serious impact requiring support"),
    (4, "Critical - Extreme impact requiring immediate assistance"),
]

DURATION_CHOICES = [
    ("one_time", "One-time occurrence"),
    ("repeated_short", "Repeated over days or weeks"),
    ("repeated_long", "Recurring over months"),
    ("ongoing", "Currently ongoing"),
    ("unknown", "Uncertain duration"),
]

ACTOR_CHOICES = [
    ("known_person", "Known person (fellow student, colleague, acquaintance)"),
    ("known_institution", "Known institution (university, department, organization)"),
    ("stranger", "Unknown person / stranger"),
    ("anonymized", "Anonymous / hidden identity"),
    ("intimate_partner", "Current or former intimate partner"),
    ("authority_figure", "Authority figure (lecturer, administrator, employer)"),
    ("group", "Group of people"),
    ("other_actor", "Other"),
]


def get_harm_by_category(category):
    """Returns display info for a given harm category key."""
    mapping = {k: (v, v, t) for k, v, t in HARM_CATEGORIES}
    return mapping.get(category, ("Unknown", "Unknown category", "other"))


def get_harm_type_choices(harm_type=None):
    """Filter harm categories by type: psychological, tangible, or other."""
    if harm_type:
        return [(k, v) for k, v, t in HARM_CATEGORIES if t == harm_type]
    return [(k, f"{v}") for k, v, t in HARM_CATEGORIES]
