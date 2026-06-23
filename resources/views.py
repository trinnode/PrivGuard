from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from resources.models import Resource


@login_required
def resource_list(request):
    """Lists all visible resources with optional category filtering."""
    category = request.GET.get("category", "")
    search = request.GET.get("q", "").strip()
    resources = Resource.objects.filter(is_visible=True)

    if category:
        resources = resources.filter(category=category)

    if search:
        from django.db.models import Q
        resources = resources.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search) |
            Q(relevance_tags__icontains=search)
        )

    paginator = Paginator(resources, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    categories = Resource.CATEGORY_CHOICES

    return render(request, "resources/list.html", {
        "page_obj": page_obj,
        "resources": page_obj,
        "categories": categories,
        "active_category": category,
        "search_query": search,
    })


@login_required
def resource_detail(request, pk):
    """Shows a single resource."""
    resource = get_object_or_404(Resource, pk=pk, is_visible=True)
    return render(request, "resources/detail.html", {"resource": resource})
