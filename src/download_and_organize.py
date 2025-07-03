import threading
import time
import os
import serial
from pathlib import Path
import requests
import logging
import subprocess
from bs4 import BeautifulSoup
import pygame
from config import AUDIO_DIR, DOWNLOAD_LOG, SOURCE_URL, LOG_FILE

# Initialize pygame mixer once globally
pygame.mixer.init()

# Ensure audio dir exists
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

# Configure logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logging.info("=== Script started ===")

def ensure_directory_exists(path: Path):
    path.mkdir(parents=True, exist_ok=True)

def is_downloaded(filename: str) -> bool:
    if not DOWNLOAD_LOG.exists():
        return False
    return filename in DOWNLOAD_LOG.read_text().splitlines()

def mark_as_downloaded(filename: str):
    with DOWNLOAD_LOG.open('a') as f:
        f.write(f"{filename}\n")

def get_mp3_links() -> list[str]:
    try:
        response = requests.get(SOURCE_URL)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Failed to fetch webpage: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    return [tag['src'] for tag in soup.find_all('source', {'type': 'audio/mpeg'})]

def download_file(mp3_url: str, target_dir: Path, filename: str):
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

def play_file(filepath: Path):
    try:
        logging.info(f"Playing: {filepath}")
        pygame.mixer.music.load(str(filepath))
        pygame.mixer.music.play()

        # Wait until playback finishes before returning
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

    except Exception as e:
        logging.error(f"Playback error for {filepath}: {e}")

def mp3_downloader():
    logging.info("=== MP3 Downloader Thread Started ===")
    ensure_directory_exists(AUDIO_DIR)
    logging.info(f"Target audio directory: {AUDIO_DIR}")
    logging.info(f"Download log path: {DOWNLOAD_LOG}")

    mp3_links = get_mp3_links()
    if not mp3_links:
        logging.warning("No MP3 links found. Exiting MP3 thread.")
        return

    for mp3_url in mp3_links:
        filename = mp3_url.split("/")[-1]
        download_file(mp3_url, AUDIO_DIR, filename)
        play_file(AUDIO_DIR / filename)

    logging.info("=== MP3 Downloader Thread Finished ===")

PORT = "/dev/ttyUSB0"
BAUD = 115200

def serial_listener():
    try:
        with serial.Serial(PORT, BAUD, timeout=0.1) as ser:
            logging.info(f"Connected to {PORT} at {BAUD} baud.")
            logging.info("Listening for button presses...")

            while True:
                if ser.in_waiting > 0:
                    # Read all available bytes, decode, strip whitespace
                    data = ser.read(ser.in_waiting).decode(errors='ignore').strip()

                    if data:
                        logging.info(f"Received serial data: {data}")
                        os.system("amixer sset Master toggle")
                        logging.info("Master volume toggled via serial input.")

                time.sleep(0.05)  # slight pause to prevent CPU hogging

    except serial.SerialException as e:
        logging.error(f"Serial error: {e}")

def main():
    t1 = threading.Thread(target=mp3_downloader, daemon=True)
    t2 = threading.Thread(target=serial_listener, daemon=True)

    t1.start()
    t2.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting...")

if __name__ == "__main__":
    main()

