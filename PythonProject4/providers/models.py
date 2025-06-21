from django.db import models
from django.contrib.postgres.indexes import GinIndex

class Taxonomy(models.Model):
    code = models.CharField(max_length=10, unique=True)
    classification = models.CharField(max_length=120, blank=True)
    specialization = models.CharField(max_length=120, blank=True)
    grouping = models.CharField(max_length=120, blank=True, null=True)

    def __str__(self):
        return f'{self.classification} ({self.code})'

class Provider(models.Model):
    npi = models.BigIntegerField(unique=True)
    first_name = models.CharField(max_length=70, db_index=True)
    middle_name = models.CharField(max_length=70, blank=True, null=True)
    last_name = models.CharField(max_length=70, db_index=True)
    gender = models.CharField(max_length=1, blank=True, null=True)
    credential = models.CharField(max_length=50, blank=True, null=True)

    address_line1 = models.CharField(max_length=100, blank=True, null=True)
    address_line2 = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=70, db_index=True)
    state = models.CharField(max_length=2, db_index=True, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    fax = models.CharField(max_length=20, blank=True, null=True)

    taxonomy = models.ForeignKey(Taxonomy, on_delete=models.PROTECT, related_name='providers')

    class Meta:
        indexes = [
            GinIndex(
                name='provider_first_name_trgm',
                fields=['first_name'],
                opclasses=['gin_trgm_ops']
            ),
            GinIndex(
                name='provider_last_name_trgm',
                fields=['last_name'],
                opclasses=['gin_trgm_ops']
            ),
            GinIndex(
                name='provider_city_trgm',
                fields=['city'],
                opclasses=['gin_trgm_ops']
            ),
        ]

    def __str__(self):
        return f'{self.last_name}, {self.first_name} ({self.npi})'
