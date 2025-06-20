# !/usr/bin/env python3
"""
Clean the CMS NPPES file `npidata_pfile_20050523-20250511.csv`
and save a compact version called `npidata_cleaned.csv`.

Run:
    python clean_npi.py
"""

import pandas as pd
from pathlib import Path
import os
from tqdm import tqdm

# --------------------------------------------------------------------------- #
# 1.  SETTINGS—edit these two paths if your file lives elsewhere
# --------------------------------------------------------------------------- #
INPUT_CSV = Path("npidata_pfile_20050523-20250511.csv")  # raw 7-million-row file
OUTPUT_CSV = Path("npidata_cleaned.csv")  # will be ~-96 % smaller

# Keep only the columns that make searching useful.
COLUMNS_TO_KEEP = [
    "NPI",
    "Provider Last Name (Legal Name)",
    "Provider First Name",
    "Provider Middle Name",
    "Provider Sex Code",
    "Provider Credential Text",
    "Provider First Line Business Practice Location Address",
    "Provider Second Line Business Practice Location Address",
    "Provider Business Practice Location Address City Name",
    "Provider Business Practice Location Address State Name",
    "Provider Business Practice Location Address Postal Code",
    "Provider Business Practice Location Address Telephone Number",
    "Provider Business Practice Location Address Fax Number",
    "Healthcare Provider Taxonomy Code_1"
]

CHUNK_SIZE = 100_000  # read 100 k rows at a time so we never fill RAM


# --------------------------------------------------------------------------- #
# 2.  HELPER FUNCTIONS
# --------------------------------------------------------------------------- #
def get_total_rows(csv_path: Path) -> int:
    """Count total rows in CSV file for progress tracking."""
    print("📊 Counting total rows in file...")

    # Method 1: Try using wc -l on Unix systems (faster)
    if os.name != 'nt':  # not Windows
        try:
            import subprocess
            result = subprocess.run(['wc', '-l', str(csv_path)],
                                    capture_output=True, text=True)
            if result.returncode == 0:
                total_lines = int(result.stdout.split()[0])
                return total_lines - 1  # subtract header row
        except:
            pass

    # Method 2: Count manually (slower but works everywhere)
    with open(csv_path, 'r', encoding='utf-8') as f:
        total_rows = sum(1 for line in f) - 1  # subtract header

    return total_rows


def clean_chunk(chunk: pd.DataFrame) -> pd.DataFrame:
    """Trim to the columns we need and normalise missing values."""
    # Select columns, fill NAs, convert to string
    chunk = chunk[COLUMNS_TO_KEEP].fillna("no data").astype(str)

    # Strip whitespace from all string columns
    chunk = chunk.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

    return chunk


# --------------------------------------------------------------------------- #
# 3.  MAIN PIPELINE WITH PROGRESS
# --------------------------------------------------------------------------- #
def main() -> None:
    if not INPUT_CSV.exists():
        raise FileNotFoundError(f"Cannot find {INPUT_CSV!s}")

    # Get file size info
    file_size_mb = INPUT_CSV.stat().st_size / (1024 * 1024)
    print(f"📁 Input file: {INPUT_CSV.name}")
    print(f"📏 File size: {file_size_mb:.1f} MB")

    # Count total rows for progress bar
    total_rows = get_total_rows(INPUT_CSV)
    total_chunks = (total_rows + CHUNK_SIZE - 1) // CHUNK_SIZE

    print(f"📊 Total rows: {total_rows:,}")
    print(f"🔄 Processing in {total_chunks} chunks of {CHUNK_SIZE:,} rows each")
    print(f"💾 Keeping {len(COLUMNS_TO_KEEP)} out of 330 columns")
    print()

    # Process with progress bar
    first_write = True
    processed_rows = 0

    # Create progress bar
    with tqdm(total=total_rows, desc="Processing", unit="rows", unit_scale=True) as pbar:
        for chunk_num, chunk in enumerate(pd.read_csv(INPUT_CSV, chunksize=CHUNK_SIZE, dtype=str), 1):
            # Clean the chunk
            cleaned = clean_chunk(chunk)

            # Write to output
            cleaned.to_csv(
                OUTPUT_CSV,
                mode="w" if first_write else "a",
                header=first_write,
                index=False
            )
            first_write = False

            # Update counters and progress
            chunk_rows = len(chunk)
            processed_rows += chunk_rows
            pbar.update(chunk_rows)

            # Update description with current chunk info
            pbar.set_description(f"Chunk {chunk_num}/{total_chunks}")

    # Final summary
    output_size_mb = OUTPUT_CSV.stat().st_size / (1024 * 1024)
    reduction_pct = (1 - output_size_mb / file_size_mb) * 100

    print()
    print("🎉 COMPLETED!")
    print(f"✓ Processed: {processed_rows:,} rows")
    print(f"✓ Output file: {OUTPUT_CSV.resolve()}")
    print(f"✓ Output size: {output_size_mb:.1f} MB")
    print(f"✓ Size reduction: {reduction_pct:.1f}%")


if __name__ == "__main__":
    main()