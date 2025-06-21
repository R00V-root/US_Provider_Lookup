import django_filters as filters
from .models import Provider

class ProviderFilter(filters.FilterSet):
    first_name = filters.CharFilter(field_name='first_name', lookup_expr='icontains')
    last_name = filters.CharFilter(field_name='last_name', lookup_expr='icontains')
    npi = filters.NumberFilter(field_name='npi', lookup_expr='exact')
    city = filters.CharFilter(field_name='city', lookup_expr='icontains')
    state = filters.CharFilter(field_name='state', lookup_expr='iexact')
    profession = filters.CharFilter(method='filter_profession')

    class Meta:
        model = Provider
        fields = ['first_name', 'last_name', 'npi', 'city', 'state', 'profession']

    def filter_profession(self, queryset, name, value):
        return queryset.filter(taxonomy__classification__icontains=value)
