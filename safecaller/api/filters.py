import django_filters
from .models import Contact


class ContactFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Contact
        fields = ['name']
