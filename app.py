import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from data_parser import parse_csv_file, process_datasets, get_category_mapping
import numpy as np
from typing import Dict

# Page configuration
st.set_page_config(
    page_title="Hilton Deep Divers Analytics Dashboard",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #003366;
        text-align: center;
        padding: 1rem 0;
    }
    .section-header {
        font-size: 1.8rem;
        font-weight: bold;
        color: #0066CC;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 3px solid #0066CC;
        padding-bottom: 0.5rem;
    }
    .insight-box {
        background-color: #E8F4F8;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #0066CC;
        margin: 1rem 0;
    }
    .metric-card {
        background-color: #F0F8FF;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    /* Improve tabs visibility */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #F0F8FF;
        padding: 8px;
        border-radius: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #FFFFFF;
        border: 2px solid #0066CC;
        border-radius: 6px;
        padding: 10px 20px;
        font-weight: 600;
        color: #0066CC;
        transition: all 0.3s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #E8F4F8;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,102,204,0.2);
    }
    .stTabs [aria-selected="true"] {
        background-color: #0066CC !important;
        color: #FFFFFF !important;
        border-color: #0066CC !important;
        box-shadow: 0 4px 12px rgba(0,102,204,0.3);
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and process the data"""
    datasets = parse_csv_file("Various_HIlton - Deep DiversvsNationally representative.csv")
    processed = process_datasets(datasets)
    return processed

def create_comparison_chart(df, section_name, top_n=10, metric='Index', question=None):
    """Create a comparison chart between Target and Control"""
    # Filter and sort
    df_filtered = df[df['Target percent'].notna() & (df['Target percent'] != 0)].copy()
    
    if metric == 'Index':
        df_sorted = df_filtered.nlargest(top_n, 'Index')
        title_metric = 'Index'
    elif metric == 'Target percent':
        df_sorted = df_filtered.nlargest(top_n, 'Target percent')
        title_metric = 'Target %'
    else:
        df_sorted = df_filtered.nlargest(top_n, 'Diff')
        title_metric = 'Difference'
    
    if df_sorted.empty:
        return None, None
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=df_sorted['Response label'],
        x=df_sorted['Target percent'],
        name='Hilton Deep Divers',
        orientation='h',
        marker_color='#0066CC',
        text=[f"{x:.1f}%" for x in df_sorted['Target percent']],
        textposition='outside'
    ))
    
    fig.add_trace(go.Bar(
        y=df_sorted['Response label'],
        x=df_sorted['Control percent'],
        name='National Average',
        orientation='h',
        marker_color='#CCCCCC',
        text=[f"{x:.1f}%" for x in df_sorted['Control percent']],
        textposition='outside'
    ))
    
    # Simplify title - remove section name, keep it short
    fig.update_layout(
        title=f"Top {top_n} by {title_metric}",
        xaxis_title="Percentage (%)",
        yaxis_title="",
        barmode='group',
        height=max(400, len(df_sorted) * 40),
        showlegend=True,
        hovermode='closest'
    )
    
    return fig, df_sorted

def create_index_chart(df, section_name, top_n=15, question=None):
    """Create a chart showing Index values"""
    df_filtered = df[df['Index'].notna() & (df['Index'] > 0) & (df['Target percent'].notna()) & (df['Target percent'] != 0)].copy()
    df_sorted = df_filtered.nlargest(top_n, 'Index')
    
    if df_sorted.empty:
        return None, None
    
    colors = ['#0066CC' if idx >= 120 else '#66B2FF' if idx >= 100 else '#CCE5FF' 
              for idx in df_sorted['Index']]
    
    fig = go.Figure(go.Bar(
        x=df_sorted['Index'],
        y=df_sorted['Response label'],
        orientation='h',
        marker_color=colors,
        text=[f"Index: {idx:.0f}" for idx in df_sorted['Index']],
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Index: %{x:.0f}<br>Target: %{customdata[0]:.1f}%<br>Control: %{customdata[1]:.1f}%<extra></extra>',
        customdata=df_sorted[['Target percent', 'Control percent']].values
    ))
    
    fig.add_vline(x=100, line_dash="dash", line_color="red", 
                  annotation_text="Baseline (100)", annotation_position="top")
    
    fig.update_layout(
        title=f"Index Analysis (Top {top_n})",
        xaxis_title="Index (100 = National Average)",
        yaxis_title="",
        height=max(500, len(df_sorted) * 35),
        showlegend=False
    )
    
    return fig, df_sorted

def create_scatter_chart(df, section_name, question=None):
    """Create scatter plot of Target vs Control with Index coloring"""
    df_filtered = df[
        (df['Target percent'].notna()) & 
        (df['Control percent'].notna()) & 
        (df['Index'].notna()) &
        (df['Target percent'] > 0)
    ].copy()
    
    if df_filtered.empty:
        return None, None
    
    fig = px.scatter(
        df_filtered,
        x='Control percent',
        y='Target percent',
        size='Index',
        color='Index',
        hover_name='Response label',
        hover_data=['Index', 'Diff'],
        color_continuous_scale='Blues',
        size_max=20,
        labels={
            'Control percent': 'National Average (%)',
            'Target percent': 'Hilton Deep Divers (%)',
            'Index': 'Index'
        },
        title=f"Target vs Control Comparison"
    )
    
    # Add diagonal line (y=x)
    max_val = max(df_filtered['Control percent'].max(), df_filtered['Target percent'].max())
    fig.add_trace(go.Scatter(
        x=[0, max_val],
        y=[0, max_val],
        mode='lines',
        line=dict(color='red', dash='dash'),
        name='Parity Line',
        showlegend=False
    ))
    
    fig.update_layout(height=600)
    
    return fig, df_filtered

def generate_insights(df, section_name):
    """Generate insights for a section"""
    insights = []
    
    # Filter valid data
    df_filtered = df[
        (df['Target percent'].notna()) & 
        (df['Target percent'] > 0) &
        (df['Index'].notna())
    ].copy()
    
    if df_filtered.empty:
        return ["No significant data available for this section."]
    
    # Top Index
    top_index = df_filtered.nlargest(1, 'Index')
    if not top_index.empty:
        top_row = top_index.iloc[0]
        insights.append(
            f"**Highest Index**: {top_row['Response label']} shows an Index of {top_row['Index']:.0f}, "
            f"meaning Hilton Deep Divers are {top_row['Index']:.0f}% more likely than the national average "
            f"({top_row['Target percent']:.1f}% vs {top_row['Control percent']:.1f}%)."
        )
    
    # Count of high index items
    high_index_count = len(df_filtered[df_filtered['Index'] >= 120])
    if high_index_count > 0:
        insights.append(
            f"**Strong Affinity**: {high_index_count} attribute(s) show an Index ≥120, "
            f"indicating good affinity with the Hilton Deep Divers segment."
        )
    
    # Largest difference
    df_filtered['abs_diff'] = abs(df_filtered['Diff'])
    top_diff = df_filtered.nlargest(1, 'abs_diff')
    if not top_diff.empty:
        top_row = top_diff.iloc[0]
        insights.append(
            f"**Largest Gap**: {top_row['Response label']} has the biggest difference "
            f"({top_row['Diff']:.1f} percentage points) between segments."
        )
    
    # Average index
    avg_index = df_filtered['Index'].mean()
    if avg_index > 100:
        insights.append(
            f"**Overall Affinity**: Average Index of {avg_index:.0f} indicates this category "
            f"generally resonates well with Hilton Deep Divers."
        )
    
    return insights

def generate_chart_insights(df_chart_data, chart_type="comparison"):
    """Generate 2-3 specific insights based on the chart data displayed"""
    insights = []
    
    if df_chart_data is None or df_chart_data.empty:
        return []
    
    # Ensure we have the necessary columns
    required_cols = ['Response label', 'Target percent', 'Control percent', 'Index']
    if not all(col in df_chart_data.columns for col in required_cols):
        return []
    
    # Insight 1: Top performer
    if 'Index' in df_chart_data.columns:
        top_item = df_chart_data.nlargest(1, 'Index')
        if not top_item.empty:
            row = top_item.iloc[0]
            insights.append(
                f"**Top Performer**: {row['Response label']} leads with an Index of {row['Index']:.0f}, "
                f"showing {row['Target percent']:.1f}% adoption among Hilton Deep Divers vs {row['Control percent']:.1f}% nationally - "
                f"a {row['Index']:.0f}% higher likelihood than the average consumer."
            )
    
    # Insight 2: Largest gap or highest percentage
    if 'Diff' in df_chart_data.columns:
        largest_gap = df_chart_data.nlargest(1, 'Diff')
        if not largest_gap.empty:
            row = largest_gap.iloc[0]
            if row['Diff'] > 0:
                insights.append(
                    f"**Biggest Opportunity**: {row['Response label']} shows the largest gap with {row['Diff']:.1f} percentage points difference "
                    f"({row['Target percent']:.1f}% vs {row['Control percent']:.1f}%), indicating strong alignment with this segment's preferences."
                )
    
    # Insight 3: High affinity items count or average
    if 'Index' in df_chart_data.columns:
        high_affinity = df_chart_data[df_chart_data['Index'] >= 120]
        if len(high_affinity) > 0:
            avg_high_index = high_affinity['Index'].mean()
            insights.append(
                f"**Strong Affinity Cluster**: {len(high_affinity)} item(s) in this view show Index ≥120 (good affinity). "
                f"The average Index for these high-affinity items is {avg_high_index:.0f}, demonstrating clear differentiation "
                f"from the national average in this category."
            )
        elif len(df_chart_data) > 0:
            # If no high affinity, mention the average
            avg_index = df_chart_data['Index'].mean()
            if avg_index >= 100:
                insights.append(
                    f"**Overall Performance**: The average Index across displayed items is {avg_index:.0f}, indicating this category "
                    f"generally aligns well with Hilton Deep Divers' interests and preferences."
                )
    
    # Return 2-3 insights
    return insights[:3]

def has_valid_data(df: pd.DataFrame) -> bool:
    """Check if a section has valid data (at least one row with Target percent > 0)"""
    if df is None or df.empty:
        return False
    
    if 'Target percent' not in df.columns:
        return False
    
    # Check if there's at least one row with valid Target percent > 0
    valid_data = df[
        (df['Target percent'].notna()) & 
        (df['Target percent'] > 0)
    ]
    
    return len(valid_data) > 0

def filter_sections_with_data(datasets: Dict) -> Dict:
    """Filter out sections that don't have valid data"""
    filtered = {}
    
    for section_name, section_data in datasets.items():
        if has_valid_data(section_data['data']):
            filtered[section_name] = section_data
    
    return filtered

def analyze_all_data_for_ai_summary(datasets: Dict) -> pd.DataFrame:
    """Analyze all data to extract key insights for AI Summary"""
    all_items = []
    
    for section_name, section_data in datasets.items():
        df = section_data['data']
        if 'Index' in df.columns and 'Response label' in df.columns:
            for _, row in df.iterrows():
                if pd.notna(row.get('Index')) and pd.notna(row.get('Response label')):
                    try:
                        index_val = float(row['Index']) if pd.notna(row['Index']) else 0
                        target_pct = float(row['Target percent']) if pd.notna(row['Target percent']) else 0
                        control_pct = float(row['Control percent']) if pd.notna(row['Control percent']) else 0
                        
                        if index_val > 0 and target_pct > 0:
                            all_items.append({
                                'section': section_name,
                                'item': str(row['Response label']),
                                'index': index_val,
                                'target_pct': target_pct,
                                'control_pct': control_pct,
                                'gap': target_pct - control_pct,
                                'category': get_item_category(section_name)
                            })
                    except (ValueError, TypeError):
                        continue
    
    return pd.DataFrame(all_items) if all_items else pd.DataFrame()

def get_item_category(section_name: str) -> str:
    """Get category for a section"""
    category_mapping = get_category_mapping()
    for cat, keywords in category_mapping.items():
        if any(kw.lower() in section_name.lower() for kw in keywords):
            return cat
    return 'Other'

def generate_ai_insights(df_all: pd.DataFrame, datasets: Dict) -> list:
    """Generate 10 strategic insights based on comprehensive data analysis"""
    insights = []
    
    if df_all.empty:
        return insights
    
    # Insight 1: Luxury Hospitality Affinity
    hotels_data = df_all[df_all['category'] == 'Travel & Hospitality'].nlargest(10, 'index')
    if not hotels_data.empty:
        top_hotel = hotels_data.iloc[0]
        insights.append({
            'title': '🏨 Exceptional Luxury Hospitality Affinity',
            'description': f"""Hilton Deep Divers show extraordinary affinity for premium hospitality brands, with {top_hotel['item']} achieving an Index of {top_hotel['index']:.0f} ({top_hotel['target_pct']:.1f}% vs {top_hotel['control_pct']:.1f}% nationally). This represents a {top_hotel['index']/100:.1f}x likelihood compared to the average consumer. The top 5 hotel brands show an average Index of {hotels_data.head(5)['index'].mean():.0f}, indicating a strong preference for established luxury hospitality experiences.""",
            'implication': 'Position Hilton as the premium choice for sophisticated travelers. Emphasize exclusivity, quality service, and luxury experiences that align with their identity.',
            'chart_data': hotels_data.head(8),
            'chart_type': 'hotels'
        })
    
    # Insight 2: Premium Skincare & Beauty
    skincare_data = df_all[df_all['section'].str.contains('Skincare', case=False, na=False)].nlargest(8, 'index')
    if not skincare_data.empty:
        top_skincare = skincare_data.iloc[0]
        insights.append({
            'title': '✨ Premium Beauty & Self-Care Culture',
            'description': f"""The audience demonstrates exceptional engagement with premium skincare and cosmetics brands. {top_skincare['item']} shows an Index of {top_skincare['index']:.0f}, with {top_skincare['target_pct']:.1f}% of Deep Divers expressing purchase intent versus {top_skincare['control_pct']:.1f}% nationally. This reflects a culture where luxury self-care is integral to identity, not just consumption.""",
            'implication': 'Connect Hilton experiences to wellness and self-care narratives. Consider partnerships with premium beauty brands or spa experiences that resonate with their luxury lifestyle.',
            'chart_data': skincare_data.head(6),
            'chart_type': 'skincare'
        })
    
    # Insight 3: Exclusive Travel Destinations
    destinations_data = df_all[df_all['section'].str.contains('Destination', case=False, na=False)].nlargest(8, 'index')
    if not destinations_data.empty:
        top_dest = destinations_data.iloc[0]
        insights.append({
            'title': '🌍 Aspirational & Exclusive Destinations',
            'description': f"""Deep Divers show strong affinity for unique, exclusive destinations. {top_dest['item']} achieves an Index of {top_dest['index']:.0f}, with {top_dest['target_pct']:.1f}% having visited or planning to visit versus {top_dest['control_pct']:.1f}% nationally. These are travelers seeking distinctive experiences that reflect their sophisticated taste and status.""",
            'implication': 'Highlight Hilton properties in exclusive destinations. Create content around unique, aspirational travel experiences that position Hilton as the gateway to extraordinary places.',
            'chart_data': destinations_data.head(6),
            'chart_type': 'destinations'
        })
    
    # Insight 4: Premium Sports & Events
    sports_data = df_all[df_all['category'] == 'Sports & Entertainment'].nlargest(10, 'index')
    if not sports_data.empty:
        top_sport = sports_data.iloc[0]
        avg_sports_index = sports_data.head(5)['index'].mean()
        insights.append({
            'title': '🎾 Premium Sports & Elite Entertainment',
            'description': f"""The audience gravitates toward premium, international sports and exclusive entertainment events. {top_sport['item']} shows an Index of {top_sport['index']:.0f}, with an average Index of {avg_sports_index:.0f} across top preferences. This includes international tournaments (Wimbledon, FIFA), Formula 1, and prestigious awards (Grammy Awards), reflecting a preference for globally recognized, high-status events.""",
            'implication': 'Position Hilton as the preferred accommodation for premium event experiences. Create packages or partnerships around major sports and entertainment events that align with their interests.',
            'chart_data': sports_data.head(8),
            'chart_type': 'sports'
        })
    
    # Insight 5: Digital Premium Brands
    digital_data = df_all[df_all['section'].str.contains('Online Brands', case=False, na=False)].nlargest(8, 'index')
    if not digital_data.empty:
        top_digital = digital_data.iloc[0]
        insights.append({
            'title': '💻 Premium Digital Services & Technology',
            'description': f"""Deep Divers show strong engagement with premium digital platforms and services. {top_digital['item']} achieves an Index of {top_digital['index']:.0f}, indicating {top_digital['target_pct']:.1f}% engagement versus {top_digital['control_pct']:.1f}% nationally. They prefer platforms that offer premium experiences, quality curation, and align with their sophisticated digital lifestyle.""",
            'implication': 'Ensure Hilton digital experience matches their expectations for premium, seamless technology. Consider partnerships with premium digital platforms for targeted communications.',
            'chart_data': digital_data.head(6),
            'chart_type': 'digital'
        })
    
    # Insight 6: Seasonal Premium Activities
    seasonal_data = df_all[df_all['section'].str.contains('time activities', case=False, na=False)]
    if not seasonal_data.empty:
        top_seasonal = seasonal_data.nlargest(10, 'index')
        spring_data = df_all[df_all['section'].str.contains('Springtime', case=False, na=False)].nlargest(5, 'index')
        insights.append({
            'title': '🌸 Premium Seasonal Lifestyle Patterns',
            'description': f"""The audience engages in distinctive seasonal activities that reflect their luxury lifestyle. Springtime activities show particularly strong engagement, with top preferences achieving Index values above 120. These activities are often premium experiences—fine dining, exclusive events, luxury travel—that align with their identity as sophisticated consumers.""",
            'implication': 'Time Q2 communications around spring travel and premium seasonal experiences. Create campaigns that connect with their seasonal lifestyle patterns and premium activity preferences.',
            'chart_data': spring_data if not spring_data.empty else top_seasonal.head(6),
            'chart_type': 'seasonal'
        })
    
    # Insight 7: Cultural Gap - Luxury vs Mainstream
    high_index = df_all[df_all['index'] >= 200]
    low_index = df_all[df_all['index'] < 80]
    if not high_index.empty and not low_index.empty:
        avg_high = high_index['index'].mean()
        avg_low = low_index['index'].mean()
        
        # Create comparison data for the gap chart
        gap_comparison = pd.DataFrame({
            'Category': ['High Affinity\n(Index ≥200)', 'Under-indexing\n(Index <80)'],
            'Average Index': [avg_high, avg_low],
            'Count': [len(high_index), len(low_index)]
        })
        
        # Also include top high and low examples
        top_high_examples = high_index.nlargest(5, 'index')[['item', 'index', 'target_pct', 'control_pct']].copy()
        top_low_examples = low_index.nsmallest(5, 'index')[['item', 'index', 'target_pct', 'control_pct']].copy()
        
        insights.append({
            'title': '📊 Significant Cultural Gap from Mainstream',
            'description': f"""There's a substantial cultural divide between Hilton Deep Divers and the national average. Items with high affinity (Index ≥200) show an average Index of {avg_high:.0f}, while items they under-index on average {avg_low:.0f}. This gap represents both an opportunity and a challenge: communications must speak to their sophisticated, luxury-oriented identity without alienating them with mainstream messaging.""",
            'implication': 'Avoid generic, mass-market messaging. Craft communications that acknowledge their sophisticated taste, premium preferences, and luxury lifestyle. Position Hilton as understanding their unique cultural position.',
            'chart_data': gap_comparison,
            'chart_type': 'gap',
            'high_examples': top_high_examples,
            'low_examples': top_low_examples
        })
    
    # Insight 8: Consumer Personality Traits
    personality_data = df_all[df_all['section'].str.contains('Consumer personalities|Traditional', case=False, na=False)]
    if not personality_data.empty:
        top_personality = personality_data.nlargest(8, 'index')
        insights.append({
            'title': '🎭 Distinctive Consumer Identity',
            'description': f"""The audience exhibits specific consumer personality traits that define their purchasing behavior. They identify strongly with luxury-oriented, quality-focused, and experience-driven consumption patterns. These personality traits inform not just what they buy, but how they see themselves and what brands they align with.""",
            'implication': 'Position Hilton as a brand that understands and reflects their identity. Communications should reinforce their self-perception as sophisticated, quality-focused consumers who choose premium experiences.',
            'chart_data': top_personality.head(6),
            'chart_type': 'personality'
        })
    
    # Insight 9: Travel Behavior & Preferences
    travel_data = df_all[df_all['section'].str.contains('Travel|Leisure trips', case=False, na=False)]
    if not travel_data.empty:
        top_travel = travel_data.nlargest(10, 'index')
        insights.append({
            'title': '✈️ Premium Travel Experiences & Preferences',
            'description': f"""Deep Divers show distinct travel preferences that emphasize quality, exclusivity, and meaningful experiences over cost. They prefer leisure trips that offer unique experiences, prefer visiting local attractions, and value travel as an expression of their lifestyle. Their travel choices reflect their identity as sophisticated, culturally engaged consumers.""",
            'implication': 'Emphasize Hilton ability to deliver unique, culturally rich experiences. Highlight local connections, exclusive access, and premium amenities that enhance their travel experience.',
            'chart_data': top_travel.head(8),
            'chart_type': 'travel'
        })
    
    # Insight 10: Strategic Communication Opportunities
    q2_opportunities = df_all[
        (df_all['index'] >= 120) & 
        (df_all['section'].str.contains('Springtime|Leisure|Travel|activities', case=False, na=False))
    ].nlargest(10, 'index')
    
    insights.append({
        'title': '🚀 Q2 Strategic Communication Opportunities',
        'description': f"""For Q2 2025, the data reveals clear opportunities: Springtime activities show strong engagement (average Index {q2_opportunities['index'].mean():.0f} for top items), travel intent is high, and premium experiences resonate strongly. The audience is primed for communications around luxury spring travel, exclusive events, and premium lifestyle experiences. With {len(q2_opportunities)} high-affinity items identified, there are multiple touchpoints for strategic messaging.""",
        'implication': 'Launch Q2 campaigns focused on spring travel, premium experiences, and luxury lifestyle. Use multiple channels (premium digital platforms, exclusive events, luxury partnerships) to reach this sophisticated audience.',
        'chart_data': q2_opportunities.head(8),
        'chart_type': 'q2'
    })
    
    return insights

def create_insight_chart(chart_data: pd.DataFrame, chart_type: str, insight_data: dict = None):
    """Create a chart for an insight"""
    if chart_data is None or chart_data.empty:
        return None
    
    if chart_type in ['hotels', 'skincare', 'destinations', 'sports', 'digital', 'seasonal', 'travel', 'q2', 'personality']:
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=chart_data['item'],
            x=chart_data['index'],
            orientation='h',
            marker_color='#0066CC',
            text=[f"Index: {idx:.0f}" for idx in chart_data['index']],
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Index: %{x:.0f}<br>Target: %{customdata[0]:.1f}%<br>Control: %{customdata[1]:.1f}%<extra></extra>',
            customdata=chart_data[['target_pct', 'control_pct']].values
        ))
        
        fig.add_vline(x=120, line_dash="dash", line_color="green", 
                      annotation_text="Strong Affinity (120)", annotation_position="top")
        fig.add_vline(x=100, line_dash="dash", line_color="red", 
                      annotation_text="Baseline (100)", annotation_position="bottom")
        
        fig.update_layout(
            title=f"Top Items by Index",
            xaxis_title="Index (100 = National Average)",
            yaxis_title="",
            height=max(400, len(chart_data) * 40),
            showlegend=False
        )
        
        return fig
    
    elif chart_type == 'gap':
        # Create a comparison chart showing the gap
        fig = go.Figure()
        
        # Bar chart comparing high vs low affinity
        colors = ['#0066CC', '#FF6B6B']
        fig.add_trace(go.Bar(
            x=chart_data['Category'],
            y=chart_data['Average Index'],
            marker_color=colors,
            text=[f"Avg: {idx:.0f}<br>Items: {cnt}" for idx, cnt in zip(chart_data['Average Index'], chart_data['Count'])],
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Average Index: %{y:.0f}<br>Number of Items: %{customdata}<extra></extra>',
            customdata=chart_data['Count'].values
        ))
        
        fig.add_hline(y=100, line_dash="dash", line_color="red", 
                      annotation_text="Baseline (100)", annotation_position="right")
        
        fig.update_layout(
            title="Cultural Gap: High Affinity vs Under-indexing",
            yaxis_title="Average Index",
            xaxis_title="",
            height=500,
            showlegend=False
        )
        
        return fig
    
    return None

def render_ai_summary(datasets: Dict):
    """Render the AI Summary page"""
    st.markdown('<div class="main-header">🤖 AI Strategic Analysis</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; color: #666; margin-bottom: 2rem;">
        <p style="font-size: 1.1rem;">Comprehensive insights for Q2 2025 Communication Strategy</p>
        <p style="font-size: 0.9rem;">Based on analysis of all 51 data sections and 1,126+ data points</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Analyze all data
    with st.spinner("Analyzing all data for strategic insights..."):
        df_all = analyze_all_data_for_ai_summary(datasets)
        insights = generate_ai_insights(df_all, datasets)
    
    if not insights:
        st.warning("Unable to generate insights. Please check the data.")
        return
    
    # Executive Summary
    st.markdown("## 📋 Executive Summary")
    st.markdown("""
    <div class="insight-box">
    <p><strong>Hilton Deep Divers represent a distinct cultural segment:</strong> High-income (200%+ median), 
    luxury-oriented consumers aged 35-44 who view premium experiences as core to their identity. Analysis of 1,126+ 
    data points across 51 sections reveals exceptional affinity for premium hospitality, exclusive destinations, 
    luxury brands, and sophisticated lifestyle experiences. The cultural gap from mainstream consumers is significant, 
    requiring communications that acknowledge their sophisticated taste and premium preferences. Q2 2025 presents 
    strong opportunities around spring travel, premium seasonal activities, and luxury lifestyle experiences.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 10 Strategic Insights
    st.markdown("## 💡 10 Strategic Insights for Q2 2025")
    
    for i, insight in enumerate(insights[:10], 1):
        st.markdown(f"### Insight {i}: {insight['title']}")
        
        st.markdown(f"""
        <div class="insight-box">
        <p>{insight['description']}</p>
        <p><strong>Strategic Implication for Q2:</strong> {insight['implication']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Add chart if available
        if insight.get('chart_data') is not None and not insight['chart_data'].empty:
            fig = create_insight_chart(insight['chart_data'], insight['chart_type'], insight)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
                
                # For gap chart, also show examples
                if insight['chart_type'] == 'gap' and 'high_examples' in insight and 'low_examples' in insight:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**Top High Affinity Examples:**")
                        st.dataframe(
                            insight['high_examples'].rename(columns={
                                'item': 'Item',
                                'index': 'Index',
                                'target_pct': 'Target %',
                                'control_pct': 'Control %'
                            }),
                            use_container_width=True,
                            hide_index=True
                        )
                    with col2:
                        st.markdown("**Top Under-indexing Examples:**")
                        st.dataframe(
                            insight['low_examples'].rename(columns={
                                'item': 'Item',
                                'index': 'Index',
                                'target_pct': 'Target %',
                                'control_pct': 'Control %'
                            }),
                            use_container_width=True,
                            hide_index=True
                        )
        
        if i < 10:
            st.markdown("---")
    
    # Back to Dashboard button
    st.markdown("---")
    if st.button("← Back to Dashboard", type="primary"):
        st.session_state['view'] = 'dashboard'
        st.rerun()

def filter_reliable_data(df_all: pd.DataFrame, max_index: float = 500) -> pd.DataFrame:
    """Filter out extreme index values that may lack statistical reliability (n=93)"""
    return df_all[(df_all['index'] <= max_index) & (df_all['target_pct'] > 0)].copy()

def generate_cultural_insights(df_all: pd.DataFrame, datasets: Dict) -> list:
    """Generate deep cultural insights with specific questions and varied visualizations"""
    insights = []
    
    if df_all.empty:
        return insights
    
    # Filter for statistical reliability (avoid extreme outliers with small sample)
    df_reliable = filter_reliable_data(df_all, max_index=500)
    
    # 1. ¿Qué hoteles y destinos prefieren? (Scatter plot)
    hotels = df_reliable[df_reliable['section'].str.contains('Hotels: Current Customer', case=False, na=False)]
    destinations = df_reliable[df_reliable['section'].str.contains('DestinationIndex', case=False, na=False)]
    
    if not hotels.empty and not destinations.empty:
        top_hotels = hotels.nlargest(8, 'index')
        top_destinations = destinations.nlargest(8, 'index')
        
        insights.append({
            'title': '🏨 Hoteles y Destinos: ¿Dónde se hospedan y viajan?',
            'description': f"""Los Hilton Deep Divers muestran preferencias claras por hoteles de lujo establecidos. {top_hotels.iloc[0]['item']} lidera con Index {top_hotels.iloc[0]['index']:.0f} ({top_hotels.iloc[0]['target_pct']:.1f}% vs {top_hotels.iloc[0]['control_pct']:.1f}% nacional). En destinos, {top_destinations.iloc[0]['item']} es el favorito con Index {top_destinations.iloc[0]['index']:.0f}. Prefieren destinos exclusivos e internacionales que reflejen su sofisticación.""",
            'chart_data': {'hotels': top_hotels, 'destinations': top_destinations},
            'chart_type': 'hotels_destinations_scatter'
        })
    
    # 2. ¿Qué hacen durante sus vacaciones? (Travel activities - Heatmap)
    travel_activities = df_reliable[df_reliable['section'].str.contains('Travel activities|Leisure trips', case=False, na=False)]
    if not travel_activities.empty:
        top_activities = travel_activities.nlargest(12, 'index')
        insights.append({
            'title': '✈️ Actividades Vacacionales: ¿Qué hacen cuando viajan?',
            'description': f"""Durante sus vacaciones, los Deep Divers priorizan experiencias culturales y de calidad. {top_activities.iloc[0]['item']} tiene Index {top_activities.iloc[0]['index']:.0f}, mostrando {top_activities.iloc[0]['target_pct']:.1f}% de preferencia vs {top_activities.iloc[0]['control_pct']:.1f}% nacional. Prefieren actividades que les permitan conectarse con la cultura local y vivir experiencias auténticas.""",
            'chart_data': top_activities,
            'chart_type': 'travel_heatmap'
        })
    
    # 3. ¿Qué hay en primavera que podamos aprovechar? (Spring activities - Bar + Comparison)
    spring_activities = df_reliable[df_reliable['section'].str.contains('Springtime', case=False, na=False)]
    if not spring_activities.empty:
        top_spring = spring_activities.nlargest(10, 'index')
        insights.append({
            'title': '🌸 Oportunidades de Primavera: ¿Qué actividades Q2 podemos aprovechar?',
            'description': f"""En primavera, los Deep Divers se enfocan en actividades premium al aire libre y experiencias sociales. {top_spring.iloc[0]['item']} muestra Index {top_spring.iloc[0]['index']:.0f} ({top_spring.iloc[0]['target_pct']:.1f}% vs {top_spring.iloc[0]['control_pct']:.1f}% nacional). Q2 es momento ideal para campañas de viajes de primavera, eventos exclusivos y experiencias premium al aire libre.""",
            'chart_data': top_spring,
            'chart_type': 'spring_comparison'
        })
    
    # 4. ¿Les gustan conciertos/eventos? ¿De qué tipo? (Music festivals - Grouped analysis)
    music_festivals = df_reliable[df_reliable['section'].str.contains('Music festival|Grammy', case=False, na=False)]
    if not music_festivals.empty:
        top_music = music_festivals.nlargest(10, 'index')
        insights.append({
            'title': '🎵 Eventos y Conciertos: ¿Qué tipo de entretenimiento prefieren?',
            'description': f"""Los Deep Divers valoran eventos de entretenimiento premium y culturalmente significativos. {top_music.iloc[0]['item']} tiene Index {top_music.iloc[0]['index']:.0f}. Prefieren eventos que ofrecen experiencias exclusivas, acceso VIP, y alineación con su identidad sofisticada.""",
            'chart_data': top_music,
            'chart_type': 'music_events'
        })
    
    # 5. ¿Qué ligas de deportes o deportes siguen? (Sports - Multi-category)
    sports = df_reliable[df_reliable['category'] == 'Sports & Entertainment']
    if not sports.empty:
        top_sports = sports.nlargest(12, 'index')
        # Group by sport type
        insights.append({
            'title': '⚽ Deportes y Ligas: ¿Qué siguen y por qué?',
            'description': f"""Los Deep Divers muestran preferencia por deportes internacionales y eventos premium. {top_sports.iloc[0]['item']} lidera con Index {top_sports.iloc[0]['index']:.0f}. Prefieren eventos globales (Wimbledon, FIFA, F1) que reflejan sofisticación y estatus, más que deportes locales mainstream.""",
            'chart_data': top_sports,
            'chart_type': 'sports_categories'
        })
    
    # 6. ¿Qué les gusta hacer? (Hobbies & Interests - Scatter)
    hobbies = df_reliable[df_reliable['section'].str.contains('Hobbies|Topics and hobbies|Leisure interests', case=False, na=False)]
    if not hobbies.empty:
        top_hobbies = hobbies.nlargest(15, 'index')
        insights.append({
            'title': '🎨 Pasatiempos e Intereses: ¿Qué les gusta hacer?',
            'description': f"""Sus hobbies reflejan un estilo de vida premium y culturalmente rico. {top_hobbies.iloc[0]['item']} tiene Index {top_hobbies.iloc[0]['index']:.0f} ({top_hobbies.iloc[0]['target_pct']:.1f}% vs {top_hobbies.iloc[0]['control_pct']:.1f}% nacional). Prefieren actividades que les permiten expresar su sofisticación y conectarse con cultura y arte.""",
            'chart_data': top_hobbies,
            'chart_type': 'hobbies_scatter'
        })
    
    # 7. ¿En qué creen? (Statements agreed - Beliefs)
    agreed_statements = df_reliable[df_reliable['section'].str.contains('Statements agreed|Consumer personalities', case=False, na=False)]
    if not agreed_statements.empty:
        top_beliefs = agreed_statements.nlargest(10, 'index')
        insights.append({
            'title': '💭 Creencias y Valores: ¿En qué creen?',
            'description': f"""Sus creencias reflejan valores de calidad, experiencia y sofisticación. {top_beliefs.iloc[0]['item']} tiene Index {top_beliefs.iloc[0]['index']:.0f}. Creen en la importancia de la calidad sobre el precio, valoran experiencias auténticas y se identifican con un estilo de vida lujoso como parte de su identidad.""",
            'chart_data': top_beliefs,
            'chart_type': 'beliefs_comparison'
        })
    
    # 8. ¿Qué detestan? (Statements disagreed - Rejections)
    disagreed_statements = df_reliable[df_reliable['section'].str.contains('Statements disagreed', case=False, na=False)]
    if not disagreed_statements.empty:
        top_rejections = disagreed_statements.nlargest(10, 'index')
        insights.append({
            'title': '❌ Rechazos Culturales: ¿Qué detestan o rechazan?',
            'description': f"""Los Deep Divers rechazan activamente experiencias genéricas, masivas o de baja calidad. {top_rejections.iloc[0]['item']} tiene Index {top_rejections.iloc[0]['index']:.0f}, mostrando {top_rejections.iloc[0]['target_pct']:.1f}% de desacuerdo vs {top_rejections.iloc[0]['control_pct']:.1f}% nacional. Evitan mensajes masivos, experiencias turísticas genéricas y opciones de bajo costo.""",
            'chart_data': top_rejections,
            'chart_type': 'rejections_bar'
        })
    
    # 9. ¿Qué marcas les gustan? (Brands - Multi-category comparison)
    brands = df_reliable[df_reliable['category'].isin(['Brands & Products'])]
    if not brands.empty:
        top_brands = brands.nlargest(12, 'index')
        insights.append({
            'title': '🛍️ Marcas Preferidas: ¿Qué marcas les gustan y por qué?',
            'description': f"""Prefieren marcas premium que reflejan calidad y sofisticación. {top_brands.iloc[0]['item']} lidera con Index {top_brands.iloc[0]['index']:.0f} ({top_brands.iloc[0]['target_pct']:.1f}% vs {top_brands.iloc[0]['control_pct']:.1f}% nacional). Valoran marcas que entienden su estilo de vida y ofrecen experiencias premium.""",
            'chart_data': top_brands,
            'chart_type': 'brands_multi'
        })
    
    # 10. Patrones Culturales: Conexiones entre categorías (Pattern analysis)
    # Find correlations between high-index items across categories
    high_affinity = df_reliable[df_reliable['index'] >= 150]
    if not high_affinity.empty:
        category_patterns = high_affinity.groupby('category').agg({
            'index': 'mean',
            'target_pct': 'mean',
            'item': 'count'
        }).round(1)
        category_patterns.columns = ['Avg Index', 'Avg Target %', 'Item Count']
        
        insights.append({
            'title': '🔗 Patrones Culturales: Conexiones entre preferencias',
            'description': f"""Análisis de patrones revela que los Deep Divers muestran consistencia en preferencias premium across categorías. Las categorías con mayor afinidad promedio son: {category_patterns.nlargest(1, 'Avg Index').index[0]} (Index promedio {category_patterns.nlargest(1, 'Avg Index')['Avg Index'].iloc[0]:.0f}). Existe una conexión cultural entre preferencias de lujo, experiencias exclusivas y marcas premium.""",
            'chart_data': category_patterns,
            'chart_type': 'pattern_heatmap'
        })
    
    return insights

def create_cultural_chart(chart_data, chart_type: str):
    """Create varied chart types for cultural insights"""
    if chart_data is None or (isinstance(chart_data, pd.DataFrame) and chart_data.empty):
        return None
    
    if chart_type == 'hotels_destinations_scatter':
        fig = go.Figure()
        
        # Hotels scatter
        hotels = chart_data['hotels']
        fig.add_trace(go.Scatter(
            x=hotels['control_pct'],
            y=hotels['target_pct'],
            mode='markers+text',
            name='Hotels',
            marker=dict(size=hotels['index']/20, color='#0066CC', opacity=0.7),
            text=hotels['item'],
            textposition='top center',
            hovertemplate='<b>%{text}</b><br>Target: %{y:.1f}%<br>Control: %{x:.1f}%<br>Index: %{marker.size:.0f}<extra></extra>'
        ))
        
        # Destinations scatter
        destinations = chart_data['destinations']
        fig.add_trace(go.Scatter(
            x=destinations['control_pct'],
            y=destinations['target_pct'],
            mode='markers+text',
            name='Destinations',
            marker=dict(size=destinations['index']/20, color='#FF6B6B', opacity=0.7),
            text=destinations['item'],
            textposition='top center',
            hovertemplate='<b>%{text}</b><br>Target: %{y:.1f}%<br>Control: %{x:.1f}%<br>Index: %{marker.size:.0f}<extra></extra>'
        ))
        
        # Parity line
        max_val = max(hotels['target_pct'].max(), hotels['control_pct'].max(), 
                     destinations['target_pct'].max(), destinations['control_pct'].max())
        fig.add_trace(go.Scatter(
            x=[0, max_val],
            y=[0, max_val],
            mode='lines',
            line=dict(color='red', dash='dash'),
            name='Parity',
            showlegend=False
        ))
        
        fig.update_layout(
            title='Hotels vs Destinations: Target vs Control',
            xaxis_title='National Average (%)',
            yaxis_title='Hilton Deep Divers (%)',
            height=600
        )
        return fig
    
    elif chart_type == 'travel_heatmap':
        # Create heatmap-style visualization
        top_10 = chart_data.head(10)
        fig = go.Figure(data=go.Bar(
            x=top_10['index'],
            y=top_10['item'],
            orientation='h',
            marker=dict(
                color=top_10['index'],
                colorscale='Blues',
                showscale=True,
                colorbar=dict(title="Index")
            ),
            text=[f"Index: {idx:.0f}<br>Target: {t:.1f}%<br>Control: {c:.1f}%" 
                  for idx, t, c in zip(top_10['index'], top_10['target_pct'], top_10['control_pct'])],
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>%{text}<extra></extra>'
        ))
        
        fig.add_vline(x=120, line_dash="dash", line_color="green", 
                      annotation_text="Strong Affinity (120)")
        fig.update_layout(
            title='Travel Activities Heatmap',
            xaxis_title='Index',
            yaxis_title='',
            height=max(500, len(top_10) * 50)
        )
        return fig
    
    elif chart_type in ['spring_comparison', 'beliefs_comparison', 'rejections_bar']:
        top_10 = chart_data.head(10)
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=top_10['item'],
            x=top_10['target_pct'],
            name='Deep Divers',
            orientation='h',
            marker_color='#0066CC',
            text=[f"{x:.1f}%" for x in top_10['target_pct']],
            textposition='outside'
        ))
        
        fig.add_trace(go.Bar(
            y=top_10['item'],
            x=top_10['control_pct'],
            name='National Avg',
            orientation='h',
            marker_color='#CCCCCC',
            text=[f"{x:.1f}%" for x in top_10['control_pct']],
            textposition='outside'
        ))
        
        fig.update_layout(
            title='Comparison: Target vs Control',
            xaxis_title='Percentage (%)',
            yaxis_title='',
            barmode='group',
            height=max(500, len(top_10) * 50)
        )
        return fig
    
    elif chart_type == 'hobbies_scatter':
        top_15 = chart_data.head(15)
        fig = px.scatter(
            top_15,
            x='control_pct',
            y='target_pct',
            size='index',
            color='index',
            hover_name='item',
            hover_data=['index'],
            color_continuous_scale='Blues',
            size_max=30,
            labels={
                'control_pct': 'National Average (%)',
                'target_pct': 'Deep Divers (%)',
                'index': 'Index'
            },
            title='Hobbies & Interests: Affinity Analysis'
        )
        
        max_val = max(top_15['target_pct'].max(), top_15['control_pct'].max())
        fig.add_trace(go.Scatter(
            x=[0, max_val],
            y=[0, max_val],
            mode='lines',
            line=dict(color='red', dash='dash'),
            name='Parity',
            showlegend=False
        ))
        fig.update_layout(height=600)
        return fig
    
    elif chart_type == 'sports_categories':
        top_12 = chart_data.head(12)
        fig = go.Figure(go.Bar(
            x=top_12['index'],
            y=top_12['item'],
            orientation='h',
            marker=dict(
                color=top_12['index'],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Index")
            ),
            text=[f"Index: {idx:.0f}" for idx in top_12['index']],
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Index: %{x:.0f}<br>Target: %{customdata[0]:.1f}%<br>Control: %{customdata[1]:.1f}%<extra></extra>',
            customdata=top_12[['target_pct', 'control_pct']].values
        ))
        
        fig.add_vline(x=120, line_dash="dash", line_color="green", 
                      annotation_text="Strong Affinity (120)")
        fig.update_layout(
            title='Sports & Leagues: Interest Levels',
            xaxis_title='Index',
            yaxis_title='',
            height=max(500, len(top_12) * 40)
        )
        return fig
    
    elif chart_type == 'pattern_heatmap':
        # Create heatmap of category patterns
        fig = go.Figure(data=go.Heatmap(
            z=[[chart_data['Avg Index'].max()]],
            x=['Average Index'],
            y=chart_data.index.tolist(),
            colorscale='Blues',
            showscale=True,
            text=[[f"{val:.0f}" for val in chart_data['Avg Index']]],
            texttemplate='%{text}',
            textfont={"size":12}
        ))
        # Actually, let's use a bar chart for better readability
        fig = go.Figure(go.Bar(
            x=chart_data.index,
            y=chart_data['Avg Index'],
            marker_color='#0066CC',
            text=[f"{val:.0f}" for val in chart_data['Avg Index']],
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Avg Index: %{y:.0f}<br>Items: %{customdata}<extra></extra>',
            customdata=chart_data['Item Count'].values
        ))
        fig.update_layout(
            title='Cultural Patterns: Average Affinity by Category',
            xaxis_title='Category',
            yaxis_title='Average Index',
            height=400
        )
        return fig
    
    elif chart_type in ['music_events', 'brands_multi']:
        top_10 = chart_data.head(10)
        fig = go.Figure(go.Bar(
            y=top_10['item'],
            x=top_10['index'],
            orientation='h',
            marker=dict(
                color=top_10['index'],
                colorscale='Blues',
                showscale=True,
                colorbar=dict(title="Index")
            ),
            text=[f"Index: {idx:.0f}" for idx in top_10['index']],
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Index: %{x:.0f}<br>Target: %{customdata[0]:.1f}%<br>Control: %{customdata[1]:.1f}%<extra></extra>',
            customdata=top_10[['target_pct', 'control_pct']].values
        ))
        
        fig.add_vline(x=120, line_dash="dash", line_color="green", 
                      annotation_text="Strong Affinity (120)")
        fig.update_layout(
            title=f'Top Items by Index',
            xaxis_title='Index',
            yaxis_title='',
            height=max(500, len(top_10) * 45)
        )
        return fig
    
    return None

def render_cultural_insights(datasets: Dict):
    """Render the Deep Cultural Insights page"""
    st.markdown('<div class="main-header">🔍 Deep Cultural Insights</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; color: #666; margin-bottom: 2rem;">
        <p style="font-size: 1.1rem;">Análisis Cultural Profundo: Hallazgos Específicos sobre la Audiencia</p>
        <p style="font-size: 0.9rem;">Enfoque en preguntas específicas, patrones culturales y oportunidades Q2 2025</p>
        <p style="font-size: 0.85rem; color: #999;"><em>Nota: Índices extremos (>500) fueron filtrados por confiabilidad estadística (n=93)</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Analyze all data
    with st.spinner("Analizando datos para insights culturales profundos..."):
        df_all = analyze_all_data_for_ai_summary(datasets)
        insights = generate_cultural_insights(df_all, datasets)
    
    if not insights:
        st.warning("No se pudieron generar insights. Por favor verifica los datos.")
        return
    
    # Display insights
    for i, insight in enumerate(insights, 1):
        st.markdown(f"### {i}. {insight['title']}")
        
        st.markdown(f"""
        <div class="insight-box">
        <p>{insight['description']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Add chart
        if insight.get('chart_data') is not None:
            fig = create_cultural_chart(insight['chart_data'], insight['chart_type'])
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        
        if i < len(insights):
            st.markdown("---")
    
    # Back to Dashboard button
    st.markdown("---")
    if st.button("← Back to Dashboard", type="primary"):
        st.session_state['view'] = 'dashboard'
        st.rerun()

def main():
    # Initialize session state for navigation
    if 'view' not in st.session_state:
        st.session_state['view'] = 'dashboard'
    
    # Check if we should show AI Summary or Cultural Insights
    if st.session_state.get('view') == 'ai_summary':
        datasets = load_data()
        if datasets:
            datasets = filter_sections_with_data(datasets)
            render_ai_summary(datasets)
        else:
            st.error("Could not load data. Please check the file.")
        return
    
    if st.session_state.get('view') == 'cultural_insights':
        datasets = load_data()
        if datasets:
            datasets = filter_sections_with_data(datasets)
            render_cultural_insights(datasets)
        else:
            st.error("Could not load data. Please check the file.")
        return
    
    # Header
    st.markdown('<div class="main-header">🏨 Hilton Deep Divers Analytics Dashboard</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; color: #666; margin-bottom: 2rem;">
        <p style="font-size: 1.1rem;">Comprehensive analysis of high-income, luxury-oriented consumers (35-44 years, 200%+ median income)</p>
        <p style="font-size: 0.9rem;">Data Source: YouGov Profiles+ USA 2025-12-07 | Target Group: 93 respondents | Control: 411,511 nationally representative</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load data
    with st.spinner("Loading data..."):
        datasets = load_data()
    
    if not datasets:
        st.error("Could not load data. Please check the file.")
        return
    
    # Filter sections with valid data
    datasets = filter_sections_with_data(datasets)
    
    if not datasets:
        st.error("No sections with valid data found.")
        return
    
    # Sidebar filters
    st.sidebar.header("🔍 Filters & Navigation")
    
    # Navigation buttons
    st.sidebar.markdown("---")
    if st.sidebar.button("🔍 Deep Cultural Insights", type="primary", use_container_width=True):
        st.session_state['view'] = 'cultural_insights'
        st.rerun()
    if st.sidebar.button("🤖 View AI Summary", type="secondary", use_container_width=True):
        st.session_state['view'] = 'ai_summary'
        st.rerun()
    st.sidebar.markdown("---")
    
    # Category filter
    category_mapping = get_category_mapping()
    all_categories = ['All Categories'] + list(category_mapping.keys())
    
    # Set default category to "Lifestyle & Interests"
    default_category_index = 0
    if 'Lifestyle & Interests' in all_categories:
        default_category_index = all_categories.index('Lifestyle & Interests')
    
    selected_category = st.sidebar.selectbox("Select Category", all_categories, index=default_category_index)
    
    # Section filter - only show sections with data
    if selected_category == 'All Categories':
        available_sections = list(datasets.keys())
    else:
        category_keywords = category_mapping[selected_category]
        available_sections = [
            section for section in datasets.keys()
            if any(cat_keyword.lower() in section.lower() for cat_keyword in category_keywords)
        ]
    
    if not available_sections:
        st.sidebar.warning("No sections available in this category.")
        st.info("Please select a different category or section.")
        return
    
    # Set default section to "Springtime activities"
    default_section_index = 0
    default_section_name = "Springtime activities"
    
    # Try to find exact match first
    matching_sections = [s for s in available_sections if default_section_name.lower() in s.lower()]
    if matching_sections:
        default_section_index = available_sections.index(matching_sections[0])
    
    selected_section = st.sidebar.selectbox("Select Section", available_sections, index=default_section_index)
    
    # Metric filter
    metric_choice = st.sidebar.radio(
        "Sort by Metric",
        ["Index", "Target percent", "Difference"],
        help="Index: Relative affinity (100 = average)\nTarget %: Absolute percentage\nDifference: Gap between segments"
    )
    
    # Top N filter
    top_n = st.sidebar.slider("Number of items to show", 5, 25, 10)
    
    # Index threshold filter
    min_index = st.sidebar.slider("Minimum Index", 0, 200, 120)
    
    # Main content
    if selected_section and selected_section in datasets:
        section_data = datasets[selected_section]
        df = section_data['data'].copy()
        
        # Apply index filter - show items with index >= min_index OR items with no index data
        df_display = df[
            (df['Index'].isna()) | (df['Index'] >= min_index) |
            ((df['Target percent'].notna()) & (df['Target percent'] > 0))
        ].copy()
        
        # Check if we have data to display
        has_data = len(df[(df['Target percent'].notna()) & (df['Target percent'] > 0)]) > 0
        
        if not has_data:
            st.warning("This section doesn't have valid data to display.")
            return
        
        # Charts - simplified layout, no header, no metrics, no general insights
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Comparison", 
            "📈 Index Analysis", 
            "🎯 Scatter Plot", 
            "📋 Data Table"
        ])
        
        with tab1:
            # Show question if available - right below tab title
            if section_data['question']:
                st.markdown(f"**Question:** {section_data['question']}")
                st.markdown("---")
            
            fig, chart_data = create_comparison_chart(df_display, selected_section, top_n, metric_choice, section_data['question'])
            if fig:
                st.plotly_chart(fig, use_container_width=True)
                
                # Generate and display chart-specific insights
                chart_insights = generate_chart_insights(chart_data, "comparison")
                if chart_insights:
                    st.markdown("#### 💡 Chart Insights")
                    for insight in chart_insights:
                        st.markdown(f'<div class="insight-box">{insight}</div>', unsafe_allow_html=True)
            else:
                st.info("No data available for this chart with current filters.")
        
        with tab2:
            # Show question if available
            if section_data['question']:
                st.markdown(f"**Question:** {section_data['question']}")
                st.markdown("---")
            
            st.markdown("""
            <div style="background-color: #E8F4F8; padding: 1rem; border-radius: 5px; margin-bottom: 1rem;">
                <strong>Understanding Index:</strong><br>
                • <strong>Index ≥120</strong>: Good affinity (20%+ more likely than average)<br>
                • <strong>Index 100-120</strong>: Moderate affinity<br>
                • <strong>Index <100</strong>: Under-indexing (less likely than average)
            </div>
            """, unsafe_allow_html=True)
            
            fig, chart_data = create_index_chart(df_display, selected_section, top_n, section_data['question'])
            if fig:
                st.plotly_chart(fig, use_container_width=True)
                
                # Generate and display chart-specific insights
                chart_insights = generate_chart_insights(chart_data, "index")
                if chart_insights:
                    st.markdown("#### 💡 Chart Insights")
                    for insight in chart_insights:
                        st.markdown(f'<div class="insight-box">{insight}</div>', unsafe_allow_html=True)
            else:
                st.info("No data available for this chart with current filters.")
        
        with tab3:
            # Show question if available
            if section_data['question']:
                st.markdown(f"**Question:** {section_data['question']}")
                st.markdown("---")
            
            st.markdown("""
            <div style="background-color: #E8F4F8; padding: 1rem; border-radius: 5px; margin-bottom: 1rem;">
                <strong>How to read:</strong> Points above the red line indicate over-indexing. 
                Larger, darker points have higher Index values.
            </div>
            """, unsafe_allow_html=True)
            
            fig, chart_data = create_scatter_chart(df_display, selected_section, section_data['question'])
            if fig:
                st.plotly_chart(fig, use_container_width=True)
                
                # Generate and display chart-specific insights
                # For scatter plot, use top items by Index
                if chart_data is not None and not chart_data.empty:
                    top_scatter = chart_data.nlargest(10, 'Index')
                    chart_insights = generate_chart_insights(top_scatter, "scatter")
                    if chart_insights:
                        st.markdown("#### 💡 Chart Insights")
                        for insight in chart_insights:
                            st.markdown(f'<div class="insight-box">{insight}</div>', unsafe_allow_html=True)
            else:
                st.info("No data available for this chart with current filters.")
        
        with tab4:
            # Show question if available
            if section_data['question']:
                st.markdown(f"**Question:** {section_data['question']}")
                st.markdown("---")
            
            st.markdown("### Detailed Data Table")
            # Filter columns
            display_cols = ['Response label', 'Target percent', 'Control percent', 'Index', 'Diff', 'Z-Score']
            available_cols = [col for col in display_cols if col in df_display.columns]
            
            # Sort
            if metric_choice == 'Index':
                sort_col = 'Index'
            elif metric_choice == 'Target percent':
                sort_col = 'Target percent'
            else:
                sort_col = 'Diff'
            
            if sort_col in df_display.columns:
                df_sorted = df_display.sort_values(sort_col, ascending=False, na_position='last')
            else:
                df_sorted = df_display
            
            st.dataframe(
                df_sorted[available_cols],
                use_container_width=True,
                height=400
            )
            
            # Download button
            csv = df_sorted[available_cols].to_csv(index=False)
            st.download_button(
                label="📥 Download filtered data as CSV",
                data=csv,
                file_name=f"{selected_section.replace(' ', '_')}_data.csv",
                mime="text/csv"
            )
    else:
        st.info("Please select a section from the sidebar to view analysis.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem;">
        <p>Hilton Deep Divers Analytics Dashboard | Built with Streamlit</p>
        <p>Target Audience: High-income luxury consumers (35-44 years, 200%+ median income)</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

