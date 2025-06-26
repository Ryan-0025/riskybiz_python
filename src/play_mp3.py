import pygame
import time
import sys
from pathlib import Path
from config import AUDIO_DIR

def initialize_audio():
    """Initialize the mixer for playback."""
    pygame.mixer.init()

def get_available_months(year: str = "2025") -> list[str]:
    """Return sorted list of folders like '2025-06' inside audio directory."""
    if not AUDIO_DIR.exists():
        print(f"[ERROR] Audio directory '{AUDIO_DIR}' not found.")
        sys.exit(1)

    return sorted([
        folder.name for folder in AUDIO_DIR.iterdir()
        if folder.is_dir() and folder.name.startswith(year) and len(folder.name) == 7
    ])

def prompt_user_for_month(months: list[str]) -> str:
    """Let user pick a month folder."""
    print("Available months:")
    for i, month in enumerate(months, 1):
        print(f"{i}. {month}")

    while True:
        try:
            choice = int(input("Select a month number to play: "))
            if 1 <= choice <= len(months):
                return months[choice - 1]
            print("Invalid number. Try again.")
        except ValueError:
            print("Please enter a valid number.")

def get_mp3_files(folder: Path) -> list[str]:
    """Return sorted list of MP3 file names in the folder."""
    return sorted([f.name for f in folder.glob('*.mp3')])

def play_audio(file_path: Path):
    """Load and play a given MP3 file."""
    pygame.mixer.music.load(str(file_path))
    pygame.mixer.music.play()

def pause_audio():
    pygame.mixer.music.pause()

def resume_audio():
    pygame.mixer.music.unpause()

def stop_audio():
    pygame.mixer.music.stop()

def main():
    initialize_audio()

    months = get_available_months()
    if not months:
        print("No audio folders found.")
        sys.exit(1)

    selected_month = prompt_user_for_month(months)
    folder_path = AUDIO_DIR / selected_month

    mp3_files = get_mp3_files(folder_path)
    if not mp3_files:
        print(f"No MP3 files found in {folder_path}")
        sys.exit(1)

    current_index = 0
    play_audio(folder_path / mp3_files[current_index])
    print(f"Now playing: {mp3_files[current_index]} from {selected_month}")
    print("Controls: [p] Pause | [r] Resume | [s] Skip | [q] Quit")

    while True:
        cmd = input("Enter command: ").strip().lower()

        if cmd == 'p':
            pause_audio()
        elif cmd == 'r':
            resume_audio()
        elif cmd == 's':
            stop_audio()
            time.sleep(0.5)
            current_index = (current_index + 1) % len(mp3_files)
            play_audio(folder_path / mp3_files[current_index])
            print(f"🎵 Now playing: {mp3_files[current_index]}")
        elif cmd == 'q':
            print("Goodbye!")
            stop_audio()
            break
        else:
            print("Invalid command. Use [p], [r], [s], or [q].")

if __name__ == "__main__":
    main()
