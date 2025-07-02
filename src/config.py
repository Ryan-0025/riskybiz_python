from pathlib import Path

# Shared audio directory
AUDIO_DIR = Path('./audio_files')
# Downloaded Files Log Filename
DOWNLOAD_LOG_FILENAME = 'downloaded_files.txt'
DOWNLOAD_LOG = AUDIO_DIR / DOWNLOAD_LOG_FILENAME
# General log file for tracking scipt actions and errors
LOG_FILE = AUDIO_DIR / 'scraper.log'
# Webpage URL containing MP3 files
SOURCE_URL = "https://risky.biz/risky-business-news/"
