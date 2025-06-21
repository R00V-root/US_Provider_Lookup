import csv, io, os, sys
from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from providers.models import Taxonomy

TAXONOMY_FIELDS = ['Code', 'Classification', 'Specialization']

PROVIDER_FIELD_MAP = {
    'NPI': 'npi',
    'Provider First Name': 'first_name',
    'Provider Middle Name': 'middle_name',
    'Provider Last Name (Legal Name)': 'last_name',
    'Provider Sex Code': 'gender',
    'Provider Credential Text': 'credential',
    'Provider First Line Business Practice Location Address': 'address_line1',
    'Provider Second Line Business Practice Location Address': 'address_line2',
    'Provider Business Practice Location Address City Name': 'city',
    'Provider Business Practice Location Address State Name': 'state',
    'Provider Business Practice Location Address Postal Code': 'postal_code',
    'Provider Business Practice Location Address Telephone Number': 'phone',
    'Provider Business Practice Location Address Fax Number': 'fax',
    'Healthcare Provider Taxonomy Code_1': 'taxonomy_code',
}

class Command(BaseCommand):
    help = 'Import NPPES provider and taxonomy data'

    def add_arguments(self, parser):
        parser.add_argument('taxonomy_csv', type=str, help='Path to nucc_taxonomy_250.csv')
        parser.add_argument('provider_csv', type=str, help='Path to npidata_cleaned.csv')

    def handle(self, *args, **options):
        taxonomy_csv_path = options['taxonomy_csv']
        provider_csv_path = options['provider_csv']

        if not os.path.exists(taxonomy_csv_path):
            raise CommandError(f'{taxonomy_csv_path} does not exist')
        if not os.path.exists(provider_csv_path):
            raise CommandError(f'{provider_csv_path} does not exist')

        self.stdout.write(self.style.NOTICE('Importing taxonomy data...'))
        self.import_taxonomy(taxonomy_csv_path)

        self.stdout.write(self.style.NOTICE('Importing provider data...'))
        self.import_providers(provider_csv_path)

        self.stdout.write(self.style.SUCCESS('Import completed.'))

    def import_taxonomy(self, csv_path):
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=TAXONOMY_FIELDS)
            next(reader, None)  # skip header
            objs = []
            for row in reader:
                objs.append(
                    Taxonomy(
                        code=row['Code'].strip(),
                        classification=row['Classification'].strip(),
                        specialization=row['Specialization'].strip(),
                    )
                )
            Taxonomy.objects.bulk_create(objs, ignore_conflicts=True)

    def import_providers(self, csv_path):
        staging_sql = '''
        DROP TABLE IF EXISTS providers_provider_staging;
        CREATE UNLOGGED TABLE providers_provider_staging
        (
            npi BIGINT PRIMARY KEY,
            first_name VARCHAR(70),
            middle_name VARCHAR(70),
            last_name VARCHAR(70),
            gender CHAR(1),
            credential VARCHAR(50),
            address_line1 VARCHAR(100),
            address_line2 VARCHAR(100),
            city VARCHAR(70),
            state CHAR(2),
            postal_code VARCHAR(20),
            phone VARCHAR(20),
            fax VARCHAR(20),
            taxonomy_code VARCHAR(10)
        );
        '''
        with connection.cursor() as cursor:
            cursor.execute(staging_sql)

        # stream CSV and copy into staging
        buffer = io.StringIO()
        writer = csv.writer(buffer)
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                raw_gender = row['Provider Sex Code'].strip().upper()
                gender = raw_gender if raw_gender in ('M', 'F') else ''  # blank for unknown
                raw_state = row['Provider Business Practice Location Address State Name'].strip().upper()
                state = raw_state if len(raw_state) == 2 and raw_state.isalpha() else ''
                writer.writerow([
                    row['NPI'],
                    row['Provider First Name'],
                    row['Provider Middle Name'],
                    row['Provider Last Name (Legal Name)'],
                    gender,
                    row['Provider Credential Text'],
                    row['Provider First Line Business Practice Location Address'],
                    row['Provider Second Line Business Practice Location Address'],
                    row['Provider Business Practice Location Address City Name'],
                    state,
                    row['Provider Business Practice Location Address Postal Code'],
                    row['Provider Business Practice Location Address Telephone Number'],
                    row['Provider Business Practice Location Address Fax Number'],
                    row['Healthcare Provider Taxonomy Code_1'],
                ])
                if buffer.tell() > 10_000_000:  # flush every ~10MB
                    buffer.seek(0)
                    with connection.cursor() as cursor:
                        cursor.copy_expert(
                            '''
                            COPY providers_provider_staging FROM STDIN WITH CSV
                            ''',
                            buffer
                        )
                    buffer.close()
                    buffer = io.StringIO()
                    writer = csv.writer(buffer)
            # flush remainder
            buffer.seek(0)
            with connection.cursor() as cursor:
                cursor.copy_expert(
                    '''
                    COPY providers_provider_staging FROM STDIN WITH CSV
                    ''',
                    buffer
                )
        buffer.close()

        merge_sql = '''
        INSERT INTO providers_provider (npi, first_name, middle_name, last_name, gender, credential,
                                        address_line1, address_line2, city, state, postal_code,
                                        phone, fax, taxonomy_id)
        SELECT s.npi, s.first_name, s.middle_name, s.last_name, s.gender, s.credential,
               s.address_line1, s.address_line2, s.city, s.state, s.postal_code,
               s.phone, s.fax, t.id
        FROM providers_provider_staging s
        JOIN providers_taxonomy t ON t.code = s.taxonomy_code
        ON CONFLICT (npi) DO NOTHING;
        DROP TABLE providers_provider_staging;
        '''
        with connection.cursor() as cursor:
            cursor.execute(merge_sql)
