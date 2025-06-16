from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import *
from django.db.models import Q
from .forms import ProductFilterForm

#This was the initial logic I wrote, specifically to minimize SQL Calls to the database. 
# It is left here on purpose despite not being used for debuging and visibility.
#This helped negate the N+1 problem common in queries
def index(request):
    latest_products = (
        Product.objects
               .prefetch_related("tags")      # one query for tags
               .select_related("category")    # one query for category
               .order_by("-created_at")[:20]
    )
    return render(request, "catalog/index.html", {"latest_products": latest_products})

#This is the main filtering and product view
def product_list(request):
    
    form = ProductFilterForm(request.GET or None)

    #Initial Queryset
    qs = (
        Product.objects
        .select_related("category")
        .prefetch_related("tags")
        .order_by("-created_at")
    )

    #Blank Q to begin combining filters
    query = Q()

  #Form check
    if form.is_valid():
        data = form.cleaned_data
        category_id = data.get("category")
        tag = data.get("tag")
        search_term = data.get("q")

        #If statements allow for combinations of queries and search
        if category_id:
            query &= Q(category_id=category_id)

        if tag:
            query &= Q(tags=tag)

        #Basic search - future work for full text search implementation
        if search_term:
            query &= (
                Q(name__icontains=search_term)
                | Q(description__icontains=search_term)
            )

    #combine queries and filter queryset
    products = qs.filter(query).distinct()

    #add context for template
    context = {
        "latest_products": products,
        "form": form,
        "categories": Category.objects.all(),
        "tags": Tag.objects.all(),
    }
    return render(request, "catalog/index.html", context)

    

