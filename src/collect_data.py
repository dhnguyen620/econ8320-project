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

def load_existing_data(filepath):
    """Load existing data if file exists"""
    if os.path.exists(filepath):
        print(f"Loading existing data from {filepath}...")
        df = pd.read_csv(filepath)
        df['date'] = pd.to_datetime(df['date'])
        print(f"Loaded {len(df)} existing records")
        return df
    else:
        print("No existing data file found. Will create new file.")
        return pd.DataFrame()

def get_latest_date(df):
    """Get the latest date in existing data"""
    if df.empty:
        return None
    return df['date'].max()

def append_new_data(existing_df, new_df):
    """Append only new records to existing data"""
    if existing_df.empty:
        return new_df
    
    # Get latest date in existing data
    latest_date = get_latest_date(existing_df)
    print(f"Latest date in existing data: {latest_date}")
    
    # Filter new data to only include records after latest date
    new_records = new_df[new_df['date'] > latest_date]
    
    if len(new_records) == 0:
        print("No new data to append.")
        return existing_df
    
    print(f"Found {len(new_records)} new records to append")
    
    # Combine old and new data
    combined_df = pd.concat([existing_df, new_records], ignore_index=True)
    combined_df = combined_df.sort_values('date')
    
    # Remove duplicates (just in case)
    combined_df = combined_df.drop_duplicates(subset=['date', 'series_id'], keep='last')
    
    return combined_df

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
    output_path = 'data/processed/labor_stats.csv'
    
    print("="*60)
    print("BLS Labor Statistics Data Collection")
    print("="*60)
    
    # Load existing data
    existing_df = load_existing_data(output_path)
    
    # Determine date range to fetch
    current_year = datetime.now().year
    
    if existing_df.empty:
        # First run - get last year of data
        start_year = 2020
        print(f"First run: Collecting data from {start_year} to {current_year}")
    else:
        # Subsequent runs - only get current year
        latest_date = get_latest_date(existing_df)
        start_year = latest_date.year if latest_date else current_year - 1
        print(f"Update run: Collecting data from {start_year} to {current_year}")
    
    print(f"Using BLS API v1 (no registration key)")
    print("="*60 + "\n")
    
    # Collect new data
    all_records = collect_all_series(SERIES_IDS, start_year, current_year)
    
    if not all_records:
        print("\n❌ No data collected. Exiting.")
        return
    
    # Convert to DataFrame
    new_df = pd.DataFrame(all_records)
    new_df['date'] = pd.to_datetime(new_df['date'])
    new_df = new_df.sort_values('date')
    
    # Append to existing data
    final_df = append_new_data(existing_df, new_df)
    
    # Display summary
    print("\n" + "="*60)
    print("Data Summary:")
    print("="*60)
    summary = final_df.groupby('series_name').agg({
        'date': ['min', 'max', 'count']
    })
    print(summary)
    
    # Save data
    save_data(final_df, output_path)
    
    print("\n✅ Data collection completed successfully!")

if __name__ == "__main__":
    main()