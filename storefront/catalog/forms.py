from django import forms

from django import forms
from .models import Category, Tag

#Class for the search form in the index.html file. The form helps with the Search and Filtering Functionality.
class ProductFilterForm(forms.Form):

    #search
    q = forms.CharField(
        label="Search products",
        required=False,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search products…",
                "aria-label": "Search products",
            }
        ),
    )

    # Category
    category = forms.ModelChoiceField(
        label="Category",
        queryset=Category.objects.all().order_by("name"),
        required=False,
        empty_label="All categories",
    )

    # Tag
    tag = forms.ModelChoiceField(
        label="Tag",
        queryset=Tag.objects.all().order_by("name"),
        required=False,
        empty_label="All tags",
    )
