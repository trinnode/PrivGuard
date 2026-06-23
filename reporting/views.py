from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from incidents.models import Incident
from incidents.views import log_audit
from reporting.pdf_generator import generate_incident_report, generate_text_summary, generate_bulk_report


@login_required
def export_pdf(request, reference_code):
    """Exports a single incident report as a PDF file."""
    incident = get_object_or_404(
        Incident.objects.prefetch_related("harms"),
        reference_code=reference_code,
        user=request.user,
    )

    try:
        pdf_buffer = generate_incident_report(incident)
        log_audit(request, "incident_export", f"Exported PDF for incident {reference_code}")
        response = HttpResponse(pdf_buffer.read(), content_type="application/pdf")
        response["Content-Disposition"] = (
            f'attachment; filename="incident_{incident.reference_code}.pdf"'
        )
        return response
    except Exception:
        log_audit(request, "incident_export", f"PDF generation failed for {reference_code}, text fallback sent")
        text_content = generate_text_summary(incident)
        response = HttpResponse(text_content, content_type="text/plain; charset=utf-8")
        response["Content-Disposition"] = (
            f'attachment; filename="incident_{incident.reference_code}.txt"'
        )
        return response


@login_required
def admin_export_bulk(request):
    """Admin: exports all incidents as a single multi-page PDF."""
    if request.user.role != "admin":
        return HttpResponse("Forbidden", status=403)

    incidents = Incident.objects.select_related("user").prefetch_related("harms").all()

    search = request.GET.get("q", "").strip()
    status_filter = request.GET.get("status", "")
    if search:
        incidents = incidents.filter(
            Q(reference_code__icontains=search) |
            Q(user__email__icontains=search) |
            Q(narrative__icontains=search)
        )
    if status_filter:
        incidents = incidents.filter(status=status_filter)

    try:
        pdf_buffer = generate_bulk_report(incidents)
        count = incidents.count()
        log_audit(request, "incident_export", f"Bulk exported {count} incidents as PDF")
        response = HttpResponse(pdf_buffer.read(), content_type="application/pdf")
        response["Content-Disposition"] = (
            f'attachment; filename="mamoru_all_incidents_{count}_reports.pdf"'
        )
        return response
    except Exception:
        log_audit(request, "incident_export", "Bulk PDF generation failed")
        return HttpResponse("PDF generation failed. Please try again.", status=500)
