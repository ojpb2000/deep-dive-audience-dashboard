"""Quick test to verify dashboard can start"""
import sys
import subprocess
import os

print("Testing dashboard setup...")
print(f"Python version: {sys.version}")

# Check if all required modules can be imported
try:
    import streamlit
    print(f"[OK] Streamlit {streamlit.__version__}")
except ImportError as e:
    print(f"[ERROR] Streamlit not installed: {e}")
    sys.exit(1)

try:
    import pandas
    print(f"[OK] Pandas {pandas.__version__}")
except ImportError as e:
    print(f"[ERROR] Pandas not installed: {e}")
    sys.exit(1)

try:
    import plotly
    print(f"[OK] Plotly {plotly.__version__}")
except ImportError as e:
    print(f"[ERROR] Plotly not installed: {e}")
    sys.exit(1)

try:
    import numpy
    print(f"[OK] NumPy {numpy.__version__}")
except ImportError as e:
    print(f"[ERROR] NumPy not installed: {e}")
    sys.exit(1)

# Check if data parser works
try:
    from data_parser import parse_csv_file, process_datasets
    datasets = parse_csv_file("Various_HIlton - Deep DiversvsNationally representative.csv")
    print(f"[OK] Data parser works - found {len(datasets)} sections")
except Exception as e:
    print(f"[ERROR] Data parser failed: {e}")
    sys.exit(1)

# Check if CSV file exists
if os.path.exists("Various_HIlton - Deep DiversvsNationally representative.csv"):
    print("[OK] CSV file found")
else:
    print("[ERROR] CSV file not found!")
    sys.exit(1)

print("\n[OK] All checks passed! Dashboard should work.")
print("\nTo run the dashboard, execute:")
print("  streamlit run app.py")

