import requests
import pandas as pd
import os
from datetime import datetime
import time

# BLS Series IDs
SERIES_IDS = {
    'Total Nonfarm Employment': 'CES0000000001',
    'Unemployment Rate': 'LNS14000000',
    'Labor Force Participation Rate': 'LNS11300000',
    'Average Hourly Earnings': 'CES0500000003',
    'Manufacturing Employment': 'CES3000000001',
    'Leisure & Hospitality Employment': 'CES7000000001',
    'Professional & Business Services Employment': 'CES6000000001'
}

def fetch_bls_data_single(series_id, start_year, end_year):
    """Fetch data from BLS API for a single series (no API key needed)"""
    url = 'https://api.bls.gov/publicAPI/v1/timeseries/data/'
    
    headers = {'Content-type': 'application/json'}
    
    data = {
        "seriesid": [series_id],
        "startyear": str(start_year),
        "endyear": str(end_year)
    }
    
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code != 200:
        print(f"Error: API returned status code {response.status_code}")
        return None
    
    json_data = response.json()
    
    if json_data['status'] != 'REQUEST_SUCCEEDED':
        print(f"Error: {json_data.get('message', 'Unknown error')}")
        return None
    
    return json_data

def parse_bls_data(json_data, series_id, series_name):
    """Parse BLS JSON response into a list of records"""
    all_data = []
    
    for series in json_data['Results']['series']:
        for item in series['data']:
            all_data.append({
                'date': f"{item['year']}-{item['period'][1:]}-01",
                'series_id': series_id,
                'series_name': series_name,
                'value': float(item['value']),
                'year': int(item['year']),
                'period': item['period'],
                'period_name': item['periodName']
            })
    
    return all_data

def collect_all_series(series_dict, start_year, end_year):
    """Collect data for all series one at a time"""
    all_data = []
    total_series = len(series_dict)
    
    print(f"Collecting data for {total_series} series (one at a time)...\n")
    
    for idx, (series_name, series_id) in enumerate(series_dict.items(), 1):
        print(f"[{idx}/{total_series}] Fetching: {series_name}...")
        
        json_data = fetch_bls_data_single(series_id, start_year, end_year)
        
        if json_data:
            records = parse_bls_data(json_data, series_id, series_name)
            all_data.extend(records)
            print(f"  ✓ Got {len(records)} records")
        else:
            print(f"  ✗ Failed to fetch {series_name}")
        
        # Wait 1 second between requests to be nice to the API
        if idx < total_series:
            time.sleep(1)
    
    return all_data

def save_data(df, filepath):
    """Save DataFrame to CSV"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    df.to_csv(filepath, index=False)
    print(f"\n{'='*60}")
    print(f"Data saved to: {filepath}")
    print(f"Total records: {len(df)}")
    print(f"Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"{'='*60}")

def main():
    """Main function to collect and save BLS data"""
    current_year = datetime.now().year
    start_year = current_year - 1
    
    print("="*60)
    print("BLS Labor Statistics Data Collection")
    print("="*60)
    print(f"Collecting data from {start_year} to {current_year}")
    print(f"Using BLS API v1 (no registration key)")
    print("="*60 + "\n")
    
    all_records = collect_all_series(SERIES_IDS, start_year, current_year)
    
    if not all_records:
        print("\n❌ No data collected. Exiting.")
        return
    
    df = pd.DataFrame(all_records)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    
    print("\n" + "="*60)
    print("Data Preview:")
    print("="*60)
    print(df.head(10))
    
    print("\n" + "="*60)
    print("Series Summary:")
    print("="*60)
    summary = df.groupby('series_name').agg({
        'date': ['min', 'max', 'count']
    })
    print(summary)
    
    output_path = 'data/processed/labor_stats.csv'
    save_data(df, output_path)
    
    print("\n✅ Data collection completed successfully!")

if __name__ == "__main__":
    main()