from datetime import timezone, timedelta

VOCAB_INTERVALS = {1, 2, 4, 15, 30} # long-term memory
ARTICLE_INTERVALS = {1, 2, 4} # short-term memory

REVIEW_INTERVALS = VOCAB_INTERVALS # ensure no bugs

NOTES_DIR = "notes"
OUTPUT_FILE = "dist/index.html"  # Output all files to the dist folder for easy deployment
TW_TIMEZONE = timezone(timedelta(hours=8))