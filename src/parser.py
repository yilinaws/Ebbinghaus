import os
import re
from datetime import datetime, timedelta # time difference calculator
from src.config import ARTICLE_INTERVALS, NOTES_DIR, TW_TIMEZONE, VOCAB_INTERVALS

def get_taiwan_today():
    return datetime.now(TW_TIMEZONE).date()

def classify_line(line):
  """Classify a single-line note and determine its review cycle."""
  text = line.strip()
  if not text:
    return None, None  # Skip blank lines

  video_domains = ("youtube.com", "youtu.be", "vimeo.com", "bilibili.com")

  # 1. Check for URLs (video or article)
  if "http://" in text or "https://" in text:
    if any(domain in text.lower() for domain in video_domains):
      return "English_Video", ARTICLE_INTERVALS
    else:
      return "English Article", ARTICLE_INTERVALS

  # 2. Treat any line containing '@' as an English word
  if "@" in text:
    return "English Vocabulary", VOCAB_INTERVALS

  # 3. Classify remaining plain text (without URLs or '@') as English sentences
  return "English Sentence", VOCAB_INTERVALS

def get_today_reviews():
    today = get_taiwan_today()
    review_items = []
    all_intervals = sorted(VOCAB_INTERVALS | ARTICLE_INTERVALS)
    
    for days_ago in all_intervals:
        target_date = today - timedelta(days=days_ago)
        date_str = target_date.strftime("%Y-%m-%d")
        filepath = os.path.join(NOTES_DIR, f"{date_str}.txt")

        if not os.path.exists(filepath):
            continue  # Skip this day if the file doesn't exist

        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                category, target_intervals = classify_line(line)

                # Append to the list only if the line is valid and the day difference matches the category's review cycle
                if category and (days_ago in target_intervals):
                    clean_text = line.strip()
                    review_items.append({
                        "source_date": date_str,
                        "interval": days_ago,
                        "category": category,  # 新增：標記是單字、句子、文章還是影片
                        "content": clean_text,  # 新增：完整的文字或網址內容
                        "url": clean_text,  # 保留原本的 "url" 欄位名稱，確保你負責產生網頁的程式不會馬上報錯
                    })

    return today.strftime("%Y-%m-%d"), review_items