from pathlib import Path
import requests
import logging
from bs4 import BeautifulSoup
from datetime import datetime
from config import AUDIO_DIR, DOWNLOAD_LOG, SOURCE_URL

def ensure_directory_exists(path: Path):
    """Create directory if it doesn't exist."""
    path.mkdir(parents=True, exist_ok=True)

def is_downloaded(filename: str) -> bool:
    """Check if the file is already listed in the download log."""
    if not DOWNLOAD_LOG.exists():
        return False
    return filename in DOWNLOAD_LOG.read_text().splitlines()

def mark_as_downloaded(filename: str):
    """Add filename to the download log."""
    with DOWNLOAD_LOG.open('a') as f:
        f.write(f"{filename}\n")

def get_mp3_links() -> list[str]:
    """Scrape MP3 file URLs from the source page."""
    try:
        response = requests.get(SOURCE_URL)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Failed to fetch webpage: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    return [tag['src'] for tag in soup.find_all('source', {'type': 'audio/mpeg'})]

def download_file(mp3_url: str, target_dir: Path, filename: str):
    """Download MP3 file to the target folder."""
    file_path = target_dir / filename

    if is_downloaded(filename):
        logging.info(f"Skipped (already logged): {filename}")
        return

    if file_path.exists():
        logging.info(f"Skipped (already exists): {filename}")
        mark_as_downloaded(filename)
        return

    try:
        response = requests.get(mp3_url, stream=True)
        response.raise_for_status()

        with file_path.open('wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)

        logging.info(f"Downloaded: {filename}")
        mark_as_downloaded(filename)

    except requests.RequestException as e:
        logging.error(f"Could not download {filename}: {e}")

def download_new_mp3s():
    """Main function to download new MP3s into one directory."""
    ensure_directory_exists(AUDIO_DIR)

    for mp3_url in get_mp3_links():
        filename = mp3_url.split('/')[-1]
        download_file(mp3_url, AUDIO_DIR, filename)

if __name__ == "__main__":
    download_new_mp3s()

def run_mpc_update(): 
    try:
        logging.info("Running 'mpc update' to refresh playlist")
        result = subprocess.run(['mpc', 'update'], capture_output=True, text=True, check=True)
        loging.info(f"'mpc update' output:\n{result.stdout.strip()}")
    except FileNotFoundError: 
        logging.error("Command 'mpc' not found. Please install MPC or adjust the script.")

    
    #run mpc update after all downloads 
    run_mpc_update()

