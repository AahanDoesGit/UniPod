# UniRpiDeck (UNI//POD)

A minimalistic music player interface for the DFRobot UniHiker and Raspberry Pi, inspired by classic click-wheel designs.

## Features
- **Click Wheel Interface**: Virtual click wheel for navigation.
- **Music Library**: Scans local directory for MP3 files.
- **Audio Management**: Auto-detects USB audio hardware on Linux.
- **Smooth Transitions**: Cross-fade effects between screens.

## Requirements
- Python 3.x
- `pygame`
- `mutagen` (optional, for metadata)

## Installation
```bash
pip install pygame mutagen
```

## Running
Navigate to the project directory and run:
```bash
python3 main.py
```

## Hardware Compatibility
Optimized for 240x320 touchscreens (like UniHiker).
