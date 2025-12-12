"""
Simple test script to verify the CSV parser works correctly
"""
from data_parser import parse_csv_file, process_datasets

def test_parser():
    print("Testing CSV parser...")
    try:
        datasets = parse_csv_file("Various_HIlton - Deep DiversvsNationally representative.csv")
        print(f"✓ Successfully parsed {len(datasets)} sections")
        
        processed = process_datasets(datasets)
        print(f"✓ Successfully processed {len(processed)} sections")
        
        # Show first few sections
        print("\nFirst 5 sections found:")
        for i, (section_name, section_data) in enumerate(list(processed.items())[:5]):
            print(f"  {i+1}. {section_name}")
            print(f"     Question: {section_data['question'][:60]}...")
            print(f"     Rows: {len(section_data['data'])}")
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_parser()

