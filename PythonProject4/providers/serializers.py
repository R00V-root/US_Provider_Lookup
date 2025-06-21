from rest_framework import serializers
from .models import Provider, Taxonomy

class TaxonomySerializer(serializers.ModelSerializer):
    class Meta:
        model = Taxonomy
        fields = ['code', 'classification', 'specialization']

class ProviderSerializer(serializers.ModelSerializer):
    taxonomy = TaxonomySerializer()
    class Meta:
        model = Provider
        fields = [
            'npi', 'first_name', 'middle_name', 'last_name', 'gender', 'credential',
            'address_line1', 'address_line2', 'city', 'state', 'postal_code',
            'phone', 'fax', 'taxonomy'
        ]
