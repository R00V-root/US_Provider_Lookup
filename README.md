# US_Provider_Lookup

# Healthcare Provider Directory 

A production-ready **Django 5** web/API service that lets you fuzzy-search the entire **NPPES** practitioner registry (≈ 8 million records) by name, location or specialty, with PostgreSQL `pg_trgm` indexes delivering sub-second responses even on commodity hardware.

---

## 1  Architecture Overview 

* **Backend**: Django 5, Django REST Framework, `django-filter`, PostgreSQL 15+ with `pg_trgm`
* **Data**  
  * **Providers**: CMS NPPES public use file (cleaned to 14 key columns)  
  * **Taxonomy**: NUCC provider-taxonomy code set (3 columns)
* **Import pipeline**  
  1. Bulk-copy CSV into `providers_provider_staging` using PostgreSQL `COPY`  
  2. Foreign-key resolution to `providers_taxonomy`  
  3. Merge into the indexed `providers_provider` table
* **Search**: Unified `ProviderFilter` serves both HTML form and JSON endpoint

---

## 2  Prerequisites ⚙

* Python 3.10+ with `pip` inside a virtual environment
* PostgreSQL with a superuser able to create `pg_trgm` extension
* Build tooling (or just install the pre-built wheel) for **`psycopg2-binary 2.9.9`**  
  🐘 [psycopg2-binary](https://www.google.com/search?q=psycopg2-binary+PyPI)

---

## 3  Fetching the Raw Data 

Download the latest source files:

* **NPPES provider file** from CMS  
  🔗 [CMS download page](https://www.google.com/search?q=CMS+NPPES+download)
* **NUCC taxonomy CSV**  
  🔗 [NUCC code-set page](https://www.google.com/search?q=NUCC+taxonomy+code+set+CSV)

Place both raw CSV files in a local `data/` directory (or anywhere you like).

---

## 4  Cleaning the 8 GB NPPES Dump 

The repository ships with `clean_npi.py` (shown below).  
Edit the two path constants at the top so they match your filenames, then run:

```
bash
python3 clean_npi.py
#!/usr/bin/env python3
# (full script omitted here for brevity; see repository)

INPUT_CSV = Path("npidata_pfile_20050523-20250511.csv")  # change me
OUTPUT_CSV = Path("npidata_cleaned.csv")                 # change me
...
```

The script streams the 330-column, multi-GB file in 100 k-row chunks, retains only 14 searchable columns and writes npidata_cleaned.csv which is roughly 96 % smaller but contains every practitioner you need.


## Local Installation

# 1. Clone and enter the project
git clone https://github.com/R00V-root/US_Provider_Lookup.git
cd healthcare-provider-directory

# 2. Activate venv and install deps
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt      # Django 5, DRF, django-filter, psycopg2-binary

# 3. Create a fresh database
createdb -U postgres providers

# 4. Apply schema
python3 manage.py migrate


python3 manage.py import_nppes data/nucc_taxonomy_250.csv data/npidata_cleaned.csv

python3 manage.py runserver



