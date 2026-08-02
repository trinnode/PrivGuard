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
        print(f"  Created user: {u['email']} (password: {u['password']})")
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
        "narrative": "My personal phone number and home address were shared in a departmental WhatsApp group by a classmate after a disagreement.",
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
        "narrative": "Someone created a fake Instagram account using my name and photos, posting inappropriate content and sending messages to my friends and lecturers.",
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
        "narrative": "I received an email that appeared to be from the university ICT directorate asking me to verify my student portal credentials through a link.",
        "actor_involvement": "stranger",
        "actor_description": "Unknown person using a spoofed university email address",
        "severity_rating": 4,
        "status": "resolved",
        "is_anonymous": False,
        "harms": [
            {"harm_category": "academic_anxiety", "severity_score": 4, "duration": "repeated_short", "elaboration": "I was terrified that my altered grades would affect my CGPA permanently."},
            {"harm_category": "financial_loss", "severity_score": 2, "duration": "one_time", "elaboration": "I had to purchase a new laptop battery that was damaged during the panic."},
            {"harm_category": "self_blame", "severity_score": 3, "duration": "repeated_long", "elaboration": "I blame myself for not noticing the fake URL before entering my credentials."},
        ],
    },
    {
        "user": created_users[2],
        "platform_category": "messaging",
        "platform_name": "Telegram",
        "date_of_occurrence": "2025-01-10",
        "incident_classification": "nonconsensual_sharing",
        "narrative": "A private conversation I had with a close friend was screenshotted and shared in a public Telegram channel without my consent.",
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
        "narrative": "My Facebook account was accessed without my permission. The intruder changed my password and email, then posted political content from my account.",
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
