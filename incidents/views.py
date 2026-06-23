import hashlib
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.db.models import Q, Count
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from incidents.models import Incident, Harm, AuditLog
from incidents.forms import IncidentForm
from incidents.taxonomy import HARM_CATEGORIES


def get_client_ip_hash(request):
    ip = request.META.get("REMOTE_ADDR", "unknown")
    return hashlib.sha256(ip.encode()).hexdigest()


def log_audit(request, event_type, summary=""):
    AuditLog.objects.create(
        event_type=event_type,
        user=request.user if request.user.is_authenticated else None,
        action_summary=summary,
        ip_hash=get_client_ip_hash(request),
    )


@login_required
def incident_list(request):
    incidents = Incident.objects.filter(user=request.user).prefetch_related("harms")

    search = request.GET.get("q", "").strip()
    if search:
        incidents = incidents.filter(
            Q(reference_code__icontains=search) |
            Q(narrative__icontains=search) |
            Q(incident_classification__icontains=search) |
            Q(platform_category__icontains=search)
        )

    status_filter = request.GET.get("status", "")
    if status_filter:
        incidents = incidents.filter(status=status_filter)

    paginator = Paginator(incidents, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "incidents/list.html", {
        "page_obj": page_obj,
        "incidents": page_obj,
        "search_query": search,
        "status_filter": status_filter,
    })


@login_required
def incident_detail(request, reference_code):
    incident = get_object_or_404(
        Incident.objects.prefetch_related("harms"),
        reference_code=reference_code,
        user=request.user,
    )
    log_audit(request, "incident_view", f"Viewed incident {reference_code}")
    return render(request, "incidents/detail.html", {"incident": incident})


@login_required
@transaction.atomic
def incident_edit(request, reference_code):
    incident = get_object_or_404(
        Incident.objects.prefetch_related("harms"),
        reference_code=reference_code,
        user=request.user,
    )
    if request.method == "POST":
        form = IncidentForm(request.POST, request.FILES, instance=incident)
        if form.is_valid():
            form.save()
            log_audit(request, "incident_create", f"Updated incident {reference_code}")
            messages.success(request, "Incident updated successfully.")
            return redirect("incidents:detail", reference_code=reference_code)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = IncidentForm(instance=incident)

    psyc_harm_categories = [h for h in HARM_CATEGORIES if h[2] == "psychological"]
    tangible_harm_categories = [h for h in HARM_CATEGORIES if h[2] == "tangible"]
    existing_harms = {h.harm_category: h for h in incident.harms.all()}

    return render(request, "incidents/edit.html", {
        "form": form,
        "incident": incident,
        "harm_categories": psyc_harm_categories,
        "tangible_categories": tangible_harm_categories,
        "existing_harms": existing_harms,
    })


@login_required
@require_POST
def incident_delete(request, reference_code):
    incident = get_object_or_404(
        Incident, reference_code=reference_code, user=request.user,
    )
    log_audit(request, "incident_create", f"Deleted incident {reference_code}")
    incident.delete()
    messages.success(request, f"Incident {reference_code} has been deleted.")
    return redirect("incidents:list")


@login_required
@require_POST
def incident_update_status(request, reference_code):
    incident = get_object_or_404(
        Incident, reference_code=reference_code, user=request.user,
    )
    new_status = request.POST.get("status", "")
    valid_statuses = [s[0] for s in Incident.STATUS_CHOICES]
    if new_status in valid_statuses:
        incident.status = new_status
        incident.save(update_fields=["status"])
        messages.success(request, f"Incident status updated to {incident.get_status_display()}.")
    else:
        messages.error(request, "Invalid status.")
    return redirect("incidents:detail", reference_code=reference_code)


@transaction.atomic
def incident_create(request):
    if request.method == "POST":
        form = IncidentForm(request.POST, request.FILES)

        if form.is_valid():
            incident = form.save(commit=False)
            incident.user = request.user if request.user.is_authenticated else None
            if not request.user.is_authenticated:
                incident.is_anonymous = True
            incident.save()

            selected_harms = request.POST.getlist("harm_sel")
            for harm_key in selected_harms:
                severity = request.POST.get(f"harm_severity_{harm_key}")
                duration = request.POST.get(f"harm_duration_{harm_key}")
                elaboration = request.POST.get(f"harm_elaboration_{harm_key}", "")

                if severity and duration:
                    Harm.objects.create(
                        incident=incident,
                        harm_category=harm_key,
                        severity_score=int(severity),
                        duration=duration,
                        elaboration=elaboration,
                    )

            log_audit(request, "incident_create", f"Created incident {incident.reference_code}")
            if request.user.is_authenticated:
                messages.success(
                    request,
                    "Your incident has been reported. A reference code has been generated for your records.",
                )
                return redirect("incidents:detail", reference_code=incident.reference_code)
            else:
                messages.success(
                    request,
                    "Your incident has been reported anonymously. Save your reference code: " + incident.reference_code,
                )
                return redirect("landing")
        else:
            messages.error(
                request,
                "There was a problem with your submission. Please check the highlighted fields.",
            )
    else:
        form = IncidentForm()

    psyc_harm_categories = [h for h in HARM_CATEGORIES if h[2] == "psychological"]
    tangible_harm_categories = [h for h in HARM_CATEGORIES if h[2] == "tangible"]

    return render(request, "incidents/create.html", {
        "form": form,
        "harm_categories": psyc_harm_categories,
        "tangible_categories": tangible_harm_categories,
    })


@login_required
def admin_list(request):
    if request.user.role != "admin":
        messages.error(request, "You do not have permission to access this page.")
        return redirect("dashboard:home")

    incidents = Incident.objects.select_related("user").prefetch_related("harms").all()

    search = request.GET.get("q", "").strip()
    if search:
        incidents = incidents.filter(
            Q(reference_code__icontains=search) |
            Q(user__email__icontains=search) |
            Q(narrative__icontains=search) |
            Q(incident_classification__icontains=search)
        )

    status_filter = request.GET.get("status", "")
    if status_filter:
        incidents = incidents.filter(status=status_filter)

    anonymized_count = Incident.objects.filter(anonymize_requested=True).count()

    paginator = Paginator(incidents, 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "incidents/admin_list.html", {
        "page_obj": page_obj,
        "incidents": page_obj,
        "anonymized_count": anonymized_count,
        "search_query": search,
        "status_filter": status_filter,
    })


@login_required
def admin_detail(request, reference_code):
    if request.user.role != "admin":
        messages.error(request, "You do not have permission to access this page.")
        return redirect("dashboard:home")
    incident = get_object_or_404(
        Incident.objects.select_related("user").prefetch_related("harms"),
        reference_code=reference_code,
    )
    log_audit(request, "admin_action", f"Admin viewed incident {reference_code}")
    return render(request, "incidents/admin_detail.html", {"incident": incident})


@login_required
@require_POST
def admin_delete(request, reference_code):
    if request.user.role != "admin":
        messages.error(request, "You do not have permission to access this page.")
        return redirect("dashboard:home")
    incident = get_object_or_404(Incident, reference_code=reference_code)
    log_audit(request, "admin_action", f"Admin deleted incident {reference_code}")
    incident.delete()
    messages.success(request, f"Incident {reference_code} has been deleted.")
    return redirect("incidents:admin_list")


@login_required
def admin_export(request, reference_code):
    if request.user.role != "admin":
        messages.error(request, "You do not have permission to access this page.")
        return redirect("dashboard:home")
    incident = get_object_or_404(
        Incident.objects.select_related("user").prefetch_related("harms"),
        reference_code=reference_code,
    )
    conceal = incident.anonymize_requested
    log_audit(request, "incident_export", f"Admin exported incident {reference_code} (conceal={conceal})")
    return render(request, "incidents/export.html", {
        "incident": incident,
        "conceal": conceal,
    })
