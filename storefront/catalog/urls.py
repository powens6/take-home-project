from django.urls import path

from . import views

#URL patterns for the app. These are added to the storefront URLs.
urlpatterns = [
    path("", views.index, name="index"),
    path("products/", views.product_list, name="product_list"),
]