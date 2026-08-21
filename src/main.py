import os
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def fetch_or_generate_data(file_path="data/market_data.csv"):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    today = datetime.date.today().strftime("%Y-%m-%d")
    
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
    else:
        df = pd.DataFrame(columns=["date", "price"])
    
    if today not in df["date"].values:
        last_price = df["price"].iloc[-1] if not df.empty else 100.0
        new_price = round(last_price + float(np.random.normal(0.5, 2.0)), 2)
        new_row = pd.DataFrame([{"date": today, "price": max(10.0, new_price)}])
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(file_path, index=False)
        
    return df

def generate_chart(df, output_path="assets/market_trend.png"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    plt.figure(figsize=(10, 4))
    plt.plot(df['date'], df['price'], marker='o', color='#2b5c8f', linewidth=2)
    plt.title('Daily Market Trend Overview', fontsize=12, fontweight='bold')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    
    plt.savefig(output_path, dpi=150)
    plt.close()

if __name__ == "__main__":
    df = fetch_or_generate_data()
    generate_chart(df)
    print("Market data updated and chart generated successfully!")
