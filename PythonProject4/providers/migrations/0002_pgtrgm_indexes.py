from django.db import migrations
from django.contrib.postgres.operations import TrigramExtension
from django.contrib.postgres.indexes import GinIndex

class Migration(migrations.Migration):

    dependencies = [
        ('providers', '0001_initial'),
    ]

    operations = [
        TrigramExtension(),
        migrations.AddIndex(
            model_name='provider',
            index=GinIndex(
                name='provider_first_name_trgm',
                fields=['first_name'],
                opclasses=['gin_trgm_ops'],
            ),
        ),
        migrations.AddIndex(
            model_name='provider',
            index=GinIndex(
                name='provider_last_name_trgm',
                fields=['last_name'],
                opclasses=['gin_trgm_ops'],
            ),
        ),
        migrations.AddIndex(
            model_name='provider',
            index=GinIndex(
                name='provider_city_trgm',
                fields=['city'],
                opclasses=['gin_trgm_ops'],
            ),
        ),
    ]
