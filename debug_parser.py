"""Debug parser to see what's happening"""
import csv
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

file_path = "Various_HIlton - Deep DiversvsNationally representative.csv"

print("Reading CSV file...")
with open(file_path, 'r', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    rows = list(reader)

print(f"Total rows: {len(rows)}")
print("\nChecking rows 8-15 (where sections should start):")
for i in range(8, min(15, len(rows))):
    row = rows[i]
    row_str = ','.join(row).strip()
    
    # Check conditions
    starts_with_quote = row_str.startswith('"')
    has_target = 'Target:' in row_str
    has_control = 'Control:' in row_str
    
    print(f"\nRow {i}:")
    print(f"  First cell: {repr(row[0]) if row else 'EMPTY'}")
    print(f"  Starts with quote: {starts_with_quote}")
    print(f"  Has 'Target:': {has_target}")
    print(f"  Has 'Control:': {has_control}")
    print(f"  Full row (first 150 chars): {row_str[:150]}")
    
    if starts_with_quote and has_target and has_control:
        print(f"  -> *** THIS IS A SECTION HEADER ***")
        # Try to extract section name
        section_name = row[0].strip('"').strip()
        if ',' in section_name:
            section_name = section_name.split(',')[0].strip()
        print(f"  Extracted section name: {repr(section_name)}")

