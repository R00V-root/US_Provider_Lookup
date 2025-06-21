from django.contrib import admin
from .models import Provider, Taxonomy

@admin.register(Taxonomy)
class TaxonomyAdmin(admin.ModelAdmin):
    list_display = ('code', 'classification', 'specialization')
    search_fields = ('code', 'classification', 'specialization')

@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ('npi', 'first_name', 'last_name', 'city', 'state', 'taxonomy')
    search_fields = ('npi', 'first_name', 'last_name', 'city', 'state', 'taxonomy__classification')
    list_filter = ('state', 'taxonomy__classification', 'gender')
