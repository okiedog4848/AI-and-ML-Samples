"""
TGO Resort AI Tracker - Change Detection (New / Removed / Price Changed)
"""

from pathlib import Path
import sqlite3
from datetime import datetime
import pandas as pd

DB_FILE = Path("data/listings_history.db")


def get_latest_snapshots():
    conn = sqlite3.connect(DB_FILE)

    # Get the two most recent snapshot dates
    dates = pd.read_sql("""
                        SELECT DISTINCT snapshot_date
                        FROM listings
                        ORDER BY snapshot_date DESC LIMIT 2
                        """, conn)

    conn.close()

    if len(dates) < 2:
        print("Not enough snapshots yet for comparison.")
        return None, None

    current_date = dates.iloc[0]['snapshot_date']
    previous_date = dates.iloc[1]['snapshot_date']

    return current_date, previous_date


def get_listings_by_date(snapshot_date):
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql("""
                     SELECT address, price, raw_text
                     FROM listings
                     WHERE snapshot_date = ?
                     """, conn, params=(snapshot_date,))
    conn.close()
    return df


def detect_changes():
    current_date, previous_date = get_latest_snapshots()
    if not current_date or not previous_date:
        return

    current_df = get_listings_by_date(current_date)
    previous_df = get_listings_by_date(previous_date)

    # Create sets for easy comparison
    current_addresses = set(current_df['address'])
    previous_addresses = set(previous_df['address'])

    # New listings
    new_listings = current_df[~current_df['address'].isin(previous_addresses)]

    # Removed listings
    removed_listings = previous_df[~previous_df['address'].isin(current_addresses)]

    # Price changes
    common = current_df[current_df['address'].isin(previous_addresses)]
    price_changes = []
    for _, row in common.iterrows():
        prev_price = previous_df[previous_df['address'] == row['address']]['price'].iloc[0]
        if row['price'] != prev_price and pd.notna(row['price']) and pd.notna(prev_price):
            price_changes.append({
                "address": row['address'],
                "old_price": prev_price,
                "new_price": row['price'],
                "change": row['price'] - prev_price
            })

    print(f"\n📊 Change Detection Report - {current_date} vs {previous_date}")
    print("=" * 60)
    print(f"New Listings: {len(new_listings)}")
    print(f"Removed Listings: {len(removed_listings)}")
    print(f"Price Changes: {len(price_changes)}")

    if not new_listings.empty:
        print("\n🆕 NEW LISTINGS:")
        print(new_listings[['address', 'price']].to_string(index=False))

    if not removed_listings.empty:
        print("\n❌ REMOVED LISTINGS:")
        print(removed_listings[['address', 'price']].to_string(index=False))

    if price_changes:
        print("\n💰 PRICE CHANGES:")
        for change in price_changes:
            direction = "↑" if change['change'] > 0 else "↓"
            print(f"{change['address']}: ${change['old_price']:,} → ${change['new_price']:,} {direction}")


if __name__ == "__main__":
    detect_changes()