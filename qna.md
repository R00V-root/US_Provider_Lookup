** This project currently assumes each provider has only 1 taxonomy code
changes needed: - update clean_npi.py to include 14 other taxonomy code columns 
                 - update tables accordingly**

process:

the data flow goes: CSV files on disk → PostgreSQL staging table (via COPY command) → Real PostgreSQL tables (via INSERT with data cleaning) → Django queries this data → Converts to JSON or HTML depending on what's requested.
