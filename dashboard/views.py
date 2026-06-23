from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
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

    severity_distribution = list(
        user_incidents
        .values("severity_rating")
        .annotate(count=Count("severity_rating"))
        .order_by("severity_rating")
    )

    platform_distribution = list(
        user_incidents
        .values("platform_category")
        .annotate(count=Count("platform_category"))
        .order_by("-count")[:5]
    )

    status_distribution = list(
        user_incidents
        .values("status")
        .annotate(count=Count("status"))
        .order_by("-count")
    )

    context = {
        "total_incidents": total_incidents,
        "recent_incidents": recent_incidents,
        "harm_counts": harm_counts_dict,
        "psychological_count": psychological_count,
        "tangible_count": tangible_count,
        "severity_distribution": severity_distribution,
        "platform_distribution": platform_distribution,
        "status_distribution": status_distribution,
    }
    return render(request, "dashboard/home.html", context)
