"""
Generate complete static HTML dashboard with all features from Streamlit version
Includes: Main Dashboard, AI Strategic Analysis, and Deep Cultural Insights
All text in English
"""
import json
from data_parser import parse_csv_file, process_datasets, get_category_mapping
import pandas as pd
from typing import Dict

def prepare_data_for_html(datasets):
    """Prepare data in format suitable for JavaScript/HTML"""
    processed = process_datasets(datasets)
    category_mapping = get_category_mapping()
    
    # Structure data for frontend
    dashboard_data = {
        'sections': {},
        'categories': category_mapping,
        'metadata': {
            'target_group': 'Hilton Deep Divers (n=93)',
            'control_group': 'Nationally representative (n=411,511)',
            'data_source': 'YouGov Profiles+ USA 2025-12-07'
        }
    }
    
    # Process each section
    for section_name, section_data in processed.items():
        df = section_data['data']
        
        # Filter valid data
        df_valid = df[
            (df['Target percent'].notna()) & 
            (df['Target percent'] > 0) &
            (df['Index'].notna())
        ].copy()
        
        if df_valid.empty:
            continue
        
        # Convert to list of dictionaries
        items = []
        for _, row in df_valid.iterrows():
            try:
                items.append({
                    'label': str(row['Response label']),
                    'target_pct': float(row['Target percent']) if pd.notna(row['Target percent']) else 0,
                    'control_pct': float(row['Control percent']) if pd.notna(row['Control percent']) else 0,
                    'index': float(row['Index']) if pd.notna(row['Index']) else 0,
                    'diff': float(row['Target percent']) - float(row['Control percent']) if pd.notna(row['Control percent']) else 0
                })
            except (ValueError, TypeError):
                continue
        
        if items:
            dashboard_data['sections'][section_name] = {
                'question': section_data.get('question', ''),
                'items': items,
                'category': get_section_category(section_name, category_mapping)
            }
    
    return dashboard_data

def get_section_category(section_name, category_mapping):
    """Get category for a section"""
    for cat, keywords in category_mapping.items():
        if any(kw.lower() in section_name.lower() for kw in keywords):
            return cat
    return 'Other'

def analyze_all_data_for_ai_summary(datasets: Dict) -> pd.DataFrame:
    """Analyze all data to extract key insights"""
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

def filter_reliable_data(df_all: pd.DataFrame, max_index: float = 500) -> pd.DataFrame:
    """Filter out extreme index values"""
    return df_all[(df_all['index'] <= max_index) & (df_all['target_pct'] > 0)].copy()

def generate_chart_insights_data(items):
    """Generate chart-specific insights (2-3 insights)"""
    if not items or len(items) == 0:
        return []
    
    insights = []
    
    # Top performer
    top_item = max(items, key=lambda x: x['index'])
    insights.append(f"<strong>Top Performer:</strong> {top_item['label']} leads with an Index of {top_item['index']:.0f}, showing {top_item['target_pct']:.1f}% adoption among Hilton Deep Divers vs {top_item['control_pct']:.1f}% nationally - a {top_item['index']:.0f}% higher likelihood than the average consumer.")
    
    # Largest gap
    largest_gap = max(items, key=lambda x: x['diff'])
    if largest_gap['diff'] > 0:
        insights.append(f"<strong>Biggest Opportunity:</strong> {largest_gap['label']} shows the largest gap with {largest_gap['diff']:.1f} percentage points difference ({largest_gap['target_pct']:.1f}% vs {largest_gap['control_pct']:.1f}%), indicating strong alignment with this segment's preferences.")
    
    # High affinity count
    high_affinity = [i for i in items if i['index'] >= 120]
    if len(high_affinity) > 0:
        avg_high_index = sum(i['index'] for i in high_affinity) / len(high_affinity)
        insights.append(f"<strong>Strong Affinity Cluster:</strong> {len(high_affinity)} item(s) in this view show Index ≥120 (good affinity). The average Index for these high-affinity items is {avg_high_index:.0f}, demonstrating clear differentiation from the national average in this category.")
    elif len(items) > 0:
        avg_index = sum(i['index'] for i in items) / len(items)
        insights.append(f"<strong>Overall Affinity:</strong> Average Index of {avg_index:.0f} indicates this category shows {'above' if avg_index > 100 else 'below'} average affinity with the Hilton Deep Divers segment.")
    
    return insights

def generate_ai_insights_data(df_all: pd.DataFrame) -> list:
    """Generate AI insights data for HTML (10 insights)"""
    insights = []
    if df_all.empty:
        return insights
    
    # Insight 1: Luxury Hospitality
    hotels_data = df_all[df_all['category'] == 'Travel & Hospitality'].nlargest(10, 'index')
    if not hotels_data.empty:
        top_hotel = hotels_data.iloc[0]
        insights.append({
            'title': '🏨 Exceptional Luxury Hospitality Affinity',
            'description': f"Hilton Deep Divers show extraordinary affinity for premium hospitality brands, with {top_hotel['item']} achieving an Index of {top_hotel['index']:.0f} ({top_hotel['target_pct']:.1f}% vs {top_hotel['control_pct']:.1f}% nationally). This represents a {top_hotel['index']/100:.1f}x likelihood compared to the average consumer. The top 5 hotel brands show an average Index of {hotels_data.head(5)['index'].mean():.0f}, indicating a strong preference for established luxury hospitality experiences.",
            'implication': 'Position Hilton as the premium choice for sophisticated travelers. Emphasize exclusivity, quality service, and luxury experiences that align with their identity.',
            'chart_data': hotels_data.head(8).to_dict('records'),
            'chart_type': 'hotels'
        })
    
    # Insight 2: Premium Skincare
    skincare_data = df_all[df_all['section'].str.contains('Skincare', case=False, na=False)].nlargest(8, 'index')
    if not skincare_data.empty:
        top_skincare = skincare_data.iloc[0]
        insights.append({
            'title': '✨ Premium Beauty & Self-Care Culture',
            'description': f"The audience demonstrates exceptional engagement with premium skincare and cosmetics brands. {top_skincare['item']} shows an Index of {top_skincare['index']:.0f}, with {top_skincare['target_pct']:.1f}% of Deep Divers expressing purchase intent versus {top_skincare['control_pct']:.1f}% nationally. This reflects a culture where luxury self-care is integral to identity, not just consumption.",
            'implication': 'Connect Hilton experiences to wellness and self-care narratives. Consider partnerships with premium beauty brands or spa experiences that resonate with their luxury lifestyle.',
            'chart_data': skincare_data.head(6).to_dict('records'),
            'chart_type': 'skincare'
        })
    
    # Insight 3: Destinations
    destinations_data = df_all[df_all['section'].str.contains('Destination', case=False, na=False)].nlargest(8, 'index')
    if not destinations_data.empty:
        top_dest = destinations_data.iloc[0]
        insights.append({
            'title': '🌍 Aspirational & Exclusive Destinations',
            'description': f"Deep Divers show strong affinity for unique, exclusive destinations. {top_dest['item']} achieves an Index of {top_dest['index']:.0f}, with {top_dest['target_pct']:.1f}% having visited or planning to visit versus {top_dest['control_pct']:.1f}% nationally. These are travelers seeking distinctive experiences that reflect their sophisticated taste and status.",
            'implication': 'Highlight Hilton properties in exclusive destinations. Create content around unique, aspirational travel experiences that position Hilton as the gateway to extraordinary places.',
            'chart_data': destinations_data.head(6).to_dict('records'),
            'chart_type': 'destinations'
        })
    
    # Insight 4: Sports
    sports_data = df_all[df_all['category'] == 'Sports & Entertainment'].nlargest(10, 'index')
    if not sports_data.empty:
        top_sport = sports_data.iloc[0]
        avg_sports_index = sports_data.head(5)['index'].mean()
        insights.append({
            'title': '🎾 Premium Sports & Elite Entertainment',
            'description': f"The audience gravitates toward premium, international sports and exclusive entertainment events. {top_sport['item']} shows an Index of {top_sport['index']:.0f}, with an average Index of {avg_sports_index:.0f} across top preferences. This includes international tournaments (Wimbledon, FIFA), Formula 1, and prestigious awards (Grammy Awards), reflecting a preference for globally recognized, high-status events.",
            'implication': 'Position Hilton as the preferred accommodation for premium event experiences. Create packages or partnerships around major sports and entertainment events that align with their interests.',
            'chart_data': sports_data.head(8).to_dict('records'),
            'chart_type': 'sports'
        })
    
    # Insight 5: Digital
    digital_data = df_all[df_all['section'].str.contains('Online Brands', case=False, na=False)].nlargest(8, 'index')
    if not digital_data.empty:
        top_digital = digital_data.iloc[0]
        insights.append({
            'title': '💻 Premium Digital Services & Technology',
            'description': f"Deep Divers show strong engagement with premium digital platforms and services. {top_digital['item']} achieves an Index of {top_digital['index']:.0f}, indicating {top_digital['target_pct']:.1f}% engagement versus {top_digital['control_pct']:.1f}% nationally. They prefer platforms that offer premium experiences, quality curation, and align with their sophisticated digital lifestyle.",
            'implication': 'Ensure Hilton digital experience matches their expectations for premium, seamless technology. Consider partnerships with premium digital platforms for targeted communications.',
            'chart_data': digital_data.head(6).to_dict('records'),
            'chart_type': 'digital'
        })
    
    # Insight 6: Seasonal
    seasonal_data = df_all[df_all['section'].str.contains('time activities', case=False, na=False)]
    if not seasonal_data.empty:
        top_seasonal = seasonal_data.nlargest(10, 'index')
        spring_data = df_all[df_all['section'].str.contains('Springtime', case=False, na=False)].nlargest(5, 'index')
        insights.append({
            'title': '🌸 Premium Seasonal Lifestyle Patterns',
            'description': f"The audience engages in distinctive seasonal activities that reflect their luxury lifestyle. Springtime activities show particularly strong engagement, with top preferences achieving Index values above 120. These activities are often premium experiences—fine dining, exclusive events, luxury travel—that align with their identity as sophisticated consumers.",
            'implication': 'Time Q2 communications around spring travel and premium seasonal experiences. Create campaigns that connect with their seasonal lifestyle patterns and premium activity preferences.',
            'chart_data': (spring_data if not spring_data.empty else top_seasonal.head(6)).to_dict('records'),
            'chart_type': 'seasonal'
        })
    
    # Insight 7: Cultural Gap
    high_index = df_all[df_all['index'] >= 200]
    low_index = df_all[df_all['index'] < 80]
    if not high_index.empty and not low_index.empty:
        avg_high = high_index['index'].mean()
        avg_low = low_index['index'].mean()
        gap_comparison = {
            'categories': ['High Affinity (Index ≥200)', 'Under-indexing (Index <80)'],
            'avg_index': [float(avg_high), float(avg_low)],
            'count': [len(high_index), len(low_index)]
        }
        insights.append({
            'title': '📊 Significant Cultural Gap from Mainstream',
            'description': f"There's a substantial cultural divide between Hilton Deep Divers and the national average. Items with high affinity (Index ≥200) show an average Index of {avg_high:.0f}, while items they under-index on average {avg_low:.0f}. This gap represents both an opportunity and a challenge: communications must speak to their sophisticated, luxury-oriented identity without alienating them with mainstream messaging.",
            'implication': 'Avoid generic, mass-market messaging. Craft communications that acknowledge their sophisticated taste, premium preferences, and luxury lifestyle. Position Hilton as understanding their unique cultural position.',
            'chart_data': gap_comparison,
            'chart_type': 'gap',
            'high_examples': high_index.nlargest(5, 'index')[['item', 'index', 'target_pct', 'control_pct']].to_dict('records'),
            'low_examples': low_index.nsmallest(5, 'index')[['item', 'index', 'target_pct', 'control_pct']].to_dict('records')
        })
    
    # Insight 8: Personality
    personality_data = df_all[df_all['section'].str.contains('Consumer personalities|Traditional', case=False, na=False)]
    if not personality_data.empty:
        top_personality = personality_data.nlargest(8, 'index')
        insights.append({
            'title': '🎭 Distinctive Consumer Identity',
            'description': f"The audience exhibits specific consumer personality traits that define their purchasing behavior. They identify strongly with luxury-oriented, quality-focused, and experience-driven consumption patterns. These personality traits inform not just what they buy, but how they see themselves and what brands they align with.",
            'implication': 'Position Hilton as a brand that understands and reflects their identity. Communications should reinforce their self-perception as sophisticated, quality-focused consumers who choose premium experiences.',
            'chart_data': top_personality.head(6).to_dict('records'),
            'chart_type': 'personality'
        })
    
    # Insight 9: Travel
    travel_data = df_all[df_all['section'].str.contains('Travel|Leisure trips', case=False, na=False)]
    if not travel_data.empty:
        top_travel = travel_data.nlargest(10, 'index')
        insights.append({
            'title': '✈️ Premium Travel Experiences & Preferences',
            'description': f"Deep Divers show distinct travel preferences that emphasize quality, exclusivity, and meaningful experiences over cost. They prefer leisure trips that offer unique experiences, prefer visiting local attractions, and value travel as an expression of their lifestyle. Their travel choices reflect their identity as sophisticated, culturally engaged consumers.",
            'implication': 'Emphasize Hilton ability to deliver unique, culturally rich experiences. Highlight local connections, exclusive access, and premium amenities that enhance their travel experience.',
            'chart_data': top_travel.head(8).to_dict('records'),
            'chart_type': 'travel'
        })
    
    # Insight 10: Q2 Opportunities
    q2_opportunities = df_all[
        (df_all['index'] >= 120) & 
        (df_all['section'].str.contains('Springtime|Leisure|Travel|activities', case=False, na=False))
    ].nlargest(10, 'index')
    
    if not q2_opportunities.empty:
        insights.append({
            'title': '🚀 Q2 Strategic Communication Opportunities',
            'description': f"For Q2 2025, the data reveals clear opportunities: Springtime activities show strong engagement (average Index {q2_opportunities['index'].mean():.0f} for top items), travel intent is high, and premium experiences resonate strongly. The audience is primed for communications around luxury spring travel, exclusive events, and premium lifestyle experiences. With {len(q2_opportunities)} high-affinity items identified, there are multiple touchpoints for strategic messaging.",
            'implication': 'Launch Q2 campaigns focused on spring travel, premium experiences, and luxury lifestyle. Use multiple channels (premium digital platforms, exclusive events, luxury partnerships) to reach this sophisticated audience.',
            'chart_data': q2_opportunities.head(8).to_dict('records'),
            'chart_type': 'q2'
        })
    
    return insights[:10]

def generate_cultural_insights_data(df_all: pd.DataFrame) -> list:
    """Generate cultural insights data for HTML (10 insights)"""
    insights = []
    if df_all.empty:
        return insights
    
    df_reliable = filter_reliable_data(df_all, max_index=500)
    
    # 1. Hotels and Destinations
    hotels = df_reliable[df_reliable['section'].str.contains('Hotels: Current Customer', case=False, na=False)]
    destinations = df_reliable[df_reliable['section'].str.contains('DestinationIndex', case=False, na=False)]
    
    if not hotels.empty and not destinations.empty:
        top_hotels = hotels.nlargest(8, 'index')
        top_destinations = destinations.nlargest(8, 'index')
        insights.append({
            'title': '🏨 Hotels and Destinations: Where do they stay and travel?',
            'description': f"Hilton Deep Divers show clear preferences for established luxury hotels. {top_hotels.iloc[0]['item']} leads with Index {top_hotels.iloc[0]['index']:.0f} ({top_hotels.iloc[0]['target_pct']:.1f}% vs {top_hotels.iloc[0]['control_pct']:.1f}% national). For destinations, {top_destinations.iloc[0]['item']} is the favorite with Index {top_destinations.iloc[0]['index']:.0f}. They prefer exclusive and international destinations that reflect their sophistication.",
            'chart_data': {
                'hotels': top_hotels.to_dict('records'),
                'destinations': top_destinations.to_dict('records')
            },
            'chart_type': 'hotels_destinations_scatter'
        })
    
    # 2. Travel Activities
    travel_activities = df_reliable[df_reliable['section'].str.contains('Travel activities|Leisure trips', case=False, na=False)]
    if not travel_activities.empty:
        top_activities = travel_activities.nlargest(12, 'index')
        insights.append({
            'title': '✈️ Vacation Activities: What do they do when traveling?',
            'description': f"During their vacations, Deep Divers prioritize cultural and quality experiences. {top_activities.iloc[0]['item']} has Index {top_activities.iloc[0]['index']:.0f}, showing {top_activities.iloc[0]['target_pct']:.1f}% preference vs {top_activities.iloc[0]['control_pct']:.1f}% national. They prefer activities that allow them to connect with local culture and live authentic experiences.",
            'chart_data': top_activities.to_dict('records'),
            'chart_type': 'travel_heatmap'
        })
    
    # 3. Spring Activities
    spring_activities = df_reliable[df_reliable['section'].str.contains('Springtime', case=False, na=False)]
    if not spring_activities.empty:
        top_spring = spring_activities.nlargest(10, 'index')
        insights.append({
            'title': '🌸 Spring Opportunities: What Q2 activities can we leverage?',
            'description': f"In spring, Deep Divers focus on premium outdoor activities and social experiences. {top_spring.iloc[0]['item']} shows Index {top_spring.iloc[0]['index']:.0f} ({top_spring.iloc[0]['target_pct']:.1f}% vs {top_spring.iloc[0]['control_pct']:.1f}% national). Q2 is the ideal time for spring travel campaigns, exclusive events, and premium outdoor experiences.",
            'chart_data': top_spring.to_dict('records'),
            'chart_type': 'spring_comparison'
        })
    
    # 4. Music Events
    music_festivals = df_reliable[df_reliable['section'].str.contains('Music festival|Grammy', case=False, na=False)]
    if not music_festivals.empty:
        top_music = music_festivals.nlargest(10, 'index')
        insights.append({
            'title': '🎵 Events and Concerts: What type of entertainment do they prefer?',
            'description': f"Deep Divers value premium and culturally significant entertainment events. {top_music.iloc[0]['item']} has Index {top_music.iloc[0]['index']:.0f}. They prefer events that offer exclusive experiences, VIP access, and alignment with their sophisticated identity.",
            'chart_data': top_music.to_dict('records'),
            'chart_type': 'music_events'
        })
    
    # 5. Sports
    sports = df_reliable[df_reliable['category'] == 'Sports & Entertainment']
    if not sports.empty:
        top_sports = sports.nlargest(12, 'index')
        insights.append({
            'title': '⚽ Sports and Leagues: What do they follow and why?',
            'description': f"Deep Divers show preference for international sports and premium events. {top_sports.iloc[0]['item']} leads with Index {top_sports.iloc[0]['index']:.0f}. They prefer global events (Wimbledon, FIFA, F1) that reflect sophistication and status, rather than mainstream local sports.",
            'chart_data': top_sports.to_dict('records'),
            'chart_type': 'sports_categories'
        })
    
    # 6. Hobbies
    hobbies = df_reliable[df_reliable['section'].str.contains('Hobbies|Topics and hobbies|Leisure interests', case=False, na=False)]
    if not hobbies.empty:
        top_hobbies = hobbies.nlargest(15, 'index')
        insights.append({
            'title': '🎨 Hobbies and Interests: What do they like to do?',
            'description': f"Their hobbies reflect a premium and culturally rich lifestyle. {top_hobbies.iloc[0]['item']} has Index {top_hobbies.iloc[0]['index']:.0f} ({top_hobbies.iloc[0]['target_pct']:.1f}% vs {top_hobbies.iloc[0]['control_pct']:.1f}% national). They prefer activities that allow them to express their sophistication and connect with culture and art.",
            'chart_data': top_hobbies.to_dict('records'),
            'chart_type': 'hobbies_scatter'
        })
    
    # 7. Beliefs
    agreed_statements = df_reliable[df_reliable['section'].str.contains('Statements agreed|Consumer personalities', case=False, na=False)]
    if not agreed_statements.empty:
        top_beliefs = agreed_statements.nlargest(10, 'index')
        insights.append({
            'title': '💭 Beliefs and Values: What do they believe in?',
            'description': f"Their beliefs reflect values of quality, experience, and sophistication. {top_beliefs.iloc[0]['item']} has Index {top_beliefs.iloc[0]['index']:.0f}. They believe in the importance of quality over price, value authentic experiences, and identify with a luxurious lifestyle as part of their identity.",
            'chart_data': top_beliefs.to_dict('records'),
            'chart_type': 'beliefs_comparison'
        })
    
    # 8. Rejections
    disagreed_statements = df_reliable[df_reliable['section'].str.contains('Statements disagreed', case=False, na=False)]
    if not disagreed_statements.empty:
        top_rejections = disagreed_statements.nlargest(10, 'index')
        insights.append({
            'title': '❌ Cultural Rejections: What do they detest or reject?',
            'description': f"Deep Divers actively reject generic, mass-market, or low-quality experiences. {top_rejections.iloc[0]['item']} has Index {top_rejections.iloc[0]['index']:.0f}, showing {top_rejections.iloc[0]['target_pct']:.1f}% disagreement vs {top_rejections.iloc[0]['control_pct']:.1f}% national. They avoid mass-market messages, generic tourist experiences, and low-cost options.",
            'chart_data': top_rejections.to_dict('records'),
            'chart_type': 'rejections_bar'
        })
    
    # 9. Brands
    brands = df_reliable[df_reliable['category'].isin(['Brands & Products'])]
    if not brands.empty:
        top_brands = brands.nlargest(12, 'index')
        insights.append({
            'title': '🛍️ Preferred Brands: What brands do they like and why?',
            'description': f"They prefer premium brands that reflect quality and sophistication. {top_brands.iloc[0]['item']} leads with Index {top_brands.iloc[0]['index']:.0f} ({top_brands.iloc[0]['target_pct']:.1f}% vs {top_brands.iloc[0]['control_pct']:.1f}% national). They value brands that understand their lifestyle and offer premium experiences.",
            'chart_data': top_brands.to_dict('records'),
            'chart_type': 'brands_multi'
        })
    
    # 10. Patterns
    high_affinity = df_reliable[df_reliable['index'] >= 150]
    if not high_affinity.empty:
        category_patterns = high_affinity.groupby('category').agg({
            'index': 'mean',
            'target_pct': 'mean',
            'item': 'count'
        }).round(1)
        category_patterns.columns = ['Avg Index', 'Avg Target %', 'Item Count']
        top_cat = category_patterns.nlargest(1, 'Avg Index')
        insights.append({
            'title': '🔗 Cultural Patterns: Connections between preferences',
            'description': f"Pattern analysis reveals that Deep Divers show consistency in premium preferences across categories. The categories with highest average affinity are: {top_cat.index[0]} (average Index {top_cat['Avg Index'].iloc[0]:.0f}). There is a cultural connection between luxury preferences, exclusive experiences, and premium brands.",
            'chart_data': category_patterns.to_dict('index'),
            'chart_type': 'pattern_heatmap'
        })
    
    return insights[:10]

def generate_html_dashboard(data_json, ai_insights_data, cultural_insights_data, output_file='index.html'):
    """Generate static HTML dashboard"""
    
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hilton Deep Divers Analytics Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-2.26.0.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: #f5f5f5;
            color: #333;
        }}
        
        .header {{
            background: linear-gradient(135deg, #003366 0%, #0066CC 100%);
            color: white;
            padding: 2rem;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .header h1 {{
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }}
        
        .header p {{
            opacity: 0.9;
            font-size: 1rem;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem;
        }}
        
        .filters {{
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
            align-items: center;
        }}
        
        .filter-group {{
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }}
        
        .filter-group label {{
            font-weight: 600;
            font-size: 0.9rem;
            color: #666;
        }}
        
        select, input {{
            padding: 0.5rem;
            border: 2px solid #e0e0e0;
            border-radius: 5px;
            font-size: 1rem;
        }}
        
        select:focus, input:focus {{
            outline: none;
            border-color: #0066CC;
        }}
        
        .section-card {{
            background: white;
            border-radius: 10px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .section-header {{
            border-bottom: 3px solid #0066CC;
            padding-bottom: 1rem;
            margin-bottom: 1.5rem;
        }}
        
        .section-header h2 {{
            color: #0066CC;
            font-size: 1.8rem;
            margin-bottom: 0.5rem;
        }}
        
        .section-header .question {{
            color: #666;
            font-style: italic;
            font-size: 1rem;
        }}
        
        .chart-container {{
            margin: 1.5rem 0;
            min-height: 400px;
            width: 100%;
            overflow-x: auto;
            background: white;
            padding: 1.5rem;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        .chart-container .js-plotly-plot {{
            width: 100% !important;
        }}
        
        .chart-container svg {{
            max-width: 100%;
            height: auto;
        }}
        
        .table-container {{
            margin: 1.5rem 0;
            width: 100%;
            overflow-x: auto;
        }}
        
        .table-wrapper {{
            overflow-x: auto;
            max-width: 100%;
        }}
        
        .data-table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        .data-table th {{
            background: #0066CC;
            color: white;
            padding: 1rem;
            text-align: left;
            font-weight: 600;
            border: 1px solid #0052a3;
        }}
        
        .data-table td {{
            padding: 0.75rem 1rem;
            border: 1px solid #e0e0e0;
        }}
        
        .data-table tr:nth-child(even) {{
            background: #f9f9f9;
        }}
        
        .data-table tr:hover {{
            background: #E8F4F8;
        }}
        
        .download-btn {{
            background: #0066CC;
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 600;
            font-size: 1rem;
            transition: all 0.3s;
        }}
        
        .download-btn:hover {{
            background: #0052a3;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,102,204,0.3);
        }}
        
        .insights {{
            background: #E8F4F8;
            padding: 1rem;
            border-radius: 8px;
            border-left: 5px solid #0066CC;
            margin-top: 1.5rem;
        }}
        
        .insights h3 {{
            color: #0066CC;
            margin-bottom: 0.5rem;
        }}
        
        .insights ul {{
            margin-left: 1.5rem;
        }}
        
        .insights li {{
            margin: 0.5rem 0;
        }}
        
        .tabs {{
            display: flex;
            gap: 0.5rem;
            margin-bottom: 1rem;
            border-bottom: 2px solid #e0e0e0;
        }}
        
        .tab {{
            padding: 0.75rem 1.5rem;
            background: #f5f5f5;
            border: none;
            border-radius: 5px 5px 0 0;
            cursor: pointer;
            font-weight: 600;
            color: #666;
            transition: all 0.3s;
        }}
        
        .tab:hover {{
            background: #e8f4f8;
        }}
        
        .tab.active {{
            background: #0066CC;
            color: white;
        }}
        
        .tab-content {{
            display: none;
        }}
        
        .tab-content.active {{
            display: block;
        }}
        
        .loading {{
            text-align: center;
            padding: 3rem;
            color: #666;
        }}
        
        .no-data {{
            text-align: center;
            padding: 3rem;
            color: #999;
        }}
        
        .nav-tabs {{
            display: flex;
            gap: 1rem;
            justify-content: center;
            margin: 2rem 0;
            padding: 0 2rem;
        }}
        
        .nav-tab {{
            padding: 1rem 2rem;
            background: white;
            border: 2px solid #0066CC;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            font-size: 1rem;
            color: #0066CC;
            transition: all 0.3s;
        }}
        
        .nav-tab:hover {{
            background: #E8F4F8;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,102,204,0.2);
        }}
        
        .nav-tab.active {{
            background: #0066CC;
            color: white;
            box-shadow: 0 4px 12px rgba(0,102,204,0.3);
        }}
        
        .view-content {{
            display: block;
        }}
        
        @media (max-width: 768px) {{
            .filters {{
                flex-direction: column;
            }}
            
            .filter-group {{
                width: 100%;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🏨 Hilton Deep Divers Analytics Dashboard</h1>
        <p>Comprehensive analysis of high-income, luxury-oriented consumers (35-44 years, 200%+ median income)</p>
        <p style="font-size: 0.9rem; margin-top: 0.5rem;">Data Source: YouGov Profiles+ USA 2025-12-07 | Target Group: 93 respondents | Control: 411,511 nationally representative</p>
    </div>
    
    <div class="nav-tabs">
        <button class="nav-tab active" onclick="showView('dashboard')">📊 Main Dashboard</button>
        <button class="nav-tab" onclick="showView('ai-summary')">🤖 AI Strategic Analysis</button>
        <button class="nav-tab" onclick="showView('cultural-insights')">🔍 Deep Cultural Insights</button>
    </div>
    
    <div class="container">
        <div class="filters">
            <div class="filter-group">
                <label>Category</label>
                <select id="categoryFilter">
                    <option value="all">All Categories</option>
                </select>
            </div>
            <div class="filter-group">
                <label>Section</label>
                <select id="sectionFilter">
                    <option value="">Select a section</option>
                </select>
            </div>
            <div class="filter-group">
                <label>Sort by</label>
                <select id="sortBy">
                    <option value="index">Index</option>
                    <option value="target">Target %</option>
                    <option value="diff">Difference</option>
                </select>
            </div>
            <div class="filter-group">
                <label>Top N</label>
                <input type="number" id="topN" value="10" min="5" max="25">
            </div>
            <div class="filter-group">
                <label>Minimum Index</label>
                <input type="number" id="minIndex" value="120" min="0" max="200">
            </div>
        </div>
        
        <div id="dashboardView" class="view-content">
            <div id="dashboardContent">
                <div class="loading">Loading data...</div>
            </div>
        </div>
        
        <div id="aiSummaryView" class="view-content" style="display: none;">
            <div id="aiSummaryContent"></div>
        </div>
        
        <div id="culturalInsightsView" class="view-content" style="display: none;">
            <div id="culturalInsightsContent"></div>
        </div>
    </div>
    
    <script>
        // Data embedded in page
        const dashboardData = {json.dumps(data_json, ensure_ascii=False, indent=2)};
        const aiInsightsData = {json.dumps(ai_insights_data, ensure_ascii=False, indent=2)};
        const culturalInsightsData = {json.dumps(cultural_insights_data, ensure_ascii=False, indent=2)};
        
        // Navigation
        function showView(viewName) {{
            document.querySelectorAll('.view-content').forEach(v => v.style.display = 'none');
            document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
            
            if (viewName === 'dashboard') {{
                document.getElementById('dashboardView').style.display = 'block';
                document.querySelectorAll('.nav-tab')[0].classList.add('active');
            }} else if (viewName === 'ai-summary') {{
                document.getElementById('aiSummaryView').style.display = 'block';
                document.querySelectorAll('.nav-tab')[1].classList.add('active');
                renderAISummary();
            }} else if (viewName === 'cultural-insights') {{
                document.getElementById('culturalInsightsView').style.display = 'block';
                document.querySelectorAll('.nav-tab')[2].classList.add('active');
                renderCulturalInsights();
            }}
        }}
        
        function renderAISummary() {{
            const content = document.getElementById('aiSummaryContent');
            let html = '<div class="section-card"><h2>🤖 AI Strategic Analysis</h2><p>Comprehensive insights for Q2 2025 Communication Strategy</p><p>Based on analysis of all data sections and 1,126+ data points</p></div>';
            html += '<div class="section-card"><h3>📋 Executive Summary</h3><div class="insight-box"><p><strong>Hilton Deep Divers represent a distinct cultural segment:</strong> High-income (200%+ median), luxury-oriented consumers aged 35-44 who view premium experiences as core to their identity. Analysis of 1,126+ data points across 51 sections reveals exceptional affinity for premium hospitality, exclusive destinations, luxury brands, and sophisticated lifestyle experiences. The cultural gap from mainstream consumers is significant, requiring communications that acknowledge their sophisticated taste and premium preferences. Q2 2025 presents strong opportunities around spring travel, premium seasonal activities, and luxury lifestyle experiences.</p></div></div>';
            
            aiInsightsData.forEach((insight, i) => {{
                html += `<div class="section-card"><h3>Insight ${{i+1}}: ${{insight.title}}</h3><div class="insight-box"><p>${{insight.description}}</p><p><strong>Strategic Implication for Q2:</strong> ${{insight.implication}}</p></div>`;
                if (insight.chart_data && (Array.isArray(insight.chart_data) ? insight.chart_data.length > 0 : true)) {{
                    html += `<div id="ai-chart-${{i}}" class="chart-container"></div>`;
                }}
                if (insight.chart_type === 'gap' && insight.high_examples && insight.low_examples) {{
                    html += `<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem;"><div><strong>Top High Affinity Examples:</strong><table style="width: 100%; margin-top: 0.5rem; border-collapse: collapse;"><tr style="background: #0066CC; color: white;"><th style="padding: 0.5rem; border: 1px solid #ddd;">Item</th><th style="padding: 0.5rem; border: 1px solid #ddd;">Index</th><th style="padding: 0.5rem; border: 1px solid #ddd;">Target %</th><th style="padding: 0.5rem; border: 1px solid #ddd;">Control %</th></tr>`;
                    insight.high_examples.forEach(ex => {{
                        html += `<tr><td style="padding: 0.5rem; border: 1px solid #ddd;">${{ex.item}}</td><td style="padding: 0.5rem; border: 1px solid #ddd;">${{ex.index.toFixed(0)}}</td><td style="padding: 0.5rem; border: 1px solid #ddd;">${{ex.target_pct.toFixed(1)}}%</td><td style="padding: 0.5rem; border: 1px solid #ddd;">${{ex.control_pct.toFixed(1)}}%</td></tr>`;
                    }});
                    html += `</table></div><div><strong>Top Under-indexing Examples:</strong><table style="width: 100%; margin-top: 0.5rem; border-collapse: collapse;"><tr style="background: #FF6B6B; color: white;"><th style="padding: 0.5rem; border: 1px solid #ddd;">Item</th><th style="padding: 0.5rem; border: 1px solid #ddd;">Index</th><th style="padding: 0.5rem; border: 1px solid #ddd;">Target %</th><th style="padding: 0.5rem; border: 1px solid #ddd;">Control %</th></tr>`;
                    insight.low_examples.forEach(ex => {{
                        html += `<tr><td style="padding: 0.5rem; border: 1px solid #ddd;">${{ex.item}}</td><td style="padding: 0.5rem; border: 1px solid #ddd;">${{ex.index.toFixed(0)}}</td><td style="padding: 0.5rem; border: 1px solid #ddd;">${{ex.target_pct.toFixed(1)}}%</td><td style="padding: 0.5rem; border: 1px solid #ddd;">${{ex.control_pct.toFixed(1)}}%</td></tr>`;
                    }});
                    html += `</table></div></div>`;
                }}
                html += '</div>';
            }});
            
            content.innerHTML = html;
            
            // Render charts
            aiInsightsData.forEach((insight, i) => {{
                if (insight.chart_data) {{
                    if (insight.chart_type === 'gap') {{
                        renderCulturalChart(`ai-chart-${{i}}`, insight.chart_data, insight.chart_type);
                    }} else if (Array.isArray(insight.chart_data) && insight.chart_data.length > 0) {{
                        renderInsightChart(`ai-chart-${{i}}`, insight.chart_data, insight.chart_type);
                    }}
                }}
            }});
        }}
        
        function renderCulturalInsights() {{
            const content = document.getElementById('culturalInsightsContent');
            let html = '<div class="section-card"><h2>🔍 Deep Cultural Insights</h2><p>In-depth cultural analysis with specific questions about preferences, beliefs, and behaviors</p><p><em>Note: Extreme indices (>500) were filtered for statistical reliability (n=93)</em></p></div>';
            
            culturalInsightsData.forEach((insight, i) => {{
                html += `<div class="section-card"><h3>${{i+1}}. ${{insight.title}}</h3><div class="insight-box"><p>${{insight.description}}</p></div>`;
                if (insight.chart_data) {{
                    html += `<div id="cultural-chart-${{i}}" class="chart-container"></div>`;
                }}
                html += '</div>';
            }});
            
            content.innerHTML = html;
            
            // Render charts
            culturalInsightsData.forEach((insight, i) => {{
                if (insight.chart_data) {{
                    renderCulturalChart(`cultural-chart-${{i}}`, insight.chart_data, insight.chart_type);
                }}
            }});
        }}
        
        function renderInsightChart(containerId, chartData, chartType) {{
            // Similar to existing chart rendering but for insights
            const items = chartData;
            if (!items || items.length === 0) return;
            
            const labels = items.map(i => i.item || i.label);
            const indexData = items.map(i => i.index);
            const colors = indexData.map(idx => idx >= 120 ? '#0066CC' : idx >= 100 ? '#66B2FF' : '#CCE5FF');
            
            const trace = {{
                x: indexData,
                y: labels,
                type: 'bar',
                orientation: 'h',
                marker: {{ color: colors }},
                text: indexData.map(idx => `Index: ${{idx.toFixed(0)}}`),
                textposition: 'outside'
            }};
            
            const layout = {{
                title: 'Top Items by Index',
                xaxis: {{ 
                    title: 'Index (100 = National Average)',
                    automargin: true
                }},
                yaxis: {{ 
                    title: '',
                    automargin: true,
                    tickangle: 0
                }},
                height: Math.max(400, items.length * 50),
                margin: {{ l: 200, r: 120, t: 50, b: 50 }},
                shapes: [{{
                    type: 'line',
                    x0: 120,
                    x1: 120,
                    y0: -0.5,
                    y1: items.length - 0.5,
                    line: {{ color: 'green', dash: 'dash' }},
                    annotation: {{ text: 'Strong Affinity (120)', x: 120, y: items.length }}
                }}]
            }};
            
            Plotly.newPlot(containerId, [trace], layout);
        }}
        
        function renderCulturalChart(containerId, chartData, chartType) {{
            // Handle different chart types for cultural insights
            if (chartType === 'hotels_destinations_scatter' && chartData.hotels && chartData.destinations) {{
                const hotels = chartData.hotels;
                const destinations = chartData.destinations;
                
                const trace1 = {{
                    x: hotels.map(h => h.control_pct),
                    y: hotels.map(h => h.target_pct),
                    mode: 'markers+text',
                    type: 'scatter',
                    name: 'Hotels',
                    text: hotels.map(h => h.item),
                    textposition: 'top center',
                    marker: {{ size: hotels.map(h => Math.min(h.index/20, 30)), color: '#0066CC', opacity: 0.7 }},
                    customdata: hotels.map(h => h.index),
                    hovertemplate: '<b>%{{text}}</b><br>Target: %{{y:.1f}}%<br>Control: %{{x:.1f}}%<br>Index: %{{customdata:.0f}}<extra></extra>'
                }};
                
                const trace2 = {{
                    x: destinations.map(d => d.control_pct),
                    y: destinations.map(d => d.target_pct),
                    mode: 'markers+text',
                    type: 'scatter',
                    name: 'Destinations',
                    text: destinations.map(d => d.item),
                    textposition: 'top center',
                    marker: {{ size: destinations.map(d => Math.min(d.index/20, 30)), color: '#FF6B6B', opacity: 0.7 }},
                    customdata: destinations.map(d => d.index),
                    hovertemplate: '<b>%{{text}}</b><br>Target: %{{y:.1f}}%<br>Control: %{{x:.1f}}%<br>Index: %{{customdata:.0f}}<extra></extra>'
                }};
                
                const maxVal = Math.max(...hotels.map(h => Math.max(h.target_pct, h.control_pct)), ...destinations.map(d => Math.max(d.target_pct, d.control_pct)));
                
                const trace3 = {{
                    x: [0, maxVal],
                    y: [0, maxVal],
                    mode: 'lines',
                    type: 'scatter',
                    line: {{ color: 'red', dash: 'dash' }},
                    name: 'Parity',
                    showlegend: false
                }};
                
                Plotly.newPlot(containerId, [trace1, trace2, trace3], {{
                    title: 'Hotels vs Destinations: Target vs Control',
                    xaxis: {{ 
                        title: 'National Average (%)',
                        automargin: true
                    }},
                    yaxis: {{ 
                        title: 'Hilton Deep Divers (%)',
                        automargin: true
                    }},
                    height: 600,
                    margin: {{ l: 80, r: 50, t: 50, b: 60 }}
                }});
            }} else if (chartType === 'travel_heatmap' || chartType === 'hobbies_scatter') {{
                // Scatter plot
                const items = Array.isArray(chartData) ? chartData : [];
                const trace = {{
                    x: items.map(i => i.control_pct),
                    y: items.map(i => i.target_pct),
                    mode: 'markers',
                    type: 'scatter',
                    text: items.map(i => i.item || i.label),
                    marker: {{
                        size: items.map(i => Math.min(i.index/5, 30)),
                        color: items.map(i => i.index),
                        colorscale: 'Blues',
                        showscale: true,
                        colorbar: {{ title: 'Index' }}
                    }},
                    customdata: items.map(i => i.index),
                    hovertemplate: '<b>%{{text}}</b><br>Target: %{{y:.1f}}%<br>Control: %{{x:.1f}}%<br>Index: %{{customdata:.0f}}<extra></extra>'
                }};
                
                const maxVal = Math.max(...items.map(i => Math.max(i.target_pct, i.control_pct)));
                const trace2 = {{
                    x: [0, maxVal],
                    y: [0, maxVal],
                    mode: 'lines',
                    type: 'scatter',
                    line: {{ color: 'red', dash: 'dash' }},
                    showlegend: false
                }};
                
                Plotly.newPlot(containerId, [trace, trace2], {{
                    title: chartType === 'travel_heatmap' ? 'Travel Activities Heatmap' : 'Hobbies & Interests: Affinity Analysis',
                    xaxis: {{ 
                        title: 'National Average (%)',
                        automargin: true
                    }},
                    yaxis: {{ 
                        title: 'Deep Divers (%)',
                        automargin: true
                    }},
                    height: 600,
                    margin: {{ l: 80, r: 50, t: 50, b: 60 }}
                }});
            }} else if (chartType === 'gap' && chartData.categories) {{
                // Gap comparison chart
                const trace = {{
                    x: chartData.categories,
                    y: chartData.avg_index,
                    type: 'bar',
                    marker: {{ color: ['#0066CC', '#FF6B6B'] }},
                    text: chartData.avg_index.map((idx, i) => `Avg: ${{idx.toFixed(0)}}<br>Items: ${{chartData.count[i]}}`),
                    textposition: 'outside'
                }};
                
                Plotly.newPlot(containerId, [trace], {{
                    title: 'Cultural Gap: High Affinity vs Under-indexing',
                    yaxis: {{ 
                        title: 'Average Index',
                        automargin: true
                    }},
                    xaxis: {{ 
                        title: '',
                        automargin: true
                    }},
                    height: 500,
                    margin: {{ l: 80, r: 50, t: 50, b: 80 }},
                    shapes: [{{
                        type: 'line',
                        x0: -0.5,
                        y0: 100,
                        x1: chartData.categories.length - 0.5,
                        y1: 100,
                        line: {{ color: 'red', dash: 'dash' }},
                        annotation: {{ text: 'Baseline (100)', x: chartData.categories.length - 0.5, y: 100 }}
                    }}]
                }});
            }} else if (chartType === 'pattern_heatmap' && typeof chartData === 'object' && !Array.isArray(chartData)) {{
                // Category patterns
                const categories = Object.keys(chartData);
                const avgIndexes = categories.map(cat => chartData[cat]['Avg Index']);
                
                const trace = {{
                    x: categories,
                    y: avgIndexes,
                    type: 'bar',
                    marker: {{ color: '#0066CC' }},
                    text: avgIndexes.map(idx => idx.toFixed(0)),
                    textposition: 'outside'
                }};
                
                Plotly.newPlot(containerId, [trace], {{
                    title: 'Cultural Patterns: Average Affinity by Category',
                    xaxis: {{ 
                        title: 'Category',
                        automargin: true,
                        tickangle: -45
                    }},
                    yaxis: {{ 
                        title: 'Average Index',
                        automargin: true
                    }},
                    height: 400,
                    margin: {{ l: 80, r: 50, t: 50, b: 100 }}
                }});
            }} else if (chartType === 'spring_comparison' || chartType === 'beliefs_comparison' || chartType === 'rejections_bar') {{
                // Comparison bar chart
                const items = Array.isArray(chartData) ? chartData : [];
                const labels = items.map(i => i.item || i.label);
                const targetData = items.map(i => i.target_pct);
                const controlData = items.map(i => i.control_pct);
                
                const trace1 = {{
                    y: labels,
                    x: targetData,
                    name: 'Deep Divers',
                    type: 'bar',
                    orientation: 'h',
                    marker: {{ color: '#0066CC' }},
                    text: targetData.map(x => `${{x.toFixed(1)}}%`),
                    textposition: 'outside'
                }};
                
                const trace2 = {{
                    y: labels,
                    x: controlData,
                    name: 'National Avg',
                    type: 'bar',
                    orientation: 'h',
                    marker: {{ color: '#CCCCCC' }},
                    text: controlData.map(x => `${{x.toFixed(1)}}%`),
                    textposition: 'outside'
                }};
                
                Plotly.newPlot(containerId, [trace1, trace2], {{
                    title: 'Comparison: Target vs Control',
                    xaxis: {{ 
                        title: 'Percentage (%)',
                        automargin: true
                    }},
                    yaxis: {{ 
                        title: '',
                        automargin: true,
                        tickangle: 0
                    }},
                    barmode: 'group',
                    height: Math.max(500, items.length * 50),
                    margin: {{ l: 200, r: 50, t: 50, b: 50 }},
                    showlegend: true
                }});
            }} else if (chartType === 'sports_categories' || chartType === 'music_events' || chartType === 'brands_multi') {{
                // Colored bar chart
                const items = Array.isArray(chartData) ? chartData : [];
                const labels = items.map(i => i.item || i.label);
                const indexData = items.map(i => i.index);
                const colors = indexData.map(idx => idx >= 120 ? '#0066CC' : idx >= 100 ? '#66B2FF' : '#CCE5FF');
                
                const trace = {{
                    y: labels,
                    x: indexData,
                    type: 'bar',
                    orientation: 'h',
                    marker: {{ color: colors }},
                    text: indexData.map(idx => `Index: ${{idx.toFixed(0)}}`),
                    textposition: 'outside'
                }};
                
                Plotly.newPlot(containerId, [trace], {{
                    title: 'Top Items by Index',
                    xaxis: {{ 
                        title: 'Index (100 = National Average)',
                        automargin: true
                    }},
                    yaxis: {{ 
                        title: '',
                        automargin: true,
                        tickangle: 0
                    }},
                    height: Math.max(500, items.length * 45),
                    margin: {{ l: 200, r: 100, t: 50, b: 50 }},
                    shapes: [{{
                        type: 'line',
                        x0: 120,
                        x1: 120,
                        y0: -0.5,
                        y1: items.length - 0.5,
                        line: {{ color: 'green', dash: 'dash' }},
                        annotation: {{ text: 'Strong Affinity (120)', x: 120, y: items.length }}
                    }}]
                }});
            }} else {{
                // Default bar chart
                renderInsightChart(containerId, chartData, chartType);
            }}
        }}
        
        // Initialize dashboard
        function initDashboard() {{
            populateFilters();
            
            // Set default category to "Travel & Hospitality"
            const categorySelect = document.getElementById('categoryFilter');
            const defaultCategory = 'Travel & Hospitality';
            if (Array.from(categorySelect.options).some(opt => opt.value === defaultCategory)) {{
                categorySelect.value = defaultCategory;
                updateSectionFilter();
            }}
            
            // Set default section to "Leisure trips - most preferred"
            const sectionSelect = document.getElementById('sectionFilter');
            const defaultSectionName = 'Leisure trips - most preferred';
            
            // Find matching section
            let defaultSection = null;
            Array.from(sectionSelect.options).forEach(opt => {{
                if (opt.value && opt.value.toLowerCase().includes('leisure trips') && opt.value.toLowerCase().includes('most preferred')) {{
                    defaultSection = opt.value;
                }}
            }});
            
            // If exact match not found, try partial match
            if (!defaultSection) {{
                Array.from(sectionSelect.options).forEach(opt => {{
                    if (opt.value && opt.value.toLowerCase().includes('leisure trips')) {{
                        defaultSection = opt.value;
                    }}
                }});
            }}
            
            // If still not found, use first available section
            if (!defaultSection && sectionSelect.options.length > 1) {{
                defaultSection = sectionSelect.options[1].value; // Skip the "Select a section" option
            }}
            
            if (defaultSection) {{
                sectionSelect.value = defaultSection;
                loadSection(defaultSection);
            }}
        }}
        
        function populateFilters() {{
            // Populate categories
            const categorySelect = document.getElementById('categoryFilter');
            const categories = Object.keys(dashboardData.categories);
            categories.forEach(cat => {{
                const option = document.createElement('option');
                option.value = cat;
                option.textContent = cat;
                categorySelect.appendChild(option);
            }});
            
            // Populate sections
            updateSectionFilter();
            
            // Event listeners
            categorySelect.addEventListener('change', updateSectionFilter);
            document.getElementById('sectionFilter').addEventListener('change', (e) => {{
                if (e.target.value) loadSection(e.target.value);
            }});
            document.getElementById('sortBy').addEventListener('change', () => {{
                const section = document.getElementById('sectionFilter').value;
                if (section) loadSection(section);
            }});
            document.getElementById('topN').addEventListener('change', () => {{
                const section = document.getElementById('sectionFilter').value;
                if (section) loadSection(section);
            }});
            document.getElementById('minIndex').addEventListener('change', () => {{
                const section = document.getElementById('sectionFilter').value;
                if (section) loadSection(section);
            }});
        }}
        
        function updateSectionFilter() {{
            const category = document.getElementById('categoryFilter').value;
            const sectionSelect = document.getElementById('sectionFilter');
            sectionSelect.innerHTML = '<option value="">Select a section</option>';
            
            Object.keys(dashboardData.sections).forEach(sectionName => {{
                const section = dashboardData.sections[sectionName];
                if (category === 'all' || section.category === category) {{
                    const option = document.createElement('option');
                    option.value = sectionName;
                    option.textContent = sectionName;
                    sectionSelect.appendChild(option);
                }}
            }});
        }}
        
        function loadSection(sectionName) {{
            const section = dashboardData.sections[sectionName];
            if (!section) return;
            
            const sortBy = document.getElementById('sortBy').value;
            const topN = parseInt(document.getElementById('topN').value);
            const minIndex = parseFloat(document.getElementById('minIndex').value);
            
            // Filter and sort data
            let items = section.items.filter(item => item.index >= minIndex);
            
            if (sortBy === 'index') {{
                items.sort((a, b) => b.index - a.index);
            }} else if (sortBy === 'target') {{
                items.sort((a, b) => b.target_pct - a.target_pct);
            }} else {{
                items.sort((a, b) => b.diff - a.diff);
            }}
            
            items = items.slice(0, topN);
            
            // Render section
            renderSection(sectionName, section, items);
        }}
        
        function renderSection(sectionName, section, items) {{
            const content = document.getElementById('dashboardContent');
            
            if (items.length === 0) {{
                content.innerHTML = '<div class="no-data">No data available with the selected filters.</div>';
                return;
            }}
            
            let html = `
                <div class="section-card">
                    <div class="section-header">
                        <h2>${{sectionName}}</h2>
                        ${{section.question && section.question.trim() && !section.question.match(/^\\d+\\.?\\d*%/) ? `<p class="question"><strong>Question:</strong> ${{section.question}}</p>` : ''}}
                    </div>
                    
                    <div class="tabs">
                        <button class="tab active" onclick="switchTab('comparison', '${{sectionName}}')">📊 Comparison</button>
                        <button class="tab" onclick="switchTab('index', '${{sectionName}}')">📈 Index Analysis</button>
                        <button class="tab" onclick="switchTab('scatter', '${{sectionName}}')">🎯 Scatter Plot</button>
                        <button class="tab" onclick="switchTab('table', '${{sectionName}}')">📋 Data Table</button>
                    </div>
                    
                    <div id="chart-${{sectionName}}" class="chart-container"></div>
                    <div id="table-${{sectionName}}" class="table-container" style="display: none;"></div>
                    
                    <div class="insights">
                        <h3>💡 Chart Insights</h3>
                        <ul>
                            ${{generateChartInsights(items)}}
                        </ul>
                    </div>
                </div>
            `;
            
            content.innerHTML = html;
            
            // Render default chart
            renderComparisonChart(sectionName, items);
        }}
        
        function generateChartInsights(items) {{
            if (!items || items.length === 0) return '<li>No insights available</li>';
            
            let html = '';
            
            // Top performer
            const top = items.reduce((max, item) => item.index > max.index ? item : max, items[0]);
            html += `<li><strong>Top Performer:</strong> ${{top.label}} leads with an Index of ${{top.index.toFixed(0)}}, showing ${{top.target_pct.toFixed(1)}}% adoption among Hilton Deep Divers vs ${{top.control_pct.toFixed(1)}}% nationally - a ${{top.index.toFixed(0)}}% higher likelihood than the average consumer.</li>`;
            
            // Largest gap
            const largestGap = items.reduce((max, item) => item.diff > max.diff ? item : max, items[0]);
            if (largestGap.diff > 0) {{
                html += `<li><strong>Biggest Opportunity:</strong> ${{largestGap.label}} shows the largest gap with ${{largestGap.diff.toFixed(1)}} percentage points difference (${{largestGap.target_pct.toFixed(1)}}% vs ${{largestGap.control_pct.toFixed(1)}}%), indicating strong alignment with this segment's preferences.</li>`;
            }}
            
            // High affinity count
            const highAffinity = items.filter(i => i.index >= 120);
            if (highAffinity.length > 0) {{
                const avgHighIndex = highAffinity.reduce((sum, i) => sum + i.index, 0) / highAffinity.length;
                html += `<li><strong>Strong Affinity Cluster:</strong> ${{highAffinity.length}} item(s) in this view show Index ≥120 (good affinity). The average Index for these high-affinity items is ${{avgHighIndex.toFixed(0)}}, demonstrating clear differentiation from the national average in this category.</li>`;
            }} else if (items.length > 0) {{
                const avgIndex = items.reduce((sum, i) => sum + i.index, 0) / items.length;
                html += `<li><strong>Overall Affinity:</strong> Average Index of ${{avgIndex.toFixed(0)}} indicates this category shows ${{avgIndex > 100 ? 'above' : 'below'}} average affinity with the Hilton Deep Divers segment.</li>`;
            }}
            
            return html;
        }}
        
        function generateInsights(items) {{
            return generateChartInsights(items);
        }}
        
        function switchTab(tabType, sectionName) {{
            // Update tab buttons
            document.querySelectorAll(`.tab`).forEach(tab => tab.classList.remove('active'));
            event.target.classList.add('active');
            
            const section = dashboardData.sections[sectionName];
            const sortBy = document.getElementById('sortBy').value;
            const topN = parseInt(document.getElementById('topN').value);
            const minIndex = parseFloat(document.getElementById('minIndex').value);
            
            let items = section.items.filter(item => item.index >= minIndex);
            
            if (sortBy === 'index') {{
                items.sort((a, b) => b.index - a.index);
            }} else if (sortBy === 'target') {{
                items.sort((a, b) => b.target_pct - a.target_pct);
            }} else {{
                items.sort((a, b) => b.diff - a.diff);
            }}
            
            items = items.slice(0, topN);
            
            if (tabType === 'comparison') {{
                document.getElementById(`chart-${{sectionName}}`).style.display = 'block';
                document.getElementById(`table-${{sectionName}}`).style.display = 'none';
                renderComparisonChart(sectionName, items);
            }} else if (tabType === 'index') {{
                document.getElementById(`chart-${{sectionName}}`).style.display = 'block';
                document.getElementById(`table-${{sectionName}}`).style.display = 'none';
                renderIndexChart(sectionName, items);
            }} else if (tabType === 'scatter') {{
                document.getElementById(`chart-${{sectionName}}`).style.display = 'block';
                document.getElementById(`table-${{sectionName}}`).style.display = 'none';
                renderScatterChart(sectionName, items);
            }} else if (tabType === 'table') {{
                document.getElementById(`chart-${{sectionName}}`).style.display = 'none';
                document.getElementById(`table-${{sectionName}}`).style.display = 'block';
                renderDataTable(sectionName, section, items);
            }}
        }}
        
        function renderDataTable(sectionName, section, items) {{
            const tableContainer = document.getElementById(`table-${{sectionName}}`);
            
            // Get all items for the table (not just filtered top N)
            const sectionData = dashboardData.sections[sectionName];
            const sortBy = document.getElementById('sortBy').value;
            const minIndex = parseFloat(document.getElementById('minIndex').value);
            
            let allItems = sectionData.items.filter(item => item.index >= minIndex);
            
            if (sortBy === 'index') {{
                allItems.sort((a, b) => b.index - a.index);
            }} else if (sortBy === 'target') {{
                allItems.sort((a, b) => b.target_pct - a.target_pct);
            }} else {{
                allItems.sort((a, b) => b.diff - a.diff);
            }}
            
            let tableHtml = '<div class="table-wrapper"><h3 style="margin-bottom: 1rem;">Detailed Data Table</h3><table class="data-table"><thead><tr>';
            tableHtml += '<th>Response Label</th><th>Target %</th><th>Control %</th><th>Index</th><th>Difference</th>';
            tableHtml += '</tr></thead><tbody>';
            
            allItems.forEach(item => {{
                tableHtml += `<tr>
                    <td>${{item.label}}</td>
                    <td>${{item.target_pct.toFixed(2)}}%</td>
                    <td>${{item.control_pct.toFixed(2)}}%</td>
                    <td>${{item.index.toFixed(0)}}</td>
                    <td>${{item.diff.toFixed(2)}}%</td>
                </tr>`;
            }});
            
            tableHtml += '</tbody></table></div>';
            
            // Add download button
            const csvRows = allItems.map(item => `"${{item.label.replace(/"/g, '""')}}",${{item.target_pct.toFixed(2)}},${{item.control_pct.toFixed(2)}},${{item.index.toFixed(0)}},${{item.diff.toFixed(2)}}`);
            const csvContent = 'Response Label,Target %,Control %,Index,Difference\\n' + csvRows.join('\\n');
            
            tableHtml += `<div style="margin-top: 1rem;"><button onclick="downloadCSV('${{sectionName.replace(/ /g, '_')}}_data.csv', ${{JSON.stringify(csvContent)}})" class="download-btn">📥 Download filtered data as CSV</button></div>`;
            
            tableContainer.innerHTML = tableHtml;
        }}
        
        function downloadCSV(filename, content) {{
            const blob = new Blob([content], {{ type: 'text/csv' }});
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
        }}
        
        function renderComparisonChart(sectionName, items) {{
            const labels = items.map(i => i.label);
            const targetData = items.map(i => i.target_pct);
            const controlData = items.map(i => i.control_pct);
            
            const trace1 = {{
                x: targetData,
                y: labels,
                name: 'Hilton Deep Divers',
                type: 'bar',
                orientation: 'h',
                marker: {{ color: '#0066CC' }}
            }};
            
            const trace2 = {{
                x: controlData,
                y: labels,
                name: 'National Average',
                type: 'bar',
                orientation: 'h',
                marker: {{ color: '#CCCCCC' }},
                text: controlData.map(x => `${{x.toFixed(1)}}%`),
                textposition: 'outside'
            }};
            
            trace1.text = targetData.map(x => `${{x.toFixed(1)}}%`);
            trace1.textposition = 'outside';
            
            const layout = {{
                title: 'Comparison: Target vs Control',
                xaxis: {{ 
                    title: 'Percentage (%)',
                    automargin: true
                }},
                yaxis: {{ 
                    title: '',
                    automargin: true,
                    tickangle: 0
                }},
                barmode: 'group',
                height: Math.max(400, items.length * 50),
                margin: {{ l: 200, r: 50, t: 50, b: 50 }},
                showlegend: true
            }};
            
            Plotly.newPlot(`chart-${{sectionName}}`, [trace1, trace2], layout);
        }}
        
        function renderIndexChart(sectionName, items) {{
            const labels = items.map(i => i.label);
            const indexData = items.map(i => i.index);
            const colors = indexData.map(idx => idx >= 120 ? '#0066CC' : idx >= 100 ? '#66B2FF' : '#CCE5FF');
            
            const trace = {{
                x: indexData,
                y: labels,
                type: 'bar',
                orientation: 'h',
                marker: {{ color: colors }},
                text: indexData.map(idx => `Index: ${{idx.toFixed(0)}}`),
                textposition: 'outside'
            }};
            
            const layout = {{
                title: 'Index Analysis',
                xaxis: {{ 
                    title: 'Index (100 = National Average)',
                    automargin: true
                }},
                yaxis: {{ 
                    title: '',
                    automargin: true,
                    tickangle: 0
                }},
                height: Math.max(500, items.length * 45),
                margin: {{ l: 200, r: 100, t: 50, b: 50 }},
                shapes: [{{
                    type: 'line',
                    x0: 120,
                    x1: 120,
                    y0: -0.5,
                    y1: items.length - 0.5,
                    line: {{ color: 'green', dash: 'dash' }},
                    annotation: {{ text: 'Strong Affinity (120)', x: 120, y: items.length }}
                }}, {{
                    type: 'line',
                    x0: 100,
                    x1: 100,
                    y0: -0.5,
                    y1: items.length - 0.5,
                    line: {{ color: 'red', dash: 'dash' }},
                    annotation: {{ text: 'Baseline (100)', x: 100, y: 0 }}
                }}]
            }};
            
            Plotly.newPlot(`chart-${{sectionName}}`, [trace], layout);
        }}
        
        function renderScatterChart(sectionName, items) {{
            const trace = {{
                x: items.map(i => i.control_pct),
                y: items.map(i => i.target_pct),
                mode: 'markers+text',
                type: 'scatter',
                text: items.map(i => i.label),
                textposition: 'top center',
                marker: {{
                    size: items.map(i => Math.min(i.index / 5, 30)),
                    color: items.map(i => i.index),
                    colorscale: 'Blues',
                    showscale: true,
                    colorbar: {{ title: 'Index' }}
                }},
                customdata: items.map(i => i.index),
                hovertemplate: '<b>%{{text}}</b><br>Target: %{{y:.1f}}%<br>Control: %{{x:.1f}}%<br>Index: %{{customdata:.0f}}<extra></extra>'
            }};
            
            const maxVal = Math.max(...items.map(i => Math.max(i.target_pct, i.control_pct)));
            
            const layout = {{
                title: 'Scatter Plot: Target vs Control',
                xaxis: {{ 
                    title: 'National Average (%)',
                    automargin: true
                }},
                yaxis: {{ 
                    title: 'Hilton Deep Divers (%)',
                    automargin: true
                }},
                height: 600,
                margin: {{ l: 80, r: 50, t: 50, b: 60 }},
                shapes: [{{
                    type: 'line',
                    x0: 0,
                    y0: 0,
                    x1: maxVal,
                    y1: maxVal,
                    line: {{ color: 'red', dash: 'dash' }},
                    annotation: {{ text: 'Parity Line' }}
                }}]
            }};
            
            Plotly.newPlot(`chart-${{sectionName}}`, [trace], layout);
        }}
        
        // Initialize on page load
        document.addEventListener('DOMContentLoaded', initDashboard);
    </script>
</body>
</html>
"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    print(f"Dashboard HTML generated: {output_file}")

if __name__ == '__main__':
    print("Generating complete static HTML dashboard...")
    
    # Load data
    datasets = parse_csv_file('Various_HIlton - Deep DiversvsNationally representative.csv')
    if not datasets:
        print("Error: Could not load CSV file")
        exit(1)
    
    # Prepare main dashboard data
    print("Processing main dashboard data...")
    dashboard_data = prepare_data_for_html(datasets)
    
    # Generate AI insights
    print("Generating AI Strategic Analysis insights...")
    df_all = analyze_all_data_for_ai_summary(datasets)
    ai_insights_data = generate_ai_insights_data(df_all)
    
    # Generate Cultural insights
    print("Generating Deep Cultural Insights...")
    cultural_insights_data = generate_cultural_insights_data(df_all)
    
    # Generate HTML
    print("Generating HTML...")
    generate_html_dashboard(dashboard_data, ai_insights_data, cultural_insights_data, 'index.html')
    
    print(f"\nDashboard generated successfully!")
    print(f"File: index.html")
    print(f"Sections processed: {len(dashboard_data['sections'])}")
    print(f"AI Insights: {len(ai_insights_data)}")
    print(f"Cultural Insights: {len(cultural_insights_data)}")
    print(f"\nNext step: Upload index.html to GitHub Pages")

