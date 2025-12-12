# Deployment Guide - Hilton Deep Divers Dashboard

## Quick Start on Replit

1. **Import Project to Replit**
   - Create a new Repl
   - Upload all project files OR use Git import
   - Ensure the CSV file is in the root directory

2. **File Structure Required**
   ```
   .
   ├── app.py              # Main dashboard application
   ├── data_parser.py      # CSV parser
   ├── requirements.txt    # Dependencies
   ├── .replit             # Replit config (auto-runs Streamlit)
   ├── .streamlit/         # Streamlit config
   │   └── config.toml
   ├── Various_HIlton - Deep DiversvsNationally representative.csv  # Data file
   └── README.md
   ```

3. **Automatic Setup**
   - Replit will automatically install dependencies from `requirements.txt`
   - The `.replit` file configures the run command
   - Click "Run" to start the dashboard

4. **Access Dashboard**
   - The dashboard will be available in the Replit webview
   - URL will be shown in the console (typically port 8080)

## Manual Setup (Local)

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Dashboard**
   ```bash
   streamlit run app.py
   ```

3. **Access**
   - Open browser to `http://localhost:8501`

## Troubleshooting

### CSV File Not Found
- Ensure the CSV file is named exactly: `Various_HIlton - Deep DiversvsNationally representative.csv`
- Check it's in the root directory

### Parser Errors
- Run `python test_parser.py` to test the parser
- Check CSV file encoding (should be UTF-8)

### Port Issues on Replit
- The `.replit` file configures port 8080
- If conflicts occur, modify `.replit` to use a different port

### Memory Issues
- The dataset is large (1285 rows)
- If memory issues occur, consider filtering data in the parser

## Features Overview

### Navigation
- **Sidebar Filters**: Category, Section, Metric, Top N items, Index threshold
- **Tabs**: Comparison Chart, Index Analysis, Scatter Plot, Data Table

### Key Metrics Displayed
- High Index Items (≥150)
- Average Index
- Highest Index
- Total Items

### Visualizations
1. **Comparison Chart**: Side-by-side bars showing Target vs Control percentages
2. **Index Analysis**: Horizontal bar chart with color coding by Index value
3. **Scatter Plot**: Target vs Control with Index as size/color
4. **Data Table**: Sortable, filterable table with export capability

### Insights
- Automated insights generated for each section
- Highlights highest Index, strong over-indexing, largest gaps, and overall affinity

## Data Categories

1. **Travel & Hospitality**: Hotels, destinations, travel activities
2. **Lifestyle & Interests**: Hobbies, consumer personalities, seasonal activities
3. **Sports & Entertainment**: Sports events, music festivals, entertainment
4. **Brands & Products**: Skincare, online brands, technology, clothing

## Understanding Index

- **Index = 100**: Equal to national average
- **Index ≥ 120**: Good affinity (20%+ more likely than average)
- **Index 100-120**: Moderate affinity
- **Index < 100**: Under-indexing (less likely than average)

## Support

For issues or questions, check:
1. CSV file format matches expected structure
2. All dependencies are installed
3. Python version is 3.8+

