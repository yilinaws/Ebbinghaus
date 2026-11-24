import os
import re
from src.config import OUTPUT_FILE


def format_item_content(category, content):
  """根據不同分類，把內容排版成最適合閱讀的 HTML"""
  # 1. 英文單字：自動把 @ 前面的單字加粗放大，後面的解釋排在旁邊
  if category == "English_Vocabulary" and "@" in content:
    word, meaning = content.split("@", 1)
    return f'<div class="vocab"><strong class="word">{word.strip()}</strong> <span class="meaning">{meaning.strip()}</span></div>'

  # 2. 英文文章或影片：精準抓出網址變成可點擊超連結，若有備註也會一併顯示
  if category in ("English_Article", "English_Video"):
    match = re.search(r"(https?://[^\s]+)", content)
    if match:
      url = match.group(1)
      note = content.replace(url, "").strip()
      note_html = f'<div class="note">📝 {note}</div>' if note else ""
      return f'{note_html}<a href="{url}" target="_blank" rel="noopener noreferrer">{url}</a>'

  # 3. 英文句子（或其他純文字）：直接顯示段落文字
  return f'<div class="sentence">{content}</div>'


def render_html(today_str, review_items):
  os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

  if not review_items:
    list_html = "<p class='empty'>🎉 Awesome! Nothing to review today.</p>"
  else:
    # 左邊維持中文（用來對應 parser.py 的分類），右邊改成你要顯示的英文標題
    sections = [
        ("English_Vocabulary", "🔤 English Vocabulary"),
        ("English_Sentences", "💬 English Sentences"),
        ("English_Articles", "📰 English Articles"),
        ("English_Videos", "🎬 English Videos"),
    ]
    sections_html = []

    for cat_key, cat_title in sections:
      cat_items = [
          item
          for item in review_items
          if item.get("category", "English_Sentences") == cat_key
      ]

      if not cat_items:
        continue

      cards = []
      for item in cat_items:
        content = item.get("content", item.get("url", ""))
        body_html = format_item_content(cat_key, content)
        cards.append(f"""
                <div class="card">
                    <div class="meta">From <strong>{item['source_date']}</strong> (Day {item['interval']} review)</div>
                    {body_html}
                </div>
                """)

      sections_html.append(f"""
            <section class="category-section">
                <h2>{cat_title} <span class="count">{len(cat_items)}</span></h2>
                {"".join(cards)}
            </section>
            """)

    list_html = "\n".join(sections_html)

  html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ebbinghaus Daily Review</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; max-width: 650px; margin: 40px auto; padding: 0 20px; background: #f4f6f8; color: #333; }}
        h1 {{ color: #1a202c; font-size: 1.6rem; border-bottom: 2px solid #e2e8f0; padding-bottom: 10px; }}
        h2 {{ color: #2d3748; font-size: 1.25rem; margin-top: 28px; margin-bottom: 12px; display: flex; align-items: center; gap: 8px; }}
        .count {{ background: #e2e8f0; color: #4a5568; font-size: 0.85rem; padding: 2px 8px; border-radius: 12px; }}
        .date-badge {{ background: #3182ce; color: white; padding: 4px 10px; border-radius: 6px; font-size: 0.9rem; }}
        .card {{ background: white; padding: 16px; margin-bottom: 12px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); word-break: break-word; }}
        .meta {{ font-size: 0.85rem; color: #718096; margin-bottom: 8px; }}
        .vocab .word {{ font-size: 1.2rem; color: #1a202c; }}
        .vocab .meaning {{ font-size: 1.05rem; color: #4a5568; margin-left: 8px; }}
        .sentence {{ font-size: 1.1rem; color: #2d3748; line-height: 1.5; }}
        .note {{ font-size: 1rem; color: #2d3748; font-weight: 500; margin-bottom: 4px; }}
        a {{ color: #2b6cb0; text-decoration: none; font-size: 0.95rem; word-break: break-all; }}
        a:hover {{ text-decoration: underline; }}
        .empty {{ background: white; padding: 24px; border-radius: 8px; text-align: center; color: #4a5568; }}
    </style>
</head>
<body>
    <h1>📅 Daily Review <span class="date-badge">{today_str}</span></h1>
    {list_html}
</body>
</html>"""

  with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(html_content)