import os
import re
from datetime import datetime, timedelta
from src.config import REVIEW_INTERVALS, NOTES_DIR, TW_TIMEZONE

def get_taiwan_today():
    return datetime.now(TW_TIMEZONE).date()

def extract_urls(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r", encoding="utf-8") as f:
        return re.findall(r'https?://[^\s\)\]\>\"\']+', f.read())

def get_today_reviews():
    today = get_taiwan_today()
    review_items = []
    
    for days_ago in REVIEW_INTERVALS:
        target_date = today - timedelta(days=days_ago)
        date_str = target_date.strftime("%Y-%m-%d")
        filepath = os.path.join(NOTES_DIR, f"{date_str}.txt")
        
        for url in extract_urls(filepath):
            review_items.append({
                "source_date": date_str,
                "interval": days_ago,
                "url": url
            })
    return today.strftime("%Y-%m-%d"), review_items