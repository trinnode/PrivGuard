from django.core.management.base import BaseCommand
from resources.models import Resource


class Command(BaseCommand):
    help = "Seed the database with real Nigerian privacy and wellbeing resources"

    def handle(self, *args, **options):
        resources = [
            # === LEGAL RIGHTS & REPORTING ===
            Resource(
                category="legal",
                title="NDPC Nigeria: Data Protection Complaint Portal",
                description="The Nigeria Data Protection Commission (NDPC) provides an official portal for filing complaints about privacy violations by data controllers. The NDPC has the authority to investigate, issue enforcement notices, and impose administrative fines of up to 2% of annual turnover. Under the Nigeria Data Protection Act 2023, every data subject has the right to lodge a complaint regarding the processing of their personal data.\n\nIn 2025, the NDPC imposed a landmark fine of N766 million on Multichoice Nigeria for privacy violations, demonstrating increased regulatory enforcement. Students experiencing privacy violations by universities, edtech platforms, or digital services can file complaints through the NDPC portal.",
                external_link="https://ndpc.gov.ng/",
                relevance_tags="NDPC, legal, complaint, NDPA, enforcement, data protection, Nigeria, fine, regulatory",
                order=1,
            ),
            Resource(
                category="legal",
                title="Nigerian Data Protection Act 2023: Student Privacy Rights",
                description="The Nigeria Data Protection Act (NDPA) 2023 provides comprehensive legal protections for personal data. Key rights include: the right to be informed about data collection, right of access to personal data, right to rectification of inaccurate data, right to erasure (right to be forgotten), right to restrict processing, right to data portability, and the right to object to processing.\n\nFor university students, this means institutions must obtain explicit consent before collecting personal data, must protect student records from breaches, and cannot share student data without lawful basis. Section 42 of the Act establishes the NDPC with enforcement powers including the ability to conduct investigations and impose administrative penalties.",
                external_link="https://ndpc.gov.ng/ndpa-2023/",
                relevance_tags="NDPA, data protection, legal rights, consent, student privacy, Nigeria, 2023, Act",
                order=2,
            ),
            Resource(
                category="legal",
                title="Falana & Falana vs Meta Platforms: Landmark Data Privacy Case",
                description="In a landmark legal action, Nigerian law firm Falana & Falana filed a fundamental rights enforcement suit against Meta Platforms (parent company of Facebook, Instagram, and WhatsApp) for alleged privacy violations affecting Nigerian users. The case argues that Meta's data processing practices, including unauthorized sharing of user data and inadequate consent mechanisms, violate Nigerian citizens' constitutional right to privacy under Section 37 of the 1999 Constitution.\n\nThis case sets an important precedent for holding global tech companies accountable under Nigerian privacy law. Nigerian students who experience privacy violations by international platforms can reference this case as an example of legal recourse being pursued at the highest level.",
                external_link="https://www.falanafalana.com/",
                relevance_tags="Falana, Meta, legal case, constitutional rights, privacy, Nigeria, precedent",
                order=3,
            ),
            # === MENTAL HEALTH & WELLBEING ===
            Resource(
                category="mental_health",
                title="Mentally Aware Nigeria Initiative (MANI)",
                description="Mentally Aware Nigeria Initiative (MANI) is a non-profit organization dedicated to improving mental health awareness, advocacy, and support across Nigeria. MANI provides free mental health first aid training, peer support programs, and crisis intervention services. They operate a helpline and online counseling services accessible to students nationwide.\n\nMANI has trained over 50,000 Nigerians in mental health first aid and reaches millions through their digital awareness campaigns. For students experiencing anxiety, depression, or distress related to privacy violations or online harassment, MANI offers a safe and confidential space to speak with trained mental health professionals.",
                external_link="https://mentallyaware.org/",
                relevance_tags="MANI, mental health, counseling, crisis support, Nigeria, online, harassment, anxiety",
                order=4,
            ),
            Resource(
                category="mental_health",
                title="Nigerian Suicide Prevention Hotline",
                description="The Nigerian Suicide Prevention Hotline provides 24/7 crisis support for individuals experiencing suicidal thoughts or emotional distress. Run by trained crisis counselors, this confidential service is available to anyone in Nigeria who needs immediate mental health support.\n\nHotline: 0806 210 6493\n\nIf you are experiencing a mental health crisis, please call immediately. The service is free, confidential, and available 24 hours a day. You do not need to be in immediate danger to call; trained professionals are available to listen and provide support for any level of distress.",
                external_link="tel:08062106493",
                relevance_tags="suicide prevention, crisis, mental health, hotline, Nigeria, 24/7, emergency",
                order=5,
            ),
            Resource(
                category="mental_health",
                title="University Campus Mental Health Services Finder",
                description="Most Nigerian universities have student counseling units or health centers that provide free or low-cost mental health services. These include: individual counseling, group therapy, stress management workshops, and referral services for specialized care.\n\nTo find your campus mental health services:\n1. Visit your university's student affairs office or health center\n2. Ask about confidential counseling services for students\n3. Inquire about peer support programs or student welfare committees\n4. Check if your university has a partnership with external mental health providers\n\nMany universities now also offer online counseling options through telemedicine partnerships.",
                external_link="",
                relevance_tags="campus, university, counseling, mental health, Nigeria, student services, wellness",
                order=6,
            ),
            # === DIGITAL SAFETY GUIDES ===
            Resource(
                category="digital_safety",
                title="Digital Security for Nigerian Students: A Practical Guide",
                description="A comprehensive guide to digital safety for Nigerian university students, covering: creating strong passwords using passphrases, enabling two-factor authentication (2FA) on all accounts, recognizing phishing attempts common in Nigerian academic contexts, securing social media privacy settings, using VPNs safely for academic research, protecting against SIM swap attacks, and securing mobile banking apps.\n\nSpecial attention is given to context-specific threats in Nigeria, including: academic phishing scams targeting university portals, fake scholarship and admission scams, SIM swap fraud targeting mobile money accounts, and social engineering attacks through academic social networks.",
                external_link="",
                relevance_tags="digital safety, cybersecurity, phishing, passwords, 2FA, Nigeria, students, social media",
                order=7,
            ),
            Resource(
                category="digital_safety",
                title="TechHER: Fighting Online Gender-Based Violence in Nigeria",
                description="TechHER is a Nigerian non-profit organization focused on addressing online gender-based violence (OGBV) and promoting digital safety for women and girls in Nigeria. They provide digital safety education, legal support for victims of online harassment, and advocacy for stronger online protections.\n\nTechHER's work includes: training programs on digital self-defense, legal aid referrals for victims of non-consensual image sharing and online stalking, awareness campaigns about sextortion and online grooming, and research on the prevalence and impact of OGBV in Nigerian universities. They are a vital resource for female students experiencing gender-based privacy violations online.",
                external_link="https://techherng.com/",
                relevance_tags="TechHER, gender-based violence, online safety, women, Nigeria, harassment, sextortion, legal aid",
                order=8,
            ),
            Resource(
                category="digital_safety",
                title="Nigeria Computer Emergency Response Team (ngCERT)",
                description="The Nigeria Computer Emergency Response Team (ngCERT) is the national agency responsible for coordinating responses to cybersecurity incidents affecting Nigerian citizens and organizations. ngCERT provides: incident reporting and response coordination, cybersecurity advisories and alerts, vulnerability disclosure coordination, and best practice guidance.\n\nStudents who experience account takeover, data breach, ransomware, or other cybersecurity incidents should report to ngCERT for technical assistance. ngCERT operates under the National Information Technology Development Agency (NITDA) and collaborates with global CERTs for cross-border incident response.",
                external_link="https://www.cert.gov.ng/",
                relevance_tags="ngCERT, cybersecurity, incident response, NITDA, Nigeria, breach, reporting",
                order=9,
            ),
            # === ACADEMIC SUPPORT ===
            Resource(
                category="academic_support",
                title="Nigerian University Privacy and Data Protection Policies",
                description="Many Nigerian universities are developing or updating their data protection policies in response to the NDPA 2023. This resource provides links to publicly available privacy policies, data protection notices, and IT acceptable use policies from Nigerian universities.\n\nStudents should review their own university's data protection policy to understand: how their academic records are processed, what data the university collects about them, who has access to their information, their rights regarding their educational data, and how to report a privacy concern within the institution. If your university does not have a published privacy policy, this may itself be a compliance issue worth raising with the NDPC.",
                external_link="",
                relevance_tags="university policy, data protection, academic, student records, NDPA, compliance",
                order=10,
            ),
            Resource(
                category="academic_support",
                title="Research: Digital Privacy Harms in Nigerian Higher Education",
                description="This academic literature review summarizes current research on digital privacy harms experienced by Nigerian university students. Studies document: the prevalence of unauthorized data sharing by university portals, the impact of social media surveillance by institutions, cases of academic record tampering, the psychological effects of online harassment within academic communities, and the unique vulnerabilities of students in Nigeria's digital ecosystem.\n\nKey findings indicate that students often underreport privacy violations due to: lack of awareness of their rights, fear of institutional retaliation, uncertainty about reporting mechanisms, and normalization of privacy-invasive practices. This research underscores the importance of accessible, confidential incident reporting systems like Mamoru.",
                external_link="",
                relevance_tags="research, academic, literature, privacy harms, Nigerian universities, survey, study",
                order=11,
            ),
            # === CAMPUS RESOURCES ===
            Resource(
                category="campus_resources",
                title="Student Rights and Campus Advocacy Groups",
                description="Student union governments and campus advocacy groups across Nigerian universities play an important role in protecting student rights, including privacy rights. These organizations can provide: peer support for students experiencing privacy violations, advocacy for better institutional data protection practices, awareness campaigns about digital rights, and escalation pathways to university administration.\n\nTo get involved or seek support: contact your Student Union Government (SUG) welfare director, look for campus chapters of digital rights organizations, connect with faculty members who research privacy or technology law, and join student-led initiatives on data protection and digital safety.",
                external_link="",
                relevance_tags="student union, advocacy, campus, rights, SUG, Nigeria, privacy, awareness",
                order=12,
            ),
            Resource(
                category="campus_resources",
                title="ICT Directorates: Reporting Technical Privacy Issues",
                description="University ICT directorates are responsible for managing institutional IT systems, including student portals, learning management systems (LMS), email systems, and campus networks. Students can report technical privacy issues such as: unauthorized access to student records, system vulnerabilities exposing personal data, suspicious emails appearing to come from university systems, and improper data sharing through institutional platforms.\n\nWhen contacting your ICT directorate: document all relevant details (dates, screenshots, communications), reference specific systems involved, keep a record of your report and any response received, and follow up in writing if you do not receive a timely response. If the ICT directorate does not adequately address your concern, escalate to the university's data protection officer (if one exists) or to the NDPC.",
                external_link="",
                relevance_tags="ICT, directorate, university, IT, reporting, technical, data breach, systems",
                order=13,
            ),
            # === EMERGENCY CONTACTS ===
            Resource(
                category="emergency",
                title="Nigeria Police Force: Cybercrime Reporting",
                description="The Nigeria Police Force, through its cybercrime units and the Force Criminal Investigation Department (FCID), accepts reports of cybercrime including: identity theft, online fraud, cyberstalking, non-consensual sharing of intimate images, and hacking. Emergency contact numbers vary by state and command.\n\nFor cybercrime reporting: Visit the nearest police station with cybercrime reporting capability, contact the Nigeria Police Force National Cybercrime Center (NPF-NCCC), or file a report through the police public complaint portal. If you are in immediate danger, call 112 (National Emergency Number). For non-emergency cybercrime reports, the FCID Annex in Alagbon, Lagos, handles specialized cybercrime investigations.",
                external_link="https://www.npf.gov.ng/",
                relevance_tags="police, cybercrime, reporting, emergency, Nigeria, NPF, FCID, NCCC",
                order=14,
            ),
            Resource(
                category="emergency",
                title="National Emergency Number: 112",
                description="112 is the universal emergency number for Nigeria, connecting callers to emergency services including police, fire, and medical assistance. The service operates 24/7 and is free to call from any mobile network in Nigeria. 112 can be dialed even with zero airtime or credit.\n\nUse 112 for: immediate physical danger or threat, ongoing privacy violation involving physical risk (such as stalking or doxxing leading to in-person harassment), medical emergencies related to privacy violation trauma, or any situation requiring immediate response. For non-emergency privacy incidents, use the reporting tools within Mamoru or contact the NDPC.",
                external_link="",
                relevance_tags="emergency, 112, police, ambulance, fire, Nigeria, crisis, immediate",
                order=15,
            ),
            # === GENERAL GUIDANCE ===
            Resource(
                category="general",
                title="What to Do After a Privacy Violation: A Step-by-Step Guide",
                description="A practical guide for Nigerian university students who have experienced a digital privacy violation:\n\n1. Document Everything: Take screenshots, save URLs, record dates and times, and capture any communications related to the incident. This evidence is crucial for any subsequent report.\n\n2. Secure Your Accounts: Change passwords immediately, enable two-factor authentication, review account activity and connected apps, and log out of all active sessions.\n\n3. Use Mamoru to Report: File a detailed incident report through Mamoru. Our structured taxonomy helps classify the harms you experienced and generates a reference code for your records.\n\n4. Seek Support: Contact mental health resources if you are experiencing distress. You are not alone, and taking care of your wellbeing is the priority.\n\n5. Know Your Rights: Under the NDPA 2023, you have the right to lodge a complaint with the NDPC against any data controller who has violated your privacy.\n\n6. Consider Legal Action: For serious violations, consult with a lawyer or legal aid organization about your options for legal recourse.",
                external_link="",
                relevance_tags="guide, steps, what to do, privacy violation, incident response, Nigeria, students",
                order=16,
            ),
            Resource(
                category="general",
                title="Privacy Glossary: Key Terms Every Student Should Know",
                description="A plain-language glossary of important privacy and data protection terms relevant to Nigerian students:\n\nData Controller: The entity (e.g., a university, social media platform, edtech company) that determines how and why personal data is processed.\n\nData Processor: An entity that processes data on behalf of the data controller (e.g., a cloud service provider used by your university).\n\nData Subject: You — the individual whose personal data is being processed.\n\nPersonal Data: Any information relating to an identified or identifiable individual. This includes names, email addresses, student ID numbers, IP addresses, and location data.\n\nConsent: Freely given, specific, informed, and unambiguous permission for data processing.\n\nData Breach: A security incident involving unauthorized access to or disclosure of personal data.\n\nDPA: Data Processing Agreement — a contract between controllers and processors.\n\nDPO: Data Protection Officer — the person within an organization responsible for data protection compliance.",
                external_link="",
                relevance_tags="glossary, privacy terms, data protection, education, Nigeria, student guide, definitions",
                order=17,
            ),
        ]

        created = 0
        for resource in resources:
            _, was_created = Resource.objects.get_or_create(
                title=resource.title,
                defaults={
                    "category": resource.category,
                    "description": resource.description,
                    "external_link": resource.external_link,
                    "relevance_tags": resource.relevance_tags,
                    "order": resource.order,
                    "is_visible": True,
                },
            )
            if was_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(f"Seeded {created} resources ({len(resources) - created} already existed)"))
