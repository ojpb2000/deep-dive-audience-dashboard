# 🏨 Hilton Deep Divers Analytics Dashboard

Interactive dashboard for analyzing the "Hilton Deep Divers" audience compared to a nationally representative control group.

## 📊 Features

- **Interactive Visualizations**: Multiple chart types (bar charts, scatter plots, heatmaps, data tables)
- **AI Strategic Analysis**: 10 strategic insights for Q2 communication planning
- **Deep Cultural Insights**: In-depth cultural analysis with varied visualizations
- **Dynamic Filtering**: Filter by category, section, index threshold, and more
- **Real-time Insights**: Automatic insights generation for each chart

## 🚀 Deployment

This dashboard is deployed as a static HTML file on **GitHub Pages**.

### Access the Dashboard

Visit: `https://ojpb2000.github.io/deep-dive-audience-dashboard/`

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/ojpb2000/deep-dive-audience-dashboard.git
```

2. Open `index.html` in your browser

## 📁 Project Structure

- `index.html` - Static HTML dashboard (ready for GitHub Pages)
- `generate_static_dashboard.py` - Script to regenerate the dashboard from CSV data
- `data_parser.py` - CSV parsing and data processing utilities
- `Various_HIlton - Deep DiversvsNationally representative.csv` - Source data file

## 📈 Data Source

- **Source**: YouGov Profiles+ USA 2025-12-07
- **Target Group**: 93 respondents (Hilton Deep Divers)
- **Control Group**: 411,511 nationally representative respondents

## 🎯 Audience Profile

The Hilton Deep Divers audience consists of:
- **Demographics**: 35-44 years old
- **Income**: 200%+ of national median
- **Characteristics**: High-income, luxury-oriented consumers who value quality and premium experiences

## 🔧 Key Metrics

- **Target Percent**: Representativeness of the core segment (Hilton Deep Divers)
- **Control Percent**: National representativeness
- **Index**: Affinity indicator (Index ≥120 indicates good affinity)

## 📝 Notes

- All texts and labels are in English
- Dashboard starts filtered on "Travel & Hospitality" category and "Leisure trips - most preferred" section
- Minimum Index filter defaults to 120
