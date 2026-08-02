"""PDF report generation for incident documentation using ReportLab."""
import io
import re
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import (
    BaseDocTemplate, SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, NextPageTemplate, Frame, PageTemplate, KeepTogether,
)
from reportlab.lib import colors
from reportlab.platypus.doctemplate import _doNothing


TERRACOTTA = HexColor("#C75B39")
CHARCOAL = HexColor("#2D2D2D")
GRAPHITE = HexColor("#4A4A4A")
LIGHT_GREY = HexColor("#F5F3EE")
MID_GREY = HexColor("#E4E0D9")


REDACTED_MARKER = "[REDACTED]"


def should_conceal(incident):
    """True when the reporter's identity must be hidden in an export."""
    return bool(incident.concealment_active)


def redact_identity(text, incident):
    """Replace the reporter's identifiable details with a redaction marker.

    Scans free-text fields (narrative, actor description, harm elaborations,
    evidence reference) for the reporter's email, full name and institution and
    replaces them so exported reports never leak the reporter's identity when
    concealment is active.
    """
    if not text:
        return text
    user = incident.user
    markers = []
    if user:
        if user.email:
            markers.append(user.email)
        if user.full_name:
            markers.append(user.full_name)
        if user.institution:
            markers.append(user.institution)
    for marker in markers:
        if marker and len(marker.strip()) >= 3:
            text = re.sub(re.escape(marker), REDACTED_MARKER, text, flags=re.IGNORECASE)
    return text


def _cover_page_footer(canvas, doc):
    """Draw footer on cover page only."""
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(HexColor("#999999"))
    canvas.drawCentredString(
        A4[0] / 2, 15 * mm,
        "PrivGuard Privacy Incident Reporting System"
    )
    canvas.restoreState()


def _content_page_template(canvas, doc):
    """Draw header and footer on content pages."""
    canvas.saveState()
    width, height = A4

    canvas.setStrokeColor(TERRACOTTA)
    canvas.setLineWidth(0.5)
    canvas.line(20 * mm, height - 15 * mm, width - 20 * mm, height - 15 * mm)

    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(HexColor("#999999"))
    canvas.drawString(20 * mm, height - 13 * mm, "PrivGuard Privacy Incident Reports")
    canvas.drawRightString(width - 20 * mm, height - 13 * mm, f"Page {doc.page}")

    canvas.setStrokeColor(MID_GREY)
    canvas.line(20 * mm, 18 * mm, width - 20 * mm, 18 * mm)
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(HexColor("#AAAAAA"))
    canvas.drawCentredString(
        width / 2, 13 * mm,
        "Confidential. Handle with care."
    )
    canvas.restoreState()


def generate_incident_report(incident, conceal=None):
    """Generates a PDF byte stream for a given incident report.

    ``conceal`` defaults to the incident's concealment state and, when active,
    the reporter's identity is redacted from the exported document.
    """
    if conceal is None:
        conceal = should_conceal(incident)
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "IncidentTitle",
        parent=styles["Heading1"],
        textColor=CHARCOAL,
        fontSize=20,
        spaceAfter=6,
        spaceBefore=0,
    )
    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        textColor=GRAPHITE,
        fontSize=10,
        spaceAfter=12,
    )
    section_style = ParagraphStyle(
        "SectionHead",
        parent=styles["Heading2"],
        textColor=TERRACOTTA,
        fontSize=14,
        spaceAfter=8,
        spaceBefore=16,
    )
    label_style = ParagraphStyle(
        "Label",
        parent=styles["Normal"],
        textColor=GRAPHITE,
        fontSize=10,
        fontName="Helvetica-Bold",
        spaceAfter=2,
    )
    value_style = ParagraphStyle(
        "Value",
        parent=styles["Normal"],
        textColor=CHARCOAL,
        fontSize=11,
        spaceAfter=8,
        leading=16,
    )
    footer_style = ParagraphStyle(
        "Footer",
        parent=styles["Normal"],
        textColor=HexColor("#888888"),
        fontSize=8,
        alignment=1,
    )

    elements = []

    elements.append(Paragraph("Privacy Incident Report", title_style))
    elements.append(Paragraph(
        f"Reference: {incident.reference_code} &nbsp;|&nbsp; "
        f"Generated: {datetime.now().strftime('%d %B %Y, %H:%M')}",
        subtitle_style,
    ))
    elements.append(HRFlowable(width="100%", color=TERRACOTTA, thickness=1))
    elements.append(Spacer(1, 6 * mm))

    elements.append(Paragraph("Incident Details", section_style))

    details = [
        ("Platform", incident.get_platform_category_display()),
        ("Date of Occurrence", incident.date_of_occurrence.strftime("%d %B %Y")),
        ("Classification", incident.get_incident_classification_display()),
        ("Actor Involvement", incident.get_actor_involvement_display()),
        ("Severity Rating", incident.get_severity_rating_display()),
    ]
    if incident.platform_name:
        details.insert(1, ("Specific Platform", incident.platform_name))
    if incident.actor_description:
        actor_desc = (
            redact_identity(incident.actor_description, incident)
            if conceal else incident.actor_description
        )
        details.append(("Actor Description", actor_desc))

    for label, value in details:
        elements.append(Paragraph(label, label_style))
        elements.append(Paragraph(str(value), value_style))

    if conceal:
        elements.append(Paragraph(
            f'<font color="#C75B39">&#128274; Identity concealment enabled &mdash; '
            f'reporter details have been redacted.</font>',
            value_style,
        ))

    elements.append(Paragraph("Incident Description", section_style))
    narrative = redact_identity(incident.narrative, incident) if conceal else incident.narrative
    elements.append(Paragraph(narrative, value_style))

    harms = incident.harms.all()
    if harms:
        elements.append(Paragraph("Harm Classification", section_style))
        harm_data = [[
            Paragraph("Harm Category", label_style),
            Paragraph("Severity", label_style),
            Paragraph("Duration", label_style),
        ]]
        for h in harms:
            harm_data.append([
                Paragraph(h.get_harm_category_display(), value_style),
                Paragraph(h.get_severity_score_display(), value_style),
                Paragraph(h.get_duration_display(), value_style),
            ])
            if h.elaboration:
                elaboration = (
                    redact_identity(h.elaboration, incident)
                    if conceal else h.elaboration
                )
                harm_data.append([
                    Paragraph(f"<i>{elaboration}</i>", ParagraphStyle(
                        "Elab", parent=value_style, fontSize=9, textColor=GRAPHITE,
                    )),
                    "", "",
                ])

        if len(harm_data) > 1:
            col_widths = [180, 120, 120]
            table = Table(harm_data, colWidths=col_widths)
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), TERRACOTTA),
                ("TEXTCOLOR", (0, 0), (-1, 0), white),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#DDDDDD")),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ]))
            elements.append(table)

    if incident.evidence_file:
        elements.append(Paragraph("Evidence", section_style))
        if conceal:
            evidence_ref = REDACTED_MARKER
        else:
            evidence_ref = incident.evidence_url or f"{incident.evidence_file.name}"
        elements.append(Paragraph(
            f"Evidence file attached: {evidence_ref}",
            value_style,
        ))

    elements.append(Spacer(1, 10 * mm))
    elements.append(HRFlowable(width="100%", color=HexColor("#CCCCCC"), thickness=0.5))
    elements.append(Spacer(1, 3 * mm))
    elements.append(Paragraph(
        "This report is generated by PrivGuard Privacy Incident Reporting System. "
        "This document contains sensitive personal information and should be handled with confidentiality.",
        footer_style,
    ))

    doc.build(elements)
    buffer.seek(0)
    return buffer


def generate_bulk_report(incidents):
    """Generates a multi-page PDF with each incident on its own page."""
    buffer = io.BytesIO()
    count = incidents.count()
    now = datetime.now().strftime("%d %B %Y, %H:%M")

    width, height = A4
    cover_frame = Frame(
        25 * mm, 25 * mm,
        width - 50 * mm, height - 50 * mm,
        id="cover"
    )
    content_frame = Frame(
        20 * mm, 22 * mm,
        width - 40 * mm, height - 42 * mm,
        id="content"
    )

    doc = BaseDocTemplate(
        buffer,
        pagesize=A4,
        title="PrivGuard Privacy Incident Reports",
        author="PrivGuard System",
    )

    cover_template = PageTemplate(
        id="cover",
        frames=[cover_frame],
        onPage=_cover_page_footer,
    )
    content_template = PageTemplate(
        id="content",
        frames=[content_frame],
        onPage=_content_page_template,
    )
    doc.addPageTemplates([cover_template, content_template])

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "CoverTitle",
        parent=styles["Title"],
        textColor=CHARCOAL,
        fontSize=28,
        fontName="Helvetica-Bold",
        spaceAfter=8,
        alignment=0,
        leading=34,
    )
    subtitle_style = ParagraphStyle(
        "CoverSubtitle",
        parent=styles["Normal"],
        textColor=GRAPHITE,
        fontSize=12,
        spaceAfter=6,
        leading=18,
    )
    section_style = ParagraphStyle(
        "SectionHead",
        parent=styles["Heading2"],
        textColor=TERRACOTTA,
        fontSize=14,
        spaceAfter=8,
        spaceBefore=14,
        fontName="Helvetica-Bold",
    )
    detail_header_style = ParagraphStyle(
        "DetailHeader",
        parent=styles["Heading2"],
        textColor=CHARCOAL,
        fontSize=13,
        spaceAfter=6,
        spaceBefore=10,
        fontName="Helvetica-Bold",
    )
    label_style = ParagraphStyle(
        "Label",
        parent=styles["Normal"],
        textColor=GRAPHITE,
        fontSize=9,
        fontName="Helvetica-Bold",
        spaceAfter=1,
        spaceBefore=0,
    )
    value_style = ParagraphStyle(
        "Value",
        parent=styles["Normal"],
        textColor=CHARCOAL,
        fontSize=10,
        spaceAfter=10,
        leading=15,
    )
    narrative_style = ParagraphStyle(
        "Narrative",
        parent=styles["Normal"],
        textColor=CHARCOAL,
        fontSize=10,
        spaceAfter=8,
        leading=16,
        firstLineIndent=0,
    )
    report_num_style = ParagraphStyle(
        "ReportNum",
        parent=styles["Normal"],
        textColor=TERRACOTTA,
        fontSize=9,
        fontName="Helvetica-Bold",
        spaceAfter=4,
    )
    toc_style = ParagraphStyle(
        "TOC",
        parent=styles["Normal"],
        textColor=CHARCOAL,
        fontSize=9,
        spaceAfter=3,
        leading=14,
    )
    toc_head_style = ParagraphStyle(
        "TOCHead",
        parent=styles["Heading2"],
        textColor=TERRACOTTA,
        fontSize=14,
        spaceAfter=10,
        fontName="Helvetica-Bold",
    )
    footer_style = ParagraphStyle(
        "PageFooter",
        parent=styles["Normal"],
        textColor=HexColor("#999999"),
        fontSize=8,
        alignment=1,
    )
    small_style = ParagraphStyle(
        "Small",
        parent=styles["Normal"],
        textColor=GRAPHITE,
        fontSize=9,
        spaceAfter=4,
        leading=13,
    )

    elements = []

    # =================== COVER PAGE ===================
    elements.append(NextPageTemplate("cover"))
    elements.append(Spacer(1, 50 * mm))
    elements.append(Paragraph("PRIVGUARD", ParagraphStyle(
        "BrandMark",
        parent=styles["Normal"],
        textColor=TERRACOTTA,
        fontSize=14,
        fontName="Helvetica-Bold",
        spaceAfter=4,
        letterSpacing=4,
    )))
    elements.append(Paragraph("Privacy Incident Reports", title_style))
    elements.append(Spacer(1, 4 * mm))
    elements.append(HRFlowable(width="40%", color=TERRACOTTA, thickness=2, hAlign="LEFT"))
    elements.append(Spacer(1, 8 * mm))
    elements.append(Paragraph(
        f"Bulk Export  |  {count} incident report{'s' if count != 1 else ''}",
        subtitle_style,
    ))
    elements.append(Paragraph(f"Generated: {now}", subtitle_style))
    elements.append(Spacer(1, 30 * mm))
    elements.append(Paragraph(
        "This document contains confidential privacy incident reports generated "
        "by the PrivGuard Privacy Incident Reporting System. All information contained "
        "herein is sensitive and should be handled with appropriate confidentiality.",
        ParagraphStyle(
            "Disclaimer",
            parent=styles["Normal"],
            textColor=GRAPHITE,
            fontSize=9,
            leading=15,
            spaceAfter=6,
        ),
    ))
    elements.append(Paragraph(
        "Nigeria Data Protection Act 2023 compliant",
        ParagraphStyle(
            "Compliance",
            parent=styles["Normal"],
            textColor=TERRACOTTA,
            fontSize=8,
            fontName="Helvetica-Bold",
        ),
    ))

    # =================== TABLE OF CONTENTS ===================
    elements.append(NextPageTemplate("content"))
    elements.append(PageBreak())
    elements.append(Paragraph("Table of Contents", toc_head_style))
    elements.append(HRFlowable(width="100%", color=MID_GREY, thickness=0.5))
    elements.append(Spacer(1, 6 * mm))

    toc_data = [[
        Paragraph("<b>#</b>", ParagraphStyle("TH", parent=label_style, textColor=white, fontSize=8)),
        Paragraph("<b>Reference</b>", ParagraphStyle("TH", parent=label_style, textColor=white, fontSize=8)),
        Paragraph("<b>Classification</b>", ParagraphStyle("TH", parent=label_style, textColor=white, fontSize=8)),
        Paragraph("<b>Severity</b>", ParagraphStyle("TH", parent=label_style, textColor=white, fontSize=8)),
        Paragraph("<b>Platform</b>", ParagraphStyle("TH", parent=label_style, textColor=white, fontSize=8)),
        Paragraph("<b>Date</b>", ParagraphStyle("TH", parent=label_style, textColor=white, fontSize=8)),
    ]]
    for idx, inc in enumerate(incidents, 1):
        toc_data.append([
            Paragraph(str(idx), toc_style),
            Paragraph(inc.reference_code, ParagraphStyle("TC", parent=toc_style, fontName="Helvetica-Bold")),
            Paragraph(inc.get_incident_classification_display(), toc_style),
            Paragraph(inc.get_severity_rating_display(), toc_style),
            Paragraph(inc.get_platform_category_display(), toc_style),
            Paragraph(inc.date_of_occurrence.strftime("%d %b %Y"), toc_style),
        ])

    if len(toc_data) > 1:
        toc_table = Table(toc_data, colWidths=[25, 75, 130, 70, 80, 65])
        toc_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), TERRACOTTA),
            ("TEXTCOLOR", (0, 0), (-1, 0), white),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("GRID", (0, 0), (-1, -1), 0.5, MID_GREY),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, LIGHT_GREY]),
        ]))
        elements.append(toc_table)

    elements.append(Spacer(1, 10 * mm))
    elements.append(Paragraph(
        f"This index covers {count} incident report{'s' if count != 1 else ''}. "
        "Each report begins on a separate page for clarity and ease of reference.",
        small_style,
    ))

    # =================== INDIVIDUAL INCIDENT PAGES ===================
    for idx, inc in enumerate(incidents, 1):
        elements.append(PageBreak())
        conceal = should_conceal(inc)

        elements.append(Paragraph(
            f"INCIDENT REPORT {idx} OF {count}",
            report_num_style,
        ))
        elements.append(Paragraph(
            f"Reference: {inc.reference_code}",
            ParagraphStyle("Ref", parent=subtitle_style, fontSize=14, fontName="Helvetica-Bold", textColor=CHARCOAL),
        ))
        elements.append(HRFlowable(width="100%", color=TERRACOTTA, thickness=1.5))
        elements.append(Spacer(1, 4 * mm))

        # Incident details in a two column table layout
        details_left = [
            ("Platform", inc.get_platform_category_display()),
            ("Date of Occurrence", inc.date_of_occurrence.strftime("%d %B %Y")),
            ("Classification", inc.get_incident_classification_display()),
            ("Actor Involvement", inc.get_actor_involvement_display()),
        ]
        details_right = [
            ("Severity Rating", inc.get_severity_rating_display()),
            ("Status", inc.get_status_display()),
        ]
        if inc.platform_name:
            details_left.insert(1, ("Specific Platform", inc.platform_name))
        if inc.actor_description:
            actor_desc = (
                redact_identity(inc.actor_description, inc)
                if conceal else inc.actor_description
            )
            details_left.append(("Actor Description", actor_desc))
        if inc.user:
            details_right.append((
                "Reporter",
                REDACTED_MARKER if conceal else inc.user.email,
            ))

        detail_rows = []
        max_len = max(len(details_left), len(details_right))
        for i in range(max_len):
            left_cell = ""
            if i < len(details_left):
                lbl, val = details_left[i]
                left_cell = Paragraph(
                    f'<font color="#4A4A4A" size="9"><b>{lbl}</b></font><br/>'
                    f'<font color="#2D2D2D" size="10">{val}</font>',
                    ParagraphStyle("Cell", parent=value_style, spaceAfter=8, leading=14),
                )
            right_cell = ""
            if i < len(details_right):
                lbl, val = details_right[i]
                right_cell = Paragraph(
                    f'<font color="#4A4A4A" size="9"><b>{lbl}</b></font><br/>'
                    f'<font color="#2D2D2D" size="10">{val}</font>',
                    ParagraphStyle("Cell", parent=value_style, spaceAfter=8, leading=14),
                )
            detail_rows.append([left_cell, right_cell])

        if detail_rows:
            detail_table = Table(detail_rows, colWidths=[230, 230])
            detail_table.setStyle(TableStyle([
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ]))
            elements.append(detail_table)

        elements.append(Spacer(1, 3 * mm))
        elements.append(HRFlowable(width="100%", color=MID_GREY, thickness=0.5))

        # Narrative
        elements.append(Spacer(1, 2 * mm))
        elements.append(Paragraph("Incident Description", section_style))
        narrative = redact_identity(inc.narrative, inc) if conceal else inc.narrative
        elements.append(Paragraph(narrative, narrative_style))

        if conceal:
            elements.append(Paragraph(
                f'<font color="#C75B39">&#128274; Identity concealment enabled '
                f'&mdash; reporter details have been redacted for this report.</font>',
                small_style,
            ))

        # Harms
        harms = inc.harms.all()
        if harms:
            elements.append(Spacer(1, 2 * mm))
            elements.append(Paragraph(
                f"Harm Classification  ({harms.count()} harm{'s' if harms.count() != 1 else ''})",
                section_style,
            ))

            harm_data = [[
                Paragraph("<b>Harm Category</b>", ParagraphStyle("TH", parent=label_style, textColor=white, fontSize=9)),
                Paragraph("<b>Severity</b>", ParagraphStyle("TH", parent=label_style, textColor=white, fontSize=9)),
                Paragraph("<b>Duration</b>", ParagraphStyle("TH", parent=label_style, textColor=white, fontSize=9)),
            ]]
            for h in harms:
                harm_data.append([
                    Paragraph(h.get_harm_category_display(), ParagraphStyle("HC", parent=value_style, fontSize=9, spaceAfter=0)),
                    Paragraph(h.get_severity_score_display(), ParagraphStyle("HS", parent=value_style, fontSize=9, spaceAfter=0)),
                    Paragraph(h.get_duration_display(), ParagraphStyle("HD", parent=value_style, fontSize=9, spaceAfter=0)),
                ])
                if h.elaboration:
                    elaboration = (
                        redact_identity(h.elaboration, inc)
                        if conceal else h.elaboration
                    )
                    harm_data.append([
                        Paragraph(
                            f'<i><font color="#4A4A4A">"{elaboration}"</font></i>',
                            ParagraphStyle("HE", parent=small_style, fontSize=8, spaceAfter=0, leading=12),
                        ),
                        "", "",
                    ])

            if len(harm_data) > 1:
                harm_table = Table(harm_data, colWidths=[200, 120, 140])
                harm_table.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), TERRACOTTA),
                    ("TEXTCOLOR", (0, 0), (-1, 0), white),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("GRID", (0, 0), (-1, -1), 0.5, MID_GREY),
                    ("TOPPADDING", (0, 0), (-1, -1), 5),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                    ("LEFTPADDING", (0, 0), (-1, -1), 8),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, LIGHT_GREY]),
                ]))
                elements.append(harm_table)

        # Evidence
        if inc.evidence_file:
            elements.append(Spacer(1, 3 * mm))
            elements.append(Paragraph("Evidence", section_style))
            if conceal:
                evidence_ref = REDACTED_MARKER
            else:
                evidence_ref = inc.evidence_url or f"{inc.evidence_file.name}"
            elements.append(Paragraph(
                f"Evidence file attached: {evidence_ref}",
                value_style,
            ))

        # Bottom marker for each incident page
        elements.append(Spacer(1, 6 * mm))
        elements.append(HRFlowable(width="100%", color=MID_GREY, thickness=0.5))
        elements.append(Spacer(1, 2 * mm))
        elements.append(Paragraph(
            f"End of Report {idx}  |  {inc.reference_code}",
            ParagraphStyle("EndMarker", parent=footer_style, fontSize=7, textColor=HexColor("#CCCCCC")),
        ))

    doc.build(elements)
    buffer.seek(0)
    return buffer


def generate_text_summary(incident, conceal=None):
    """Generates plain text summary as fallback when PDF generation fails."""
    if conceal is None:
        conceal = should_conceal(incident)
    lines = []
    lines.append("=" * 50)
    lines.append("PRIVACY INCIDENT REPORT")
    lines.append(f"Reference: {incident.reference_code}")
    lines.append("=" * 50)
    lines.append("")
    if conceal:
        lines.append("IDENTITY CONCEALMENT ENABLED - REPORTER DETAILS REDACTED")
        lines.append("")
    lines.append("INCIDENT DETAILS")
    lines.append(f"  Platform: {incident.get_platform_category_display()}")
    lines.append(f"  Date: {incident.date_of_occurrence}")
    lines.append(f"  Type: {incident.get_incident_classification_display()}")
    lines.append(f"  Actor: {incident.get_actor_involvement_display()}")
    lines.append(f"  Severity: {incident.get_severity_rating_display()}")
    if incident.actor_description:
        actor_desc = (
            redact_identity(incident.actor_description, incident)
            if conceal else incident.actor_description
        )
        lines.append(f"  Actor Details: {actor_desc}")
    lines.append("")
    lines.append("DESCRIPTION")
    narrative = redact_identity(incident.narrative, incident) if conceal else incident.narrative
    lines.append(f"  {narrative}")
    lines.append("")
    lines.append("HARMS")
    for harm in incident.harms.all():
        lines.append(f"  - {harm.get_harm_category_display()} (Severity: {harm.get_severity_score_display()})")
        if harm.elaboration:
            elaboration = (
                redact_identity(harm.elaboration, incident)
                if conceal else harm.elaboration
            )
            lines.append(f"    {elaboration}")
    lines.append("")
    lines.append("=" * 50)
    return "\n".join(lines)
