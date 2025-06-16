from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import *
from django.db.models import Q
from .forms import ProductFilterForm

def index(request):
    latest_products = (
        Product.objects
               .prefetch_related("tags")      # one query for tags
               .select_related("category")    # one query for category
               .order_by("-created_at")[:20]
    )
    return render(request, "catalog/index.html", {"latest_products": latest_products})


def product_list(request):
    
    form = ProductFilterForm(request.GET or None)

    qs = (
        Product.objects
        .select_related("category")
        .prefetch_related("tags")
        .order_by("-created_at")
    )

    query = Q()

    if form.is_valid():
        data = form.cleaned_data
        category_id = data.get("category")
        tag_id = data.get("tag")
        search_term = data.get("q")

        if category_id:
            query &= Q(category_id=category_id)

        if tag_id:
            query &= Q(tags__id=tag_id)

        if search_term:
            query &= (
                Q(name__icontains=search_term)
                | Q(description__icontains=search_term)
            )

    products = qs.filter(query).distinct()

    context = {
        "latest_products": products,
        "form": form,
        "categories": Category.objects.all(),
        "tags": Tag.objects.all(),
    }
    return render(request, "catalog/index.html", context)

    

