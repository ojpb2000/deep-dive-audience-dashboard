import pandas as pd
import re
from typing import List, Dict, Tuple

import csv

def parse_csv_file(file_path: str) -> Dict[str, pd.DataFrame]:
    """
    Parse the YouGov Profiles+ CSV file into a dictionary of DataFrames
    organized by question set/category.
    """
    datasets = {}
    current_section = None
    current_question = None
    current_data = []
    headers = None
    
    with open(file_path, 'r', encoding='utf-8-sig') as f:  # utf-8-sig handles BOM
        reader = csv.reader(f)
        rows = list(reader)
    
    i = 0
    while i < len(rows):
        row = rows[i]
        
        # Skip empty rows and metadata
        if not row or i < 8:
            i += 1
            continue
        
        # Join row to check for section headers
        row_str = ','.join(row).strip()
        
        # Check if it's a section header (contains "Target:" and "Control:")
        # Note: csv.reader already strips quotes, so we don't check for starting quote
        if 'Target:' in row_str and 'Control:' in row_str and len(row) > 0:
            # Save previous section if exists
            if current_section and current_data and headers:
                try:
                    df = pd.DataFrame(current_data, columns=headers)
                    if not df.empty and len(df.columns) == len(headers):
                        datasets[current_section] = {
                            'question': current_question,
                            'data': df
                        }
                except Exception as e:
                    print(f"Error saving section {current_section}: {e}")
            
            # Start new section - extract section name from first column
            # Section format: "Section Name, Target: ..., Control: ..."
            # csv.reader already removed quotes, so we just need to split
            section_name = row[0].strip()
            if ',' in section_name:
                section_name = section_name.split(',')[0].strip()
            if not section_name:
                # Try to extract from full row string
                section_name = row_str.split(',')[0].strip()
            current_section = section_name
            current_data = []
            current_question = None
            headers = None
            i += 1
            continue
        
        # Check if it's a question line (next non-empty line after section header)
        # Question should be before the "Response label" header and not contain numeric data patterns
        if current_section and not current_question and not row_str.startswith('Response label'):
            if row_str:
                # Question can be in one cell or span multiple
                # But we need to filter out rows that look like data (contain many numbers/percentages)
                potential_question = ' '.join([cell for cell in row if cell]).strip()
                
                # Check if this looks like a question (not a data row)
                # Data rows typically have many numbers, percentages, or specific patterns
                # Questions are usually text-only or have minimal numbers
                numbers_found = re.findall(r'\d+\.?\d*%?', potential_question)
                has_many_numbers = len(numbers_found) > 4  # More than 4 numbers suggests it's data
                has_data_pattern = bool(re.search(r'\d+\.?\d*%\s+\d+\s+\d+\s+\d+', potential_question))
                
                # If it doesn't look like data, it's probably the question
                if not has_many_numbers and not has_data_pattern:
                    # Clean up the question - extract only the text part
                    # Split by the first occurrence of a percentage followed by numbers
                    # This pattern typically marks the start of data: "63.28% 11 17 23"
                    match = re.search(r'(.+?)(?:\s+\d+\.?\d*%\s+\d+\s+\d+)', potential_question)
                    if match:
                        current_question = match.group(1).strip()
                    else:
                        # Try to remove trailing numeric patterns
                        # Remove patterns like "63.28%" at the end if followed by numbers
                        cleaned = re.sub(r'\s+\d+\.?\d*%\s+.*$', '', potential_question)
                        # If we removed a lot, it was probably data; otherwise keep it
                        if len(cleaned) > len(potential_question) * 0.5:
                            current_question = cleaned.strip()
                        else:
                            current_question = potential_question
                else:
                    # This looks like data, not a question - skip it
                    # The question might be in the section name or we'll use a default
                    pass
            i += 1
            continue
        
        # Check if it's the header row
        if row_str.startswith('Response label'):
            headers = [h.strip() for h in row]
            i += 1
            continue
        
        # Parse data rows
        if headers and len(row) >= len(headers):
            # Clean up the data
            cleaned_row = []
            for j, val in enumerate(row[:len(headers)]):
                cleaned_val = str(val).strip().replace('%', '')
                if cleaned_val == '' or cleaned_val == '-' or cleaned_val == 'nan':
                    cleaned_val = None
                cleaned_row.append(cleaned_val)
            
            # Only add if we have valid data (at least response label)
            if cleaned_row[0] and cleaned_row[0] != 'None':
                current_data.append(cleaned_row)
        
        i += 1
    
    # Save last section
    if current_section and current_data and headers:
        try:
            df = pd.DataFrame(current_data, columns=headers)
            if not df.empty and len(df.columns) == len(headers):
                datasets[current_section] = {
                    'question': current_question,
                    'data': df
                }
        except Exception as e:
            print(f"Error saving final section {current_section}: {e}")
    
    return datasets

def clean_numeric_column(series: pd.Series) -> pd.Series:
    """Clean and convert numeric columns"""
    return pd.to_numeric(series.astype(str).str.replace('%', '').str.replace(',', ''), errors='coerce')

def process_datasets(datasets: Dict) -> Dict[str, pd.DataFrame]:
    """Process datasets to clean numeric columns"""
    processed = {}
    
    for section_name, section_data in datasets.items():
        df = section_data['data'].copy()
        
        # Clean numeric columns
        numeric_cols = ['Target percent', 'Control percent', 'Index', 'Diff', 'Z-Score']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = clean_numeric_column(df[col])
        
        # Filter out rows where Target percent is 0 or null (unless we want to show them)
        # For now, we'll keep them but can filter in the dashboard
        
        processed[section_name] = {
            'question': section_data['question'],
            'data': df
        }
    
    return processed

def get_category_mapping() -> Dict[str, List[str]]:
    """Map question sets to categories for better organization"""
    return {
        'Travel & Hospitality': [
            'Hotels: Current Customer',
            'DestinationIndex: Current Customer',
            'DestinationIndex: Positive Satisfaction',
            'DestinationIndex: Aided Brand Awareness',
            'Amusement, Cruise, Travel Agents',
            'Travel activities',
            'Leisure trips - most preferred',
            'Statements agreed with about Travel',
            'Statements disagreed with about Travel',
            'In Market: Hotels',
        ],
        'Lifestyle & Interests': [
            'Hobbies',
            'Topics and hobbies of interest',
            'Leisure interests',
            'Consumer personalities',
            'Traditional',
            'Springtime activities',
            'Wintertime activities',
            'Autumntime activities',
        ],
        'Sports & Entertainment': [
            'SportsIndex- Events',
            'NBA',
            'NFL',
            'MLB World Series',
            'NASCAR',
            'Formula 1',
            'Wimbledon',
            'FIFA Football World Cup',
            'Major League Soccer',
            'College Football Playoff',
            'Grammy Awards',
            'Music festival',
            'Esports',
        ],
        'Brands & Products': [
            'Skincare & Cosmetics',
            'Online Brands',
            'Communications, Media, and Technology',
            'Clothing',
            'Retail: Apparel',
            'Household and Personal Care',
            'Gambling & Casinos',
        ]
    }

