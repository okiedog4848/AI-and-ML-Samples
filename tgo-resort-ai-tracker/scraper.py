"""
TGO Resort AI Properties Tracker - Phase 1 (Groq as default - Free Tier)
"""

import json
from pathlib import Path
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

from langchain_core.prompts import PromptTemplate

# ================== LLM Setup - Groq (Free & Fast) ==================
from langchain_groq import ChatGroq

llm = ChatGroq(
    model="llama-3.3-70b-versatile",   # Excellent for structured parsing
    temperature=0,
    groq_api_key=os.getenv("GROQ_API_KEY")
)

# Alternative: OpenAI (commented out)
# from langchain_openai import ChatOpenAI
# llm = ChatOpenAI(
#     model="gpt-4o-mini",
#     temperature=0,
#     openai_api_key=os.getenv("OPENAI_API_KEY")
# )

# ===============================================

DATA_FILE = Path("data/current_listings.txt")
PROMPTS_DIR = Path("prompts")
DB_FILE = Path("data/listings_history.db")

def load_raw_listings():
    if not DATA_FILE.exists():
        print(f"❌ Error: {DATA_FILE} not found.")
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def parse_with_llm(raw_text: str):
    prompt_path = PROMPTS_DIR / "parse_listing_prompt.txt"
    if not prompt_path.exists():
        print(f"❌ Prompt file not found: {prompt_path}")
        return {"address": raw_text, "price": None}

    with open(prompt_path, "r", encoding="utf-8") as f:
        template = f.read()

    prompt = PromptTemplate.from_template(template)
    chain = prompt | llm

    try:
        response = chain.invoke({"listing_text": raw_text})
        cleaned = response.content.strip()

        if cleaned.startswith("{") and "}" in cleaned:
            json_str = cleaned[cleaned.find("{"):cleaned.rfind("}") + 1]
            return json.loads(json_str)
        else:
            # Simple fallback
            parts = raw_text.rsplit(", $", 1)
            address = parts[0].strip()
            price_str = parts[1].replace(",", "") if len(parts) > 1 else None
            price = int(price_str) if price_str and price_str.isdigit() else None
            return {"address": address, "price": price}
    except Exception as e:
        print(f"⚠️ Parsing error: {e}")
        return {"address": raw_text, "price": None}

def save_snapshot(parsed_listings):
    DB_FILE.parent.mkdir(exist_ok=True)
    import sqlite3
    conn = sqlite3.connect(DB_FILE)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS listings (
            snapshot_date TEXT,
            address TEXT,
            price INTEGER,
            raw_text TEXT,
            PRIMARY KEY (snapshot_date, address)
        )
    """)

    today = datetime.now().strftime("%Y-%m-%d")
    count = 0
    for item in parsed_listings:
        conn.execute("""
            INSERT OR REPLACE INTO listings 
            (snapshot_date, address, price, raw_text)
            VALUES (?, ?, ?, ?)
        """, (today, item.get("address"), item.get("price"), item.get("raw_text", "")))
        count += 1

    conn.commit()
    conn.close()
    print(f"✅ Saved {count} listings to database for {today}")

if __name__ == "__main__":
    print("🚀 Starting TGO Resort AI Tracker - Phase 1 (using Groq)\n")

    raw_listings = load_raw_listings()
    print(f"Loaded {len(raw_listings)} raw listings.\n")

    print("Parsing listings with Groq...")
    parsed_listings = []
    for i, raw in enumerate(raw_listings):
        print(f"  [{i+1:2d}/{len(raw_listings)}] {raw[:70]}...")
        parsed = parse_with_llm(raw)
        parsed["raw_text"] = raw
        parsed_listings.append(parsed)

    save_snapshot(parsed_listings)

    print("\n✅ Phase 1 Complete using Groq!")
    print("   • All listings parsed")
    print("   • Data saved to SQLite")
    print("\nNext: Change detection + Streamlit dashboard")

