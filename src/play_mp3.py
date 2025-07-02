import pygame
import time
import sys
from pathlib import Path
from config import AUDIO_DIR

def initialize_audio():
    """Initialize the mixer for playback."""
    pygame.mixer.init()

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

    if not AUDIO_DIR.exists():
        print(f"[ERROR] Audio directory '{AUDIO_DIR}' not found.")
        sys.exit(1)

    mp3_files = get_mp3_files(AUDIO_DIR)
    if not mp3_files:
        print(f"No MP3 files found in {AUDIO_DIR}")
        sys.exit(1)

    current_index = 0
    play_audio(AUDIO_DIR / mp3_files[current_index])
    print(f"Now playing: {mp3_files[current_index]}")
    print("Controls: [p] Pause | [r] Resume | [s] Skip | [q] Quit")

    while True:
        if not pygame.mixer.music.get_busy():
            # Automatically go to next track when current one ends
            current_index = (current_index + 1) % len(mp3_files)
            play_audio(AUDIO_DIR / mp3_files[current_index])
            print(f"🎵 Auto-playing: {mp3_files[current_index]}")

        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            cmd = input("Enter command: ").strip().lower()

            if cmd == 'p':
                pause_audio()
            elif cmd == 'r':
                resume_audio()
            elif cmd == 's':
                stop_audio()
                time.sleep(0.5)
                current_index = (current_index + 1) % len(mp3_files)
                play_audio(AUDIO_DIR / mp3_files[current_index])
                print(f"🎵 Skipped to: {mp3_files[current_index]}")
            elif cmd == 'q':
                print("Goodbye!")
                stop_audio()
                break
            else:
                print("Invalid command. Use [p], [r], [s], or [q].")

        time.sleep(0.5)  # Slight delay to reduce CPU usage

if __name__ == "__main__":
    import select  # Needed for non-blocking input detection
    main()

