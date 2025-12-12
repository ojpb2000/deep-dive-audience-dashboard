# Hilton Deep Divers Analytics Dashboard - Project Summary

## 🎯 Project Overview

An interactive, comprehensive analytics dashboard for analyzing the **Hilton Deep Divers** audience segment - high-income, luxury-oriented consumers (ages 35-44, income 200%+ above national median) compared to nationally representative data.

## 📊 Key Features

### Interactive Visualizations
- **Comparison Charts**: Side-by-side bars showing Target vs Control percentages
- **Index Analysis**: Color-coded horizontal bars showing relative affinity
- **Scatter Plots**: Multi-dimensional analysis with Target vs Control and Index visualization
- **Data Tables**: Sortable, filterable tables with CSV export

### Advanced Filtering
- Category-based navigation (Travel, Lifestyle, Sports, Brands)
- Section-specific analysis
- Metric sorting (Index, Target %, Difference)
- Top N items display
- Index threshold filtering

### Automated Insights
- Highest Index identification
- Strong over-indexing detection (Index ≥150)
- Largest gap analysis
- Overall affinity assessment

## 📁 Project Structure

```
.
├── app.py              # Main Streamlit dashboard application
├── data_parser.py      # CSV parsing and data processing engine
├── requirements.txt    # Python dependencies
├── .replit             # Replit deployment configuration
├── .streamlit/         # Streamlit configuration
│   └── config.toml
├── Various_HIlton - Deep DiversvsNationally representative.csv  # Source data
├── README.md           # Project documentation
├── DEPLOYMENT_GUIDE.md # Deployment instructions
├── test_parser.py      # Parser testing utility
└── PROJECT_SUMMARY.md  # This file
```

## 🔑 Key Metrics Explained

### Target Percent
- Percentage representation of the Hilton Deep Divers segment
- Shows absolute penetration within the target audience

### Control Percent
- National average for comparison
- Baseline for understanding relative performance

### Index
- **100 = National Average**: Equal likelihood
- **≥120 = Good Affinity**: 20%+ more likely than average
- **100-120 = Moderate Affinity**: Somewhat more likely
- **<100 = Under-indexing**: Less likely than average

## 📈 Data Categories

1. **Travel & Hospitality** (10 sections)
   - Hotels, destinations, travel activities, leisure preferences

2. **Lifestyle & Interests** (8 sections)
   - Hobbies, consumer personalities, seasonal activities

3. **Sports & Entertainment** (13 sections)
   - Sports events, music festivals, entertainment preferences

4. **Brands & Products** (7 sections)
   - Skincare, online brands, technology, clothing, household products

## 🚀 Deployment

### Replit (Recommended)
1. Import project to Replit
2. Ensure CSV file is in root directory
3. Click "Run" - dashboard starts automatically
4. Access via Replit webview

### Local Development
```bash
pip install -r requirements.txt
streamlit run app.py
```

## 💡 Usage Tips

1. **Start with Categories**: Use sidebar to navigate by category
2. **Filter by Index**: Set minimum Index to focus on high-affinity items
3. **Compare Metrics**: Switch between Index, Target %, and Difference views
4. **Export Data**: Download filtered results as CSV from Data Table tab
5. **Review Insights**: Check automated insights for each section

## 🎨 Dashboard Sections

### Header
- Title and audience description
- Data source information

### Sidebar
- Category filter
- Section selector
- Metric sorting options
- Top N slider
- Index threshold filter

### Main Content
- Key metrics cards
- Automated insights
- Interactive chart tabs
- Data table with export

## 📊 Chart Types

1. **Comparison Chart** (Tab 1)
   - Grouped bar chart
   - Target vs Control percentages
   - Top N items by selected metric

2. **Index Analysis** (Tab 2)
   - Horizontal bar chart
   - Color-coded by Index value
   - Baseline reference line at 100

3. **Scatter Plot** (Tab 3)
   - Target % vs Control %
   - Index as size and color
   - Parity line reference

4. **Data Table** (Tab 4)
   - Full dataset view
   - Sortable columns
   - CSV export functionality

## 🔍 Insights Generation

The dashboard automatically generates insights for each section:
- Identifies highest Index items
- Counts good affinity attributes (Index ≥120)
- Highlights largest gaps between segments
- Assesses overall category affinity

## 📝 Data Source

- **Platform**: YouGov Profiles+ USA
- **Date**: 2025-12-07
- **Target Group**: Hilton Deep Divers (n=93)
- **Control Group**: Nationally representative (n=411,511)
- **Total Rows**: 1,285 data points
- **Sections**: 38+ question sets

## 🛠️ Technical Stack

- **Framework**: Streamlit
- **Visualization**: Plotly
- **Data Processing**: Pandas
- **Language**: Python 3.8+

## ✨ Key Differentiators

1. **Comprehensive Parsing**: Handles complex YouGov CSV structure
2. **Category Organization**: Logical grouping of 38+ sections
3. **Interactive Filtering**: Multiple filter options for deep analysis
4. **Automated Insights**: AI-generated insights for each section
5. **Export Capabilities**: CSV download for further analysis
6. **Replit Ready**: Pre-configured for easy deployment

## 📋 Next Steps

1. Deploy to Replit following DEPLOYMENT_GUIDE.md
2. Test parser with test_parser.py if needed
3. Explore different categories and sections
4. Export insights for reporting
5. Customize filters based on analysis needs

## 🎯 Target Audience Profile

- **Age**: 35-44 years
- **Income**: 200%+ above national median
- **Lifestyle**: Luxury-oriented, premium product preference
- **Values**: Quality over price, willing to pay more for luxury
- **Identity**: Identifies with luxurious lifestyle

---

**Built with ❤️ for Hilton Analytics**

