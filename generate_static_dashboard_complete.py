"""
Generate complete static HTML dashboard with all features from Streamlit version
Includes: Main Dashboard, AI Strategic Analysis, and Deep Cultural Insights
All text in English
"""
import json
from data_parser import parse_csv_file, process_datasets, get_category_mapping
import pandas as pd
from typing import Dict

# Import analysis functions from app.py logic
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

def prepare_data_for_html(datasets):
    """Prepare data in format suitable for JavaScript/HTML"""
    processed = process_datasets(datasets)
    category_mapping = get_category_mapping()
    
    dashboard_data = {
        'sections': {},
        'categories': category_mapping,
        'metadata': {
            'target_group': 'Hilton Deep Divers (n=93)',
            'control_group': 'Nationally representative (n=411,511)',
            'data_source': 'YouGov Profiles+ USA 2025-12-07'
        }
    }
    
    for section_name, section_data in processed.items():
        df = section_data['data']
        df_valid = df[
            (df['Target percent'].notna()) & 
            (df['Target percent'] > 0) &
            (df['Index'].notna())
        ].copy()
        
        if df_valid.empty:
            continue
        
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

def generate_ai_insights_data(df_all: pd.DataFrame) -> list:
    """Generate AI insights data for HTML"""
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
            'avg_index': [avg_high, avg_low],
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
    
    insights.append({
        'title': '🚀 Q2 Strategic Communication Opportunities',
        'description': f"For Q2 2025, the data reveals clear opportunities: Springtime activities show strong engagement (average Index {q2_opportunities['index'].mean():.0f} for top items), travel intent is high, and premium experiences resonate strongly. The audience is primed for communications around luxury spring travel, exclusive events, and premium lifestyle experiences. With {len(q2_opportunities)} high-affinity items identified, there are multiple touchpoints for strategic messaging.",
        'implication': 'Launch Q2 campaigns focused on spring travel, premium experiences, and luxury lifestyle. Use multiple channels (premium digital platforms, exclusive events, luxury partnerships) to reach this sophisticated audience.',
        'chart_data': q2_opportunities.head(8).to_dict('records'),
        'chart_type': 'q2'
    })
    
    return insights

def generate_cultural_insights_data(df_all: pd.DataFrame) -> list:
    """Generate cultural insights data for HTML"""
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
    
    return insights

def generate_chart_insights_data(items):
    """Generate chart-specific insights"""
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

# Continue with HTML generation...
# This is getting very long, let me create the complete file in the next part

