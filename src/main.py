import os
from datetime import datetime, timezone
import requests
import pandas as pd

API_URL = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd&include_24hr_change=true&include_24hr_vol=true&include_market_cap=true"

def fetch_market_data():
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(API_URL, headers=headers, timeout=15)
    response.raise_for_status()
    return response.json()

def process_data(raw_data):
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    records = []
    
    for asset, metrics in raw_data.items():
        records.append({
            "timestamp": timestamp,
            "asset": asset,
            "price_usd": metrics.get("usd"),
            "market_cap_usd": metrics.get("usd_market_cap"),
            "vol_24h_usd": metrics.get("usd_24h_vol"),
            "change_24h_pct": metrics.get("usd_24h_change")
        })
    
    df_new = pd.DataFrame(records)
    data_file = "data/raw_history.csv"
    
    os.makedirs("data", exist_ok=True)
    if os.path.exists(data_file):
        df_existing = pd.read_csv(data_file)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_combined = df_new
        
    df_combined.to_csv(data_file, index=False)
    generate_markdown_report(df_combined)

def generate_markdown_report(df):
    os.makedirs("reports", exist_ok=True)
    latest_time = df['timestamp'].max()
    latest_df = df[df['timestamp'] == latest_time]
    
    md_content = f"# Automated Market Intelligence Report\n\n"
    md_content += f"**Last Updated (UTC):** `{latest_time}`\n\n"
    md_content += "## Current Snapshot\n\n"
    md_content += "| Asset | Price (USD) | 24h Change (%) | Market Cap (USD) |\n"
    md_content += "|---|---|---|---|\n"
    
    for _, row in latest_df.iterrows():
        md_content += f"| **{row['asset'].upper()}** | ${row['price_usd']:,.2f} | {row['change_24h_pct']:.2f}% | ${row['market_cap_usd']:,.0f} |\n"
    
    with open("reports/summary.md", "w") as f:
        f.write(md_content)

if __name__ == "__main__":
    data = fetch_market_data()
    process_data(data)
