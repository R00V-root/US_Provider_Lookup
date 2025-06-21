from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Taxonomy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, unique=True)),
                ('classification', models.CharField(blank=True, max_length=120)),
                ('specialization', models.CharField(blank=True, max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('npi', models.BigIntegerField(unique=True)),
                ('first_name', models.CharField(db_index=True, max_length=70)),
                ('middle_name', models.CharField(blank=True, max_length=70, null=True)),
                ('last_name', models.CharField(db_index=True, max_length=70)),
                ('gender', models.CharField(blank=True, max_length=1, null=True)),
                ('credential', models.CharField(blank=True, max_length=50, null=True)),
                ('address_line1', models.CharField(blank=True, max_length=100, null=True)),
                ('address_line2', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(db_index=True, max_length=70)),
                ('state', models.CharField(db_index=True, max_length=2)),
                ('postal_code', models.CharField(blank=True, max_length=20, null=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('fax', models.CharField(blank=True, max_length=20, null=True)),
                ('taxonomy', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='providers', to='providers.taxonomy')),
            ],
        ),
    ]
