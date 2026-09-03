from django.core.management.base import BaseCommand
from resources.models import Resource


class Command(BaseCommand):
    help = "Seed the database with real Nigerian privacy, safety, and wellbeing resources"

    def handle(self, *args, **options):
        resources = [
            # === LEGAL RIGHTS & REPORTING ===
            Resource(
                category="legal",
                title="NDPC Nigeria: Data Protection Complaint Portal",
                description=(
                    "The Nigeria Data Protection Commission (NDPC) is the statutory authority "
                    "established under the Nigeria Data Protection Act 2023 to protect the rights "
                    "of data subjects. Students can lodge formal complaints about privacy "
                    "violations by universities, edtech platforms, banks, or digital services "
                    "through the NDPC online complaint portal. The Commission has the power to "
                    "investigate, issue enforcement notices, and impose administrative fines of "
                    "up to 2% of annual turnover or N20 million, whichever is greater. "
                    "Complaints are free and can be filed anonymously.\n\n"
                    "How to file:\n1. Visit the NDPC portal and select 'Lodge a Complaint'\n"
                    "2. Provide the organisation's name and details of the violation\n"
                    "3. Attach supporting evidence (screenshots, emails, reference codes)\n"
                    "4. The NDPC will acknowledge, review, and potentially investigate the matter."
                ),
                external_link="https://ndpc.gov.ng/",
                contact_phone="",
                relevance_tags="NDPC, legal, complaint, NDPA, enforcement, data protection, Nigeria, regulatory",
                incident_types="unauthorized_access,doxxing,impersonation,data_breach,phishing,account_takeover,surveillance,outing",
                harm_categories="financial_loss,reputation,academic_penalty",
                order=1,
            ),
            Resource(
                category="legal",
                title="Nigerian Data Protection Act 2023: Your Privacy Rights",
                description=(
                    "The Nigeria Data Protection Act (NDPA) 2023 gives every Nigerian data subject "
                    "a comprehensive set of rights, including: the right to be informed about how "
                    "your data is used, the right of access to your personal data, the right to "
                    "rectification of inaccurate data, the right to erasure (the 'right to be "
                    "forgotten'), the right to restrict processing, the right to data portability, "
                    "and the right to object to processing.\n\n"
                    "For university students this means: institutions must obtain explicit consent "
                    "before collecting personal data, must keep student records secure, and cannot "
                    "share student information without a lawful basis. Section 42 establishes the "
                    "NDPC with enforcement powers. If a university or platform violates these "
                    "rights, students may complain to the NDPC and may also seek redress through "
                    "the courts under Section 37 of the 1999 Constitution (right to privacy)."
                ),
                external_link="https://ndpc.gov.ng/ndpa-2023/",
                contact_phone="",
                relevance_tags="NDPA, data protection, legal rights, consent, student privacy, Nigeria, 2023, Act",
                incident_types="unauthorized_access,doxxing,data_breach,account_takeover,impersonation",
                harm_categories="reputation,fear_safety,academic_penalty",
                order=2,
            ),
            Resource(
                category="legal",
                title="Falana & Falana: Landmark Data Privacy Litigation",
                description=(
                    "Falana & Falana is a prominent Nigerian law firm that filed a landmark "
                    "fundamental rights enforcement suit against Meta Platforms over alleged "
                    "privacy violations affecting Nigerian users of Facebook, Instagram, and "
                    "WhatsApp. The case invokes Section 37 of the 1999 Constitution (right to "
                    "privacy) and the NDPA 2023, arguing that inadequate consent mechanisms and "
                    "unauthorised data sharing violate Nigerian law.\n\n"
                    "This is a useful precedent for students considering legal action against "
                    "global platforms. The firm offers consultations on privacy and fundamental "
                    "rights matters and can advise on the viability of a complaint or lawsuit."
                ),
                external_link="https://www.falanafalana.com/",
                contact_phone="",
                relevance_tags="Falana, Meta, legal case, constitutional rights, privacy, Nigeria, precedent, fundamental rights",
                incident_types="doxxing,impersonation,nonconsensual_sharing,surveillance,data_breach",
                harm_categories="reputation,financial_loss,fear_safety",
                order=3,
            ),
            Resource(
                category="legal",
                title="Nigeria Police Force: National Cybercrime Centre (NPF-NCCC)",
                description=(
                    "The Nigeria Police Force National Cybercrime Centre (NPF-NCCC) investigates "
                    "cybercrime offences including identity theft, online fraud, cyberstalking, "
                    "hacking, and non-consensual sharing of intimate images. Victims can file "
                    "complaints in person at NPF-NCCC offices (Force Headquarters, Area 11, Abuja) "
                    "or through the nearest State CID cybercrime desk.\n\n"
                    "What to bring: a written statement, screenshots or evidence of the offence, "
                    "your identification, and any reference codes or correspondence. You are "
                    "entitled to obtain a formal complaint acknowledgement (extract) for your "
                    "records, which is useful for follow-ups."
                ),
                external_link="https://www.npf.gov.ng/",
                contact_phone="",
                relevance_tags="police, cybercrime, NPF, NCCC, reporting, Nigeria, identity theft, fraud",
                incident_types="cyberstalking,impersonation,account_takeover,nonconsensual_sharing,phishing,harassment,doxxing",
                harm_categories="fear_safety,financial_loss,reputation,physical_safety",
                order=4,
            ),
            Resource(
                category="legal",
                title="Nigerian Constitution Section 37: Right to Privacy",
                description=(
                    "Section 37 of the 1999 Constitution of the Federal Republic of Nigeria "
                    "guarantees that 'the privacy of citizens, their homes, correspondence, "
                    "telephone conversations and telegraphic communications is hereby guaranteed "
                    "and protected.' This is the constitutional foundation for all data privacy "
                    "claims in Nigeria.\n\n"
                    "Students whose privacy has been violated can pursue a Fundamental Rights "
                    "Enforcement action in the Federal High Court, even where a statute does not "
                    "specifically address the violation. Legal aid options include the Legal Aid "
                    "Council of Nigeria for eligible students."
                ),
                external_link="https://www.nigerialaw.org/ConstitutionOfTheFederalRepublicOfNigeria.htm",
                contact_phone="",
                relevance_tags="constitution, section 37, privacy, legal, fundamental rights, court, Nigeria",
                incident_types="doxxing,surveillance,outing,nonconsensual_sharing,cyberstalking",
                harm_categories="reputation,fear_safety,humiliation",
                order=5,
            ),
            Resource(
                category="legal",
                title="Legal Aid Council of Nigeria",
                description=(
                    "The Legal Aid Council of Nigeria provides free legal services to Nigerians "
                    "who cannot afford a lawyer, including students. It handles civil and criminal "
                    "matters and can assist with privacy-related complaints, harassment cases, and "
                    "fundamental rights enforcement where the applicant meets the means test.\n\n"
                    "Services include legal advice, representation in court, and referrals. The "
                    "Council has offices in all 36 states and the FCT. Students should bring their "
                    "identification, evidence of the incident, and any police complaint extract."
                ),
                external_link="https://legalaidcouncil.gov.ng/",
                contact_phone="",
                relevance_tags="legal aid, free legal services, Nigeria, court, representation, advice",
                incident_types="doxxing,harassment,cyberstalking,nonconsensual_sharing",
                harm_categories="reputation,financial_loss,physical_safety",
                order=6,
            ),
            Resource(
                category="legal",
                title="Nigeria Data Protection Act: The Right to Erasure (Be Forgotten)",
                description=(
                    "Under the NDPA 2023, data subjects have the right to request the erasure of "
                    "personal data where it is no longer necessary, where consent is withdrawn, or "
                    "where processing is unlawful. This is the legal tool for removing your "
                    "private information, leaked documents, or images from a data controller's "
                    "systems.\n\n"
                    "How to exercise it: 1) Write to the data controller (platform, university, "
                    "school) citing your request, 2) Follow up after 14 days if no response, "
                    "3) Escalate to the NDPC with evidence of the request. Keep copies of all "
                    "correspondence."
                ),
                external_link="https://ndpc.gov.ng/",
                contact_phone="",
                relevance_tags="right to erasure, be forgotten, NDPA, legal, removal, data controller",
                incident_types="doxxing,outing,nonconsensual_sharing,data_breach,impersonation",
                harm_categories="reputation,humiliation,academic_penalty",
                order=7,
            ),
            # === MENTAL HEALTH & WELLBEING ===
            Resource(
                category="mental_health",
                title="Mentally Aware Nigeria Initiative (MANI)",
                description=(
                    "Mentally Aware Nigeria Initiative (MANI) is a non-profit providing free mental "
                    "health first aid, peer support, and crisis counselling for Nigerians. MANI "
                    "offers a confidential helpline, WhatsApp counselling, and online support "
                    "groups. It has trained over 50,000 Nigerians in mental health first aid.\n\n"
                    "MANI is an appropriate first point of contact for students experiencing "
                    "anxiety, distress, depression, or trauma related to online harassment, "
                    "doxxing, or cyberstalking. Support is free, confidential, and student-friendly."
                ),
                external_link="https://mentallyaware.org/",
                contact_phone="0906 336 6263",
                relevance_tags="MANI, mental health, counselling, crisis support, Nigeria, harassment, anxiety",
                incident_types="harassment,cyberstalking,doxxing,nonconsensual_sharing,revenge_porn",
                harm_categories="anxiety,distress,ptsd_symptoms,isolation,self_blame,humiliation,loss_trust",
                order=8,
            ),
            Resource(
                category="mental_health",
                title="Nigerian Suicide Prevention Hotline (24/7)",
                description=(
                    "The Nigerian Suicide Prevention Hotline provides 24/7 crisis intervention for "
                    "anyone experiencing suicidal thoughts or severe emotional distress. The "
                    "service is free, confidential, and staffed by trained crisis counsellors.\n\n"
                    "Call: 0806 210 6493 (24 hours, 7 days a week). You do not need to be in "
                    "immediate danger to call, trained professionals are available to listen and "
                    "support any level of distress. If you are a FUT Minna student in crisis, you "
                    "can also contact the University Counselling and Career Unit during office hours."
                ),
                external_link="tel:08062106493",
                contact_phone="0806 210 6493",
                relevance_tags="suicide prevention, crisis, mental health, hotline, Nigeria, 24/7, emergency",
                incident_types="harassment,cyberstalking,doxxing,revenge_porn,nonconsensual_sharing,surveillance",
                harm_categories="ptsd_symptoms,distress,anxiety,isolation,self_blame",
                order=9,
            ),
            Resource(
                category="mental_health",
                title="The Asido Foundation: Student Mental Health Support",
                description=(
                    "The Asido Foundation is a Nigerian mental health advocacy organisation focused "
                    "on young people and students. It runs the 'Asido Campus Network' across "
                    "Nigerian universities, training peer counsellors and raising awareness about "
                    "depression, anxiety, and the stigma of seeking help.\n\n"
                    "Students can access educational resources, attend campus mental health "
                    "programmes, and connect with trained peer supporters. Asido also runs free "
                    "online mental health first aid trainings suitable for students affected by "
                    "online abuse."
                ),
                external_link="https://theasidofoundation.org/",
                contact_phone="",
                relevance_tags="Asido, mental health, students, campus, awareness, peer support, Nigeria",
                incident_types="harassment,cyberstalking,doxxing",
                harm_categories="anxiety,distress,isolation,academic_anxiety,self_blame",
                order=10,
            ),
            Resource(
                category="mental_health",
                title="She Writes Woman: Survivor Support for Gender-Based Violence",
                description=(
                    "She Writes Woman (SWW) is a Nigerian not-for-profit that provides psychosocial "
                    "and legal support to survivors of sexual and gender-based violence (SGBV), "
                    "including non-consensual image sharing and online harassment targeted at "
                    "women. They operate a helpline and a survivor support centre.\n\n"
                    "SWW offers confidential counselling, safety planning, and referrals to medical "
                    "and legal services. It is a relevant resource for female students who have "
                    "experienced online gender-based violence."
                ),
                external_link="https://www.shewriteswoman.com/",
                contact_phone="",
                relevance_tags="She Writes Woman, SGBV, survivors, support, gender-based violence, Nigeria",
                incident_types="nonconsensual_sharing,revenge_porn,harassment,cyberstalking,outing",
                harm_categories="ptsd_symptoms,distress,humiliation,isolation,fear_safety",
                order=11,
            ),
            # === DIGITAL SAFETY GUIDES ===
            Resource(
                category="digital_safety",
                title="Paradigm Initiative (PIN): Digital Rights in Nigeria",
                description=(
                    "Paradigm Initiative (PIN) is a pan-African social enterprise working on "
                    "digital rights and inclusion. It produces the 'Londa' annual report on digital "
                    "rights in Africa and provides the DIAL (Digital Inclusion and Access Lab) "
                    "which offers digital security training and incident support for individuals "
                    "and civil society.\n\n"
                    "PIN's resources help students understand surveillance, censorship, and online "
                    "privacy threats, and offer practical guidance on secure communication and "
                    "data protection."
                ),
                external_link="https://paradigmhq.org/",
                contact_phone="",
                relevance_tags="Paradigm Initiative, PIN, digital rights, digital security, surveillance, Nigeria, Africa",
                incident_types="surveillance,data_breach,unauthorized_access,account_takeover",
                harm_categories="loss_trust,fear_safety,anxiety",
                order=12,
            ),
            Resource(
                category="digital_safety",
                title="ngCERT: Nigeria Computer Emergency Response Team",
                description=(
                    "The Nigeria Computer Emergency Response Team (ngCERT), operating under NITDA, "
                    "coordinates national responses to cybersecurity incidents. It issues "
                    "advisories, publishes vulnerability alerts, and accepts incident reports "
                    "affecting Nigerian citizens and organisations.\n\n"
                    "Students affected by account takeover, phishing, data breaches, or malware can "
                    "report incidents to ngCERT for technical assistance and to help prevent the "
                    "same attacks affecting others. Include any technical details (affected "
                    "platform, timestamps, error messages)."
                ),
                external_link="https://www.cert.gov.ng/",
                contact_phone="",
                relevance_tags="ngCERT, cybersecurity, incident response, NITDA, Nigeria, breach, phishing",
                incident_types="phishing,account_takeover,data_breach,unauthorized_access,impersonation",
                harm_categories="financial_loss,loss_trust,anxiety",
                order=13,
            ),
            Resource(
                category="digital_safety",
                title="TechHER: Fighting Online Gender-Based Violence in Nigeria",
                description=(
                    "TechHER is a Nigerian non-profit addressing online gender-based violence "
                    "(OGBV) and promoting digital safety for women and girls. They provide digital "
                    "safety education, legal aid referrals, and advocacy.\n\n"
                    "Their programmes cover non-consensual image sharing, online stalking, "
                    "sextortion, and grooming. TechHER also supports victims in securing their "
                    "accounts and taking down harmful content."
                ),
                external_link="https://techherng.com/",
                contact_phone="",
                relevance_tags="TechHER, gender-based violence, online safety, women, Nigeria, sextortion, legal aid",
                incident_types="nonconsensual_sharing,revenge_porn,harassment,cyberstalking,outing",
                harm_categories="fear_safety,humiliation,reputation,distress",
                order=14,
            ),
            Resource(
                category="digital_safety",
                title="Google Safety Center: Practical Account Security Guides",
                description=(
                    "The Google Safety Center offers step-by-step guides to protect Google "
                    "accounts, Gmail, and Android devices. These are directly useful after "
                    "phishing, account takeover, or unauthorised access incidents, and include "
                    "checking for suspicious activity, running a security check-up, enabling "
                    "two-factor authentication, and signing out of unknown devices.\n\n"
                    "The steps are free and apply to the most commonly used email and device "
                    "ecosystem among Nigerian students."
                ),
                external_link="https://safety.google/security/",
                contact_phone="",
                relevance_tags="Google, safety, account security, 2FA, phishing, recovery, Gmail",
                incident_types="phishing,account_takeover,unauthorized_access,impersonation",
                harm_categories="financial_loss,loss_trust,anxiety",
                order=15,
            ),
            Resource(
                category="digital_safety",
                title="Take It Down: Remove Non-Consensual Intimate Images",
                description=(
                    "Take It Down is a free service that helps individuals prevent the online "
                    "distribution of intimate images taken without consent (including images taken "
                    "of a minor). Operated by the National Center for Missing & Exploited Children, "
                    "it works with participating platforms to block and remove such content.\n\n"
                    "You provide a hash of the image, not the image itself, so your privacy is "
                    "protected. This is a first-line technical response for non-consensual image "
                    "sharing before or alongside legal action."
                ),
                external_link="https://takeitdown.ncmec.org/",
                contact_phone="",
                relevance_tags="Take It Down, intimate images, non-consensual, removal, hash, NCMEC",
                incident_types="nonconsensual_sharing,revenge_porn,outing",
                harm_categories="humiliation,reputation,ptsd_symptoms,fear_safety",
                order=16,
            ),
            # === ACADEMIC SUPPORT ===
            Resource(
                category="academic_support",
                title="FUT Minna Counselling and Career Unit",
                description=(
                    "The Federal University of Technology Minna Counselling and Career Unit offers "
                    "free, confidential counselling to students facing emotional, academic, or "
                    "social difficulties, including the aftermath of online harassment, doxxing, "
                    "and cyberstalking. The unit supports students in managing distress, restoring "
                    "focus on studies, and navigating academic consequences.\n\n"
                    "Students can walk in during office hours or request an appointment through the "
                    "Students' Affairs Division. Services are confidential and free."
                ),
                external_link="",
                contact_phone="",
                relevance_tags="FUT Minna, counselling, career, student affairs, wellness, campus",
                incident_types="harassment,cyberstalking,doxxing,academic_penalty",
                harm_categories="academic_anxiety,distress,anxiety,isolation,academic_penalty,lost_opportunity",
                order=17,
            ),
            Resource(
                category="academic_support",
                title="FUT Minna Students' Affairs Division",
                description=(
                    "The Students' Affairs Division at FUT Minna administers student welfare, "
                    "discipline, and grievance processes. Students experiencing harassment by "
                    "other students or staff, or academic retaliation linked to an incident, can "
                    "file a formal complaint here. The Division also oversees the Students' Union "
                    "and welfare officers who can provide support and advocacy.\n\n"
                    "Document your complaint in writing, attach evidence, and request a formal "
                    "acknowledgement. The Division can refer matters to the ICT Directorate, the "
                    "Dean of Students, or the University's management as appropriate."
                ),
                external_link="",
                contact_phone="",
                relevance_tags="FUT Minna, student affairs, welfare, grievance, complaint, dean of students",
                incident_types="harassment,academic_penalty,outing,doxxing",
                harm_categories="academic_penalty,reputation,social_ostracism,academic_anxiety",
                order=18,
            ),
            Resource(
                category="academic_support",
                title="FUT Minna ICT Directorate: Reporting Technical Privacy Issues",
                description=(
                    "The ICT Directorate at FUT Minna manages the student portal, learning "
                    "management system, email systems, and campus network. Students should report "
                    "technical privacy issues here: unauthorised access to portal accounts, "
                    "suspicious emails claiming to be from the university, system vulnerabilities "
                    "exposing personal data, or improper data sharing through institutional "
                    "platforms.\n\n"
                    "When reporting: document dates, screenshots, and affected systems; keep a "
                    "record of your report; and follow up in writing. If the issue is not resolved, "
                    "escalate to the University's Data Protection Officer (if designated) or the NDPC."
                ),
                external_link="",
                contact_phone="",
                relevance_tags="FUT Minna, ICT, directorate, portal, reporting, technical, data breach",
                incident_types="unauthorized_access,data_breach,phishing,account_takeover,surveillance",
                harm_categories="financial_loss,academic_penalty,loss_trust",
                order=19,
            ),
            Resource(
                category="academic_support",
                title="FUT Minna Security Division (Campus Safety)",
                description=(
                    "The FUT Minna Security Division provides campus-wide physical security and "
                    "responds to threats on and around the Gidan Kwano and Bosso campuses. Students "
                    "facing physical danger linked to online incidents, such as doxxing that "
                    "reveals their hostel location, or cyberstalking escalating to in-person "
                    "contact, should report to the Security Division immediately and, if in "
                    "immediate danger, call 112.\n\n"
                    "Contact the Security Division control room (available 24/7) or visit their "
                    "office at either campus."
                ),
                external_link="",
                contact_phone="",
                relevance_tags="FUT Minna, security, campus safety, physical danger, emergency",
                incident_types="doxxing,cyberstalking,harassment,nonconsensual_sharing",
                harm_categories="physical_safety,fear_safety",
                order=20,
            ),
            # === CAMPUS RESOURCES ===
            Resource(
                category="campus_resources",
                title="Student Rights and Campus Advocacy Groups",
                description=(
                    "Student union governments and campus advocacy groups across Nigerian "
                    "universities play an important role in protecting student rights, including "
                    "privacy rights. These groups provide peer support, advocate for better "
                    "institutional data protection, run awareness campaigns, and offer escalation "
                    "pathways to university administration.\n\n"
                    "To seek support: contact your Student Union Government (SUG) welfare director, "
                    "join campus chapters of digital rights organisations, and connect with faculty "
                    "who research privacy or technology law."
                ),
                external_link="",
                contact_phone="",
                relevance_tags="student union, SUG, advocacy, campus, rights, privacy, awareness",
                incident_types="harassment,doxxing,outing,social_ostracism",
                harm_categories="social_ostracism,reputation,academic_penalty",
                order=21,
            ),
            Resource(
                category="campus_resources",
                title="FUT Minna Health Centre (Gidan Kwano & Bosso)",
                description=(
                    "The FUT Minna University Health Centre provides primary healthcare, medical "
                    "certificates, and basic mental health assessment to students. Following a "
                    "traumatic online incident, students can attend the Health Centre for a medical "
                    "review, request a referral for specialist mental health care, and obtain "
                    "documentation that may be useful for academic accommodations.\n\n"
                    "The centre is located on both campuses; bring your student ID. A medical "
                    "certificate can support a formal request for extensions or academic "
                    "consideration after an incident."
                ),
                external_link="",
                contact_phone="",
                relevance_tags="FUT Minna, health centre, medical, clinic, wellness, referral",
                incident_types="harassment,cyberstalking,nonconsensual_sharing,doxxing",
                harm_categories="ptsd_symptoms,distress,physical_safety,academic_penalty",
                order=22,
            ),
            # === EMERGENCY CONTACTS ===
            Resource(
                category="emergency",
                title="National Emergency Number: 112",
                description=(
                    "112 is the universal emergency number in Nigeria, connecting callers to "
                    "police, fire, and medical services. It operates 24/7, is free to call from any "
                    "network, and works even with zero airtime or credit.\n\n"
                    "Use 112 for: immediate physical danger, an ongoing violation that involves "
                    "physical risk (e.g. stalking or doxxing leading to in-person threats), a "
                    "medical emergency, or any situation requiring an immediate response. For "
                    "non-emergency privacy incidents, use PrivGuard's reporting tools or the NDPC."
                ),
                external_link="",
                contact_phone="112",
                relevance_tags="emergency, 112, police, ambulance, fire, Nigeria, crisis, immediate",
                incident_types="cyberstalking,harassment,doxxing,physical_safety",
                harm_categories="physical_safety,fear_safety,ptsd_symptoms",
                order=23,
            ),
            Resource(
                category="emergency",
                title="Nigeria Police Force: Emergency & Cybercrime Hotlines",
                description=(
                    "The Nigeria Police Force provides a national emergency line (0800 1999 0000, "
                    "toll-free) and operates cybercrime units at the Force Headquarters and in "
                    "state commands. For immediate police assistance on campus or elsewhere, call "
                    "the emergency line or visit the nearest police station.\n\n"
                    "For online offences, identity theft, fraud, cyberstalking, non-consensual "
                    "image sharing, file a formal complaint at the cybercrime desk and request a "
                    "written acknowledgement. Keep all evidence and reference codes."
                ),
                external_link="https://www.npf.gov.ng/",
                contact_phone="0800 1999 0000",
                relevance_tags="police, NPF, emergency, cybercrime, hotline, Nigeria, 24/7",
                incident_types="cyberstalking,impersonation,harassment,nonconsensual_sharing,account_takeover,phishing",
                harm_categories="fear_safety,physical_safety,financial_loss",
                order=24,
            ),
            Resource(
                category="emergency",
                title="NAPTIP: National Agency for the Prohibition of Trafficking in Persons",
                description=(
                    "NAPTIP is the Federal agency responsible for human trafficking and related "
                    "offences, and it also handles cases of internet-facilitated sexual exploitation "
                    "and severe online abuse. NAPTIP provides victim support, counselling, and "
                    "referral for survivors.\n\n"
                    "Victims of sextortion, online grooming, or severe exploitation can contact "
                    "NAPTIP's national helpline. Reports are treated with confidentiality."
                ),
                external_link="https://naptip.gov.ng/",
                contact_phone="0800 627 847",
                relevance_tags="NAPTIP, trafficking, exploitation, sextortion, victim support, Nigeria, helpline",
                incident_types="nonconsensual_sharing,revenge_porn,harassment,cyberstalking",
                harm_categories="fear_safety,physical_safety,ptsd_symptoms,distress",
                order=25,
            ),
            # === GENERAL GUIDANCE ===
            Resource(
                category="general",
                title="What to Do After a Privacy Violation: A Step-by-Step Guide",
                description=(
                    "A practical guide for Nigerian university students who have experienced a "
                    "digital privacy violation:\n\n"
                    "1. Document Everything, take screenshots, save URLs, record dates and times, "
                    "and capture communications. Evidence is crucial for any report.\n"
                    "2. Secure Your Accounts, change passwords immediately, enable two-factor "
                    "authentication, review connected apps, and sign out of all sessions.\n"
                    "3. Report on PrivGuard, file a detailed incident report; your structured "
                    "report generates a reference code for your records.\n"
                    "4. Seek Support, if you are distressed, contact mental health resources such "
                    "as MANI or the campus counselling unit.\n"
                    "5. Know Your Rights, under the NDPA 2023 you may complain to the NDPC, and "
                    "Section 37 of the Constitution protects your privacy.\n"
                    "6. Consider Reporting to Police, for criminal conduct (fraud, stalking, "
                    "non-consensual image sharing), report to the NPF-NCCC.\n"
                    "7. For immediate danger, call 112."
                ),
                external_link="",
                contact_phone="",
                relevance_tags="guide, steps, what to do, privacy violation, incident response, Nigeria, students",
                incident_types="doxxing,harassment,cyberstalking,impersonation,phishing,account_takeover,nonconsensual_sharing,unauthorized_access,data_breach,surveillance,outing,revenge_porn",
                harm_categories="anxiety,distress,reputation,loss_trust,isolation",
                order=26,
            ),
            Resource(
                category="general",
                title="Privacy Glossary: Key Terms Every Student Should Know",
                description=(
                    "A plain-language glossary of important privacy and data protection terms:\n\n"
                    "Data Controller: the entity (university, platform, edtech company) that decides "
                    "how and why personal data is processed.\n"
                    "Data Processor: an entity that processes data on behalf of a controller (e.g. "
                    "a cloud provider used by your university).\n"
                    "Data Subject: you, the individual whose personal data is processed.\n"
                    "Personal Data: any information relating to an identified or identifiable "
                    "individual (name, email, student ID, IP address, location).\n"
                    "Consent: freely given, specific, informed, and unambiguous permission for "
                    "processing.\n"
                    "Data Breach: a security incident involving unauthorised access to or "
                    "disclosure of personal data.\n"
                    "DPO: Data Protection Officer, the person responsible for an organisation's "
                    "data protection compliance.\n"
                    "DPA: Data Processing Agreement between controllers and processors."
                ),
                external_link="",
                contact_phone="",
                relevance_tags="glossary, privacy terms, data protection, education, Nigeria, student guide, definitions",
                incident_types="doxxing,data_breach,unauthorized_access,impersonation,phishing",
                harm_categories="loss_trust,anxiety",
                order=27,
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
                    "contact_phone": resource.contact_phone,
                    "relevance_tags": resource.relevance_tags,
                    "incident_types": resource.incident_types,
                    "harm_categories": resource.harm_categories,
                    "order": resource.order,
                    "is_visible": True,
                },
            )
            if was_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(
            f"Seeded {created} resources ({len(resources) - created} already existed)"
        ))
