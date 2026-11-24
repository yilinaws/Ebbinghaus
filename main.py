from src.parser import get_today_reviews
from src.renderer import render_html

def main():
  today_str, review_items = get_today_reviews()
  render_html(today_str, review_items)
  print(f"[{today_str}] Build complete. Collected {len(review_items)} review items.")


if __name__ == "__main__":
  main()