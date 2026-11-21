import os
from src.config import OUTPUT_FILE

def render_html(today_str, review_items):
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    if not review_items:
        list_html = "<p class='empty'>🎉 太棒了！今天沒有需要複習的影片。</p>"
    else:
        items_html = [
            f"""
            <div class="card">
                <div class="meta">來自 <strong>{item['source_date']}</strong> 的筆記（第 {item['interval']} 天複習）</div>
                <a href="{item['url']}" target="_blank" rel="noopener noreferrer">{item['url']}</a>
            </div>
            """
            for item in review_items
        ]
        list_html = "\n".join(items_html)

    html_content = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>艾賓浩斯每日複習清單</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; max-width: 650px; margin: 40px auto; padding: 0 20px; background: #f4f6f8; color: #333; }}
        h1 {{ color: #1a202c; font-size: 1.6rem; border-bottom: 2px solid #e2e8f0; padding-bottom: 10px; }}
        .date-badge {{ background: #3182ce; color: white; padding: 4px 10px; border-radius: 6px; font-size: 0.9rem; }}
        .card {{ background: white; padding: 16px; margin-bottom: 12px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); word-break: break-all; }}
        .meta {{ font-size: 0.85rem; color: #718096; margin-bottom: 6px; }}
        a {{ color: #2b6cb0; text-decoration: none; font-weight: 500; font-size: 1.05rem; }}
        a:hover {{ text-decoration: underline; }}
        .empty {{ background: white; padding: 24px; border-radius: 8px; text-align: center; color: #4a5568; }}
    </style>
</head>
<body>
    <h1>📅 今日複習清單 <span class="date-badge">{today_str}</span></h1>
    {list_html}
</body>
</html>"""

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html_content)