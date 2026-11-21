from datetime import timezone, timedelta

REVIEW_INTERVALS = {1, 2, 4, 7, 14, 30, 60, 120, 240}
NOTES_DIR = "notes"
OUTPUT_FILE = "dist/index.html"  # Output all files to the dist folder for easy deployment
TW_TIMEZONE = timezone(timedelta(hours=8))