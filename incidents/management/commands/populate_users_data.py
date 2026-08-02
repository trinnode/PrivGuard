"""
Populate the database with 254 simulated FUT Minna students and their
privacy incident reports, reported between 1 May and 10 July 2026.

Run:  python manage.py populate_users_data
      python manage.py populate_users_data --fresh   (delete existing test data first)

The synthetic data mirrors the survey proportions documented in Chapter 4:
- Harm frequencies from Table 4.4 (anxiety 61.3 %, distress 54.6 %, …)
- Platform categories from Table 4.2
- Incident classifications from Table 4.3

Names are drawn from Nigerian ethnic groups (Hausa, Yoruba, Igbo, Igala,
Idoma, Nupe) with Hausa and Yoruba dominant, and each student receives a
matching institutional email address.
"""

import random
from datetime import date, timedelta, datetime
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone
from incidents.models import Incident, Harm
from incidents.taxonomy import (
    PLATFORM_CATEGORIES,
    INCIDENT_CLASSIFICATIONS,
    HARM_CATEGORIES,
    SEVERITY_LEVELS,
    DURATION_CHOICES,
    ACTOR_CHOICES,
)

User = get_user_model()

# ---------------------------------------------------------------------------
# Nigerian names by ethnic group (male first names, female first names,
# surnames). Weights control ethnic distribution; Hausa and Yoruba dominate.
# ---------------------------------------------------------------------------
ETHNIC_GROUPS = [
    {
        "name": "Hausa",
        "weight": 30,
        "male_first": [
            "Musa", "Umar", "Ibrahim", "Abdullahi", "Abubakar", "Suleiman",
            "Aliyu", "Sani", "Bello", "Lawan", "Haruna", "Usman", "Isah",
            "Aminu", "Bashir", "Jibrin", "Nuhu", "Yakubu", "Garba", "Bala",
            "Danjuma", "Idris", "Rabiu", "Adamu", "Tijjani",
        ],
        "female_first": [
            "Amina", "Aisha", "Fatima", "Zainab", "Mariam", "Hadiza",
            "Hauwa", "Bilkisu", "Khadija", "Halima", "Asmau", "Rukayya",
            "Salamatu", "Maimuna", "Jummai", "Rabiat", "Hafsat", "Ladi",
            "Sa'adatu", "Zahra",
        ],
        "surnames": [
            "Bello", "Musa", "Ibrahim", "Abdullahi", "Abubakar", "Suleiman",
            "Aliyu", "Sani", "Umar", "Lawal", "Haruna", "Usman", "Garba",
            "Bala", "Danjuma", "Idris", "Adamu", "Yau", "Nuhu", "Jibrin",
            "Tukur", "Gwadabe", "Barau", "Magaji",
        ],
    },
    {
        "name": "Yoruba",
        "weight": 30,
        "male_first": [
            "Adewale", "Babatunde", "Olumide", "Kayode", "Femi", "Segun",
            "Tunde", "Kunle", "Damilare", "Ayodeji", "Gbenga", "Wale",
            "Adebayo", "Kehinde", "Taiwo", "Olawale", "Akintunde", "Abiodun",
            "Oladipo", "Adedamola", "Olamide", "Oluwaseun", "Lanre", "Rilwan",
            "Seyi", "Tobi",
        ],
        "female_first": [
            "Funmilayo", "Yetunde", "Temitope", "Bukola", "Kemi", "Bolanle",
            "Iyabo", "Modupe", "Olamide", "Titilayo", "Yemisi", "Ronke",
            "Wuraola", "Abike", "Bunmi", "Ifeoluwa", "Oluwakemi", "Simisola",
            "Tolulope", "Aderonke", "Mojisola", "Ebunoluwa", "Omolara",
            "Bisola",
        ],
        "surnames": [
            "Adeyemi", "Ogunleye", "Adebayo", "Adeleke", "Ajayi", "Balogun",
            "Fashola", "Ogunbiyi", "Akinyemi", "Adepoju", "Adedokun",
            "Babatunde", "Oladipo", "Adeyinka", "Akintola", "Alabi", "Amoo",
            "Bamidele", "Oyelaran", "Salako", "Sowunmi", "Osho", "Lawanson",
            "Ogunlade",
        ],
    },
    {
        "name": "Igbo",
        "weight": 15,
        "male_first": [
            "Chibueze", "Emeka", "Chinedu", "Ebuka", "Ifeanyi", "Chisom",
            "Nnamdi", "Chukwudi", "Chidera", "Ikenna", "Kenechukwu", "Obinna",
            "Chijioke", "Kelechi", "Nonso", "Uchenna", "Chibuike", "Chukwuma",
            "Izu", "Chukwuemeka", "Somtochukwu", "Tochukwu", "Ugochukwu",
            "Arinze", "Chidiebere",
        ],
        "female_first": [
            "Ngozi", "Chiamaka", "Adaeze", "Chioma", "Nneka", "Ifunanya",
            "Ogechi", "Amaka", "Nkechi", "Chinyere", "Uju", "Chinwendu",
            "Ebere", "Onyinye", "Chidinma", "Adanna", "Nneoma", "Obiageli",
            "Uzoamaka", "Ezinne", "Mmesoma", "Kelechi",
        ],
        "surnames": [
            "Okafor", "Nwachukwu", "Okonkwo", "Okeke", "Nwosu", "Chukwu",
            "Ugwu", "Eze", "Nnamdi", "Okoro", "Onyema", "Osuagwu", "Egbuna",
            "Mbah", "Ugwuoke", "Eke", "Nwoye", "Okechukwu", "Uzochukwu",
            "Nwankwo", "Anyaegbu", "Onwuchekwa", "Ezeani", "Okafor",
        ],
    },
    {
        "name": "Igala",
        "weight": 8,
        "male_first": [
            "Ocholi", "Opaluwa", "Ene", "Ocheja", "Atabo", "Akwu", "Abutu",
            "Onoja", "Egwuma", "Iyaji", "Odaudu", "Oche", "Obaje", "Etuh",
            "Amodu", "Aliyu", "Ojochogwu", "Okpanachi",
        ],
        "female_first": [
            "Ameh", "Ojone", "Ene", "Atabo", "Omale", "Oche", "Grace",
            "Regina", "Rachael", "Jochebed", "Amina", "Rukayat", "Ade",
        ],
        "surnames": [
            "Opaluwa", "Ocholi", "Atabo", "Ocheja", "Akwu", "Onoja", "Abutu",
            "Iyaji", "Egwu", "Odaudu", "Ene", "Obaje", "Etuh", "Idoko",
            "Amodu", "Okpanachi",
        ],
    },
    {
        "name": "Idoma",
        "weight": 7,
        "male_first": [
            "Ochai", "Ogbole", "Adah", "Audu", "Oche", "Ejeh", "Ochimana",
            "Abah", "Ogah", "Okwute", "Ojokwu", "Enemona", "Obida", "Adoka",
            "Agbo", "Odoh", "Eche",
        ],
        "female_first": [
            "Ochanya", "Oche", "Ene", "Eunice", "Grace", "Mary", "Esther",
            "Amina", "Regina", "Hawa", "Joy", "Peace", "Rebecca",
        ],
        "surnames": [
            "Ochai", "Ogbole", "Adah", "Audu", "Oche", "Ejeh", "Abah",
            "Ogah", "Obida", "Agbo", "Enemona", "Adoka", "Okwute", "Ochimana",
            "Odoh", "Eche",
        ],
    },
    {
        "name": "Nupe",
        "weight": 10,
        "male_first": [
            "Ndagi", "Tsado", "Sheshi", "Bello", "Idris", "Musa", "Kolo",
            "Gana", "Jimada", "Adamu", "Umar", "Abubakar", "Jiya", "Etsu",
            "Salifu", "Muhammadu", "Ubandawaki",
        ],
        "female_first": [
            "Salamatu", "Maimuna", "Larai", "Aisha", "Fatima", "Amina",
            "Binta", "Hawau", "Nana", "Sadiya", "Zainab", "Rukayyat",
            "Hadiza",
        ],
        "surnames": [
            "Ndagi", "Tsado", "Sheshi", "Kolo", "Gana", "Jimada", "Jiya",
            "Etsu", "Salifu", "Bello", "Idris", "Musa", "Ndagj", "Umar",
            "Abubakar", "Muhammadu",
        ],
    },
]


def weighted_ethnicity():
    """Pick an ethnic group using the configured weights."""
    groups, weights = zip(*[(g, g["weight"]) for g in ETHNIC_GROUPS])
    return random.choices(groups, weights=weights, k=1)[0]


def nigerian_name():
    """Return (first_name, surname, ethnicity) with matching ethnicity and gender."""
    group = weighted_ethnicity()
    gender = random.choice(["male", "female"])
    pool = group["male_first"] if gender == "male" else group["female_first"]
    first = random.choice(pool)
    surname = random.choice(group["surnames"])
    return first, surname, group["name"]

# ---------------------------------------------------------------------------
# Survey-based weights (from Chapter 4 tables)
# ---------------------------------------------------------------------------
PLATFORM_WEIGHTS = [
    ("social_media", 72.4), ("messaging", 45.9), ("learning", 31.3),
    ("email", 28.6), ("cloud_storage", 18.3), ("mobile_app", 34.2),
    ("website", 22.8), ("video_conference", 5.0), ("other", 3.0),
]

INCIDENT_WEIGHTS = [
    ("harassment", 23.6), ("doxxing", 19.1), ("unauthorized_access", 15.4),
    ("impersonation", 12.2), ("nonconsensual_sharing", 10.1),
    ("phishing", 8.5), ("cyberstalking", 6.4), ("account_takeover", 4.8),
    ("other", 3.2),
]

# Percentage of users who experienced each harm (Table 4.4)
HARM_RATES = {
    "anxiety": 61.3, "distress": 54.6, "loss_trust": 48.5,
    "humiliation": 39.8, "self_blame": 32.4, "isolation": 28.1,
    "academic_anxiety": 24.7, "fear_safety": 19.4, "ptsd_symptoms": 12.7,
    "reputation": 44.3, "academic_penalty": 21.5, "financial_loss": 16.7,
    "social_ostracism": 29.4, "lost_opportunity": 14.3,
    "employment_impact": 8.8, "physical_safety": 11.1,
}

# Mean severity by harm (for realistic assignment)
HARM_MEAN_SEVERITY = {
    "anxiety": 2.7, "distress": 2.9, "loss_trust": 2.4,
    "humiliation": 3.1, "self_blame": 2.2, "isolation": 2.6,
    "academic_anxiety": 2.5, "fear_safety": 3.3, "ptsd_symptoms": 3.4,
    "reputation": 2.8, "academic_penalty": 2.6, "financial_loss": 2.1,
    "social_ostracism": 2.7, "lost_opportunity": 2.3,
    "employment_impact": 2.0, "physical_safety": 3.2,
}

SEVERITY_VALUES = [s[0] for s in SEVERITY_LEVELS]
DURATION_VALUES = [d[0] for d in DURATION_CHOICES]
ACTOR_VALUES = [a[0] for a in ACTOR_CHOICES]

# ---------------------------------------------------------------------------
# Template narratives for variety
# ---------------------------------------------------------------------------
INCIDENT_NARRATIVES = {
    "harassment": [
        "One guy in my department keeps sending me mean messages on the WhatsApp group. It started when I disagreed with him about a course project. Now some of his friends joined in too and nobody is stopping them.",
        "Someone started a thread about me on a campus page, calling me names I don't even want to repeat. A lot of people saw it before I reported it and got it removed.",
        "I keep getting insulting messages on Instagram from this person. When I block one account they open another one and continue. It's been going on for weeks now.",
    ],
    "doxxing": [
        "Someone posted my phone number and my address in our class group chat. I don't even know how they got it. Now I get calls and messages from strangers at night.",
        "My ex friend shared my grades and my personal details on Twitter. Even my matric number was there. People in my department saw it and I felt really exposed.",
        "Somebody shared where I stay and my lecture schedule in a Telegram group. Now I don't feel safe walking to class anymore because I feel like people are watching me.",
    ],
    "unauthorized_access": [
        "Someone logged into my school portal without my permission. They changed my course registration and submitted forms I didn't do. It took the ICT people two weeks before I got my account back.",
        "I found out someone had logged into my Google account from another device. They went through my Drive and saw my personal documents and my school work.",
    ],
    "impersonation": [
        "Someone opened a fake Instagram account using my name and my pictures. They sent weird messages to my lecturers and my classmates. I only found out when my friends started asking me why I was talking like that.",
        "Someone created an email that looks like mine and used it to ask for my academic records from the department office. The lecturer only found out it wasn't me when he called me directly.",
    ],
    "nonconsensual_sharing": [
        "Private pictures from my phone were shared in a WhatsApp group without me knowing. I only found out when a friend told me people were passing them around.",
        "My roommate recorded a private conversation we had and shared it in a student group. People took my words out of context and started spreading rumors about me.",
    ],
    "phishing": [
        "I got an email that looked like it was from the ICT department asking me to confirm my portal password. I typed my details in and only later found out the website was fake. My account was hacked within hours.",
        "Someone sent me a link that looked like it was about my stipend payment. I clicked it and it took my Instagram login. Then they started posting on my account without my permission.",
    ],
    "cyberstalking": [
        "This person has been messaging me on WhatsApp, Telegram and Instagram for months now. They know my routine and they know where I live on campus and it's really scary.",
        "Someone made a fake account to follow everything I post. They comment on things I share and they always seem to know where I am. I've blocked them like five times but they keep making new accounts.",
    ],
    "account_takeover": [
        "Someone took over my WhatsApp through a SIM swap. They turned on two factor authentication before I could recover it so I was locked out for days. They even messaged my contacts asking for money.",
        "A hacker got into my Instagram and changed my password and my email. They posted things and sent messages to my followers. It took me a whole week to get my account back.",
    ],
    "other": [
        "The exam portal showed my script to other students because of an error. My answers and my score were visible to everyone in my class for some hours before they fixed it.",
        "My lecturer shared a spreadsheet with our names, numbers and grades to the whole class by email. A lot of students complained about it.",
    ],
}

PLATFORM_NAMES = {
    "social_media": ["WhatsApp", "Instagram", "TikTok", "Twitter", "Facebook"],
    "messaging": ["Telegram", "Signal", "SMS"],
    "learning": ["Google Classroom", "Moodle", "Blackboard"],
    "video_conference": ["Zoom", "Google Meet", "Microsoft Teams"],
    "email": ["University Email", "Gmail", "Outlook", "Yahoo Mail"],
    "cloud_storage": ["Google Drive", "OneDrive", "Dropbox", "iCloud"],
    "mobile_app": ["Bolt", "PiggyVest", "Paystack", "OPay", "Flutterwave"],
    "website": ["School Portal", "Campus Blog", "JAMB Portal"],
    "other": ["Other Platform"],
}

HARM_ELABORATIONS = {
    "anxiety": [
        "I keep checking my phone even when I don't want to. I'm scared of what I might see.",
        "I can't concentrate in class anymore. My mind keeps going back to what happened.",
        "Even opening my social media makes my heart beat fast now.",
    ],
    "distress": [
        "I cried so many times thinking about it. I couldn't even talk about it to anyone at first.",
        "I couldn't eat or sleep properly for weeks. I just kept replaying everything in my head.",
    ],
    "loss_trust": [
        "I don't trust anyone with my information anymore. Not even my friends.",
        "This thing made me stop trusting people online completely.",
    ],
    "humiliation": [
        "I felt so ashamed knowing people saw my private stuff. I didn't want to show my face in class.",
        "I just wanted to disappear when I found out people were talking about me.",
    ],
    "self_blame": [
        "I keep telling myself I should have been more careful.",
        "I blame myself for trusting the wrong person. I should have known better.",
    ],
    "isolation": [
        "I deleted all my social media after it happened. I don't even want to look at it.",
        "I stopped talking to my friends because I felt too ashamed to explain what happened.",
    ],
    "academic_anxiety": [
        "I kept thinking my grades were going to suffer because of this.",
        "I couldn't focus on my school work at all after what happened.",
        "I was scared the lecturer would treat me differently.",
    ],
    "fear_safety": [
        "I'm scared to walk alone on campus now. I always look behind me.",
        "I changed the way I walk to lectures because I feel like someone is watching me.",
        "I don't even feel safe in my hostel anymore.",
    ],
    "ptsd_symptoms": [
        "I have nightmares about it. I wake up and it feels like it's happening again.",
        "When I get a notification I get scared for no reason. My heart just jumps.",
        "I can't use that app anymore without feeling afraid.",
    ],
    "reputation": [
        "People I don't even know already have an opinion about me because of what was shared.",
        "People in my department look at me differently now.",
        "Even some lecturers treat me different because of what they heard.",
    ],
    "academic_penalty": [
        "I missed a lot of deadlines because I couldn't focus on anything.",
        "My grades dropped because I stopped going to class.",
        "This affected my results for the semester.",
    ],
    "financial_loss": [
        "I had to buy a new SIM card because of the hack. It cost me money.",
        "I spent money buying data to secure all my accounts.",
        "There was money in my account and it's gone now.",
    ],
    "social_ostracism": [
        "My friends stopped inviting me to things. They act like I did something wrong.",
        "People avoid me in the department now because of the rumors.",
        "I was left out of study groups because of what people heard about me.",
    ],
    "lost_opportunity": [
        "I lost a chance to be a class representative because of all the gossip.",
        "I missed out on an internship because of what happened.",
        "They didn't even consider me for a position because of the whole drama.",
    ],
    "employment_impact": [
        "I'm scared this will follow me even after I graduate. Employers might see those posts.",
        "I'm starting to think I should not go into this line of work at all.",
        "I worry companies will find those posts when they search my name.",
    ],
    "physical_safety": [
        "Someone who saw my location actually followed me on campus.",
        "The person who exposed me came to my hostel. I was so scared.",
        "I had to report to security because I was getting threats.",
    ],
}


def weighted_choice(items):
    """Pick an item from a list of (value, weight) tuples."""
    values, weights = zip(*items)
    return random.choices(values, weights=weights, k=1)[0]


def pick_harms():
    """Return a list of harm_category keys based on survey prevalence rates."""
    selected = []
    for harm_key, rate in HARM_RATES.items():
        if rate >= 100 or random.random() < rate / 100:
            selected.append(harm_key)
    return selected if selected else ["anxiety"]  # at least one harm


def random_severity(mean):
    """Generate a realistic severity score (1-4) clustered around a mean."""
    base = round(random.gauss(mean, 0.7))
    return max(1, min(4, base))


def random_date(start: date, end: date) -> date:
    return start + timedelta(days=random.randint(0, (end - start).days))


class Command(BaseCommand):
    help = "Populate 254 simulated FUT Minna students with backdated incidents and harms"

    def add_arguments(self, parser):
        parser.add_argument(
            "--fresh",
            action="store_true",
            help="Delete existing incidents, harms, and student users before populating",
        )

    def handle(self, *args, **options):
        random.seed(42)
        fresh = options["fresh"]

        # ------------------------------------------------------------------
        # Optionally remove old data
        # ------------------------------------------------------------------
        if fresh:
            self.stdout.write("Deleting existing test data …")
            Harm.objects.all().delete()
            Incident.objects.all().delete()
            User.objects.filter(
                role="student",
                email__endswith="@st.futminna.edu.ng",
            ).delete()
            User.objects.filter(
                role="student",
                email__regex=r"@(gmail|yahoo|outlook)\.com$",
            ).delete()
            self.stdout.write("Done.\n")

        # ------------------------------------------------------------------
        # Ensure admin user exists
        # ------------------------------------------------------------------
        admin_email = "admin@futminna.edu.ng"
        if not User.objects.filter(email=admin_email).exists():
            admin_user = User.objects.create_superuser(
                email=admin_email,
                password="admin123",
                full_name="System Administrator",
                institution="Federal University of Technology Minna",
                role="admin",
            )
            self.stdout.write(f"Created admin: {admin_email} / admin123")
        else:
            self.stdout.write(f"Admin exists: {admin_email}")

        # ------------------------------------------------------------------
        # Create 254 students, registered between 1 May and 10 July 2026
        # ------------------------------------------------------------------
        registration_start = date(2026, 5, 1)
        registration_end = date(2026, 7, 10)
        incident_period_start = date(2026, 1, 1)
        incident_period_end = date(2026, 7, 10)

        created_users = 0
        batch = []
        used_emails = set()

        self.stdout.write(f"Creating {254} students …")

        for i in range(254):
            first, surname, ethnicity = nigerian_name()
            slug = lambda s: s.lower().replace("'", "").replace(" ", "")
            # Predominantly Gmail (80%), with Outlook and Yahoo split the rest.
            domain_roll = random.random()
            if domain_roll < 0.80:
                domain = "gmail.com"
            elif domain_roll < 0.90:
                domain = "outlook.com"
            else:
                domain = "yahoo.com"
            email = f"{slug(first)}.{slug(surname)}@{domain}"
            if email in used_emails:
                email = f"{slug(first)}.{slug(surname)}{i}@{domain}"
            used_emails.add(email)

            full_name = f"{first} {surname}"
            reg_date = random_date(registration_start, registration_end)
            consent = random.random() < 0.85

            batch.append(
                User(
                    email=email,
                    full_name=full_name,
                    role="student",
                    institution="Federal University of Technology Minna",
                    is_active=True,
                    date_joined=timezone.make_aware(datetime.combine(reg_date, datetime.min.time())),
                    consent_granted=consent,
                    consent_date=timezone.make_aware(datetime.combine(reg_date, datetime.min.time())) if consent else None,
                    last_password_reset=None,
                )
            )
            created_users += 1

            # Flush every 50 to keep memory low
            if len(batch) >= 50:
                User.objects.bulk_create(batch, ignore_conflicts=True)
                self.stdout.write(f"  … {created_users} users created")
                batch = []

        if batch:
            User.objects.bulk_create(batch, ignore_conflicts=True)

        self.stdout.write(self.style.SUCCESS(f"Created {created_users} users total"))

        # ------------------------------------------------------------------
        # Fetch them back for FK references
        # ------------------------------------------------------------------
        all_students = list(
            User.objects.filter(
                role="student",
                email__regex=r"@(gmail|yahoo|outlook)\.com$",
            )
        )
        self.stdout.write(f"Found {len(all_students)} student records in database")

        # ------------------------------------------------------------------
        # Create 1 incident per student with harms
        # ------------------------------------------------------------------
        total_incidents = 0
        total_harms = 0

        self.stdout.write("Creating incidents and harms …")

        for idx, student in enumerate(all_students):
            num_incidents = 1

            for _ in range(num_incidents):
                platform_key = weighted_choice(PLATFORM_WEIGHTS)
                incident_key = weighted_choice(INCIDENT_WEIGHTS)
                narratives = INCIDENT_NARRATIVES.get(incident_key, ["A privacy incident occurred on a digital platform."])
                narrative = random.choice(narratives)

                platform_name = random.choice(PLATFORM_NAMES.get(platform_key, ["Unknown"]))
                actor_key = random.choice(ACTOR_VALUES)

                student_reg_local = timezone.localtime(student.date_joined).date()

                # Incident date: backdate within period but before or near registration
                if random.random() < 0.6:
                    # Incident happened before registration (that's why they joined)
                    occ_date = random_date(incident_period_start, min(student_reg_local, incident_period_end))
                else:
                    # Incident happened after registration
                    occ_date = random_date(student_reg_local, incident_period_end)

                severity = random.choice(SEVERITY_VALUES)
                is_anon = random.random() < 0.15
                anonymize = random.random() < 0.08
                status = random.choice(["submitted", "under_review", "resolved", "closed"])

                incident = Incident(
                    user=student,
                    status=status,
                    platform_category=platform_key,
                    platform_name=platform_name,
                    date_of_occurrence=occ_date,
                    incident_classification=incident_key,
                    narrative=narrative,
                    actor_involvement=actor_key,
                    actor_description="",
                    severity_rating=severity,
                    is_anonymous=is_anon,
                    anonymize_requested=anonymize,
                )
                incident.save()  # save triggers reference_code generation
                total_incidents += 1

                # Simulate a realistic mix of concealment outcomes so the
                # admin panel shows pending, active, and denied requests.
                if anonymize:
                    roll = random.random()
                    if roll < 0.4:
                        Incident.objects.filter(pk=incident.pk).update(concealment_status="granted")
                    elif roll < 0.55:
                        Incident.objects.filter(pk=incident.pk).update(
                            concealment_status="revoked", anonymize_requested=False,
                        )

                # Backdate created_at so incidents appear in a realistic
                # chronological order within the reporting window.
                # Reported date = registration date + 0-14 days, capped at 10 July 2026.
                # Use local (Africa/Lagos) time so dates never roll into UTC
                # boundary days outside the reporting window.
                student_reg = timezone.localtime(student.date_joined).date()
                report_dt = timezone.make_aware(
                    datetime.combine(
                        min(student_reg + timedelta(days=random.randint(0, 14)), incident_period_end),
                        datetime.min.time(),
                    )
                )
                Incident.objects.filter(pk=incident.pk).update(created_at=report_dt)

                # Assign harms matching survey proportions
                harm_keys = pick_harms()
                for hk in harm_keys:
                    mean_sev = HARM_MEAN_SEVERITY.get(hk, 2.5)
                    sev = random_severity(mean_sev)
                    dur = random.choice(DURATION_VALUES)
                    elab = random.choice(HARM_ELABORATIONS.get(hk, [""]))
                    Harm.objects.create(
                        incident=incident,
                        harm_category=hk,
                        severity_score=sev,
                        duration=dur,
                        elaboration=elab,
                    )
                    total_harms += 1

            if (idx + 1) % 50 == 0:
                self.stdout.write(f"  … processed {idx + 1} / {len(all_students)} students")

        # ------------------------------------------------------------------
        # Summary
        # ------------------------------------------------------------------
        self.stdout.write(self.style.SUCCESS(
            f"\nDone!  Created {created_users} users, "
            f"{total_incidents} incidents, {total_harms} harm classifications."
        ))

        # Report actual percentages
        self.stdout.write("\nHarm prevalence in generated data:\n")
        all_harm_cats = Harm.objects.values_list("harm_category", flat=True)
        total_h = len(all_harm_cats)
        if total_h:
            from collections import Counter
            harm_dist = Counter(all_harm_cats)
            label_map = {k: v for k, v, _ in HARM_CATEGORIES}
            for code in sorted(harm_dist, key=harm_dist.get, reverse=True):
                pct = harm_dist[code] / total_incidents * 100  # per-incident rate
                self.stdout.write(f"  {label_map.get(code, code):35s}  {pct:5.1f}%  ({harm_dist[code]})")
