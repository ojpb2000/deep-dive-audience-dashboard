# Hilton Deep Divers Analytics Dashboard

An interactive analytics dashboard for analyzing the Hilton Deep Divers audience segment compared to nationally representative data.

## Overview

This dashboard provides comprehensive insights into the **Hilton Deep Divers** audience - high-income, luxury-oriented consumers (ages 35-44, with income 200%+ above the national median) who identify with a luxurious lifestyle and prefer premium products and experiences.

## Features

- **Interactive Visualizations**: Multiple chart types including comparison bars, index analysis, scatter plots, heatmaps, and more
- **Category Organization**: Data organized by Travel & Hospitality, Lifestyle & Interests, Sports & Entertainment, and Brands & Products
- **Advanced Filtering**: Filter by category, section, metric, and index thresholds
- **AI Strategic Analysis**: Comprehensive 10-insight analysis for Q2 2025 communication strategy
- **Deep Cultural Insights**: In-depth cultural analysis with specific questions about preferences, beliefs, and behaviors
- **Automated Insights**: Chart-specific insights generation for each section
- **Export Capabilities**: Download filtered data as CSV

## Key Metrics

- **Target Percent**: Percentage representation of the Hilton Deep Divers segment
- **Control Percent**: National average for comparison
- **Index**: Relative affinity metric (100 = national average, >150 = strong over-indexing)

## Data Source

YouGov Profiles+ USA 2025-12-07
- Target Group: Hilton Deep Divers (n=93)
- Control Group: Nationally representative (n=411,511)

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure the CSV file is in the root directory:
- `Various_HIlton - Deep DiversvsNationally representative.csv`

3. Run the application:
```bash
streamlit run app.py
```

## Deployment Options

### Option 1: Streamlit Community Cloud (⭐ Recommended - Free)

1. Push your code to GitHub (see `GITHUB_SETUP.md`)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub
4. Click "New app"
5. Select your repository: `ojpb2000/deep-divers-yougov`
6. Main file path: `app.py`
7. Click "Deploy"
8. Your dashboard will be live at a public URL!

### Option 2: Replit

This project is configured for Replit deployment:

1. Import the project into Replit (from GitHub or upload files)
2. The `.replit` file will automatically configure the run command
3. Click "Run" to start the dashboard
4. The dashboard will be available on the Replit webview

See `REPLIT_DEPLOYMENT.md` for detailed instructions.

### Option 3: Local Development

```bash
pip install -r requirements.txt
streamlit run app.py
```

Access at `http://localhost:8080`

## Project Structure

```
.
├── app.py              # Main Streamlit application
├── data_parser.py      # CSV parsing and data processing
├── requirements.txt    # Python dependencies
├── .replit             # Replit configuration
├── .streamlit/         # Streamlit configuration
│   └── config.toml
├── Various_HIlton - Deep DiversvsNationally representative.csv  # Data file
├── GITHUB_SETUP.md     # Guide for GitHub setup
├── REPLIT_DEPLOYMENT.md # Guide for Replit deployment
└── README.md           # This file
```

## Usage

### Main Dashboard
1. Use the sidebar to navigate between categories and sections
2. Adjust filters to focus on specific metrics or index ranges
3. Explore different chart types in the tabs (Comparison, Index Analysis, Scatter Plot, Data Table)
4. Review automated insights for each chart
5. Export filtered data as needed

### AI Strategic Analysis
- Click "🤖 View AI Summary" in the sidebar
- Get comprehensive 10-insight analysis for Q2 2025 communication strategy
- Each insight includes charts and strategic implications

### Deep Cultural Insights
- Click "🔍 Deep Cultural Insights" in the sidebar
- Explore specific cultural questions:
  - What hotels and destinations do they prefer?
  - What do they do during vacations?
  - What spring activities can we leverage for Q2?
  - What type of concerts/events do they like?
  - What sports/leagues do they follow?
  - What do they like to do? (hobbies)
  - What do they believe in?
  - What do they detest/reject?
  - What brands do they like?
  - Cultural patterns and connections

## Insights Interpretation

- **Index ≥120**: Good affinity - 20%+ more likely than national average
- **Index 100-120**: Moderate affinity
- **Index <100**: Under-indexing - less likely than average

## License

Internal use for Hilton analytics.

