from django import forms

from django import forms
from .models import Category, Tag


class ProductFilterForm(forms.Form):

    # Free-text search
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

    # Category dropdown
    category = forms.ModelChoiceField(
        label="Category",
        queryset=Category.objects.all().order_by("name"),
        required=False,
        empty_label="All categories",
    )

    # Tag dropdown
    tag = forms.ModelChoiceField(
        label="Tag",
        queryset=Tag.objects.all().order_by("name"),
        required=False,
        empty_label="All tags",
    )

    def __init__(self, *args, **kwargs):
        """
        AI helped me do this to do the following:
        If you ever want to pass in pre-filtered querysets for
        Category or Tag (e.g. only active ones), you can do it
        here by popping extra kwargs before super().__init__().
        """
        super().__init__(*args, **kwargs)
