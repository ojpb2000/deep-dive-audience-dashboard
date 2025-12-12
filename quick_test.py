"""Quick test script"""
import sys
import io

# Fix encoding for Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from data_parser import parse_csv_file, process_datasets

print("Testing parser...")
datasets = parse_csv_file("Various_HIlton - Deep DiversvsNationally representative.csv")
print(f"[OK] Found {len(datasets)} sections")

processed = process_datasets(datasets)
print(f"[OK] Processed {len(processed)} sections")

# Show sample
if processed:
    first_section = list(processed.items())[0]
    print(f"\nSample section: {first_section[0]}")
    print(f"  Rows: {len(first_section[1]['data'])}")
    print(f"  Columns: {list(first_section[1]['data'].columns)[:5]}...")
    
    # Show a few more sections
    print(f"\nFirst 5 sections:")
    for i, (name, data) in enumerate(list(processed.items())[:5]):
        row_count = len(data['data'])
        print(f"  {i+1}. {name[:60]}... ({row_count} rows)")

print("\n[OK] Parser test completed successfully!")

