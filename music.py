"""
UNI//POD — Music Library
"""

import os
from typing import List, Dict, Optional


def get_duration(filepath: str) -> float:
    """Get track duration in seconds."""
    try:
        from mutagen.mp3 import MP3
        audio = MP3(filepath)
        return audio.info.length
    except Exception:
        try:
            size = os.path.getsize(filepath)
            return size / 16000.0
        except:
            return 0.0


class Track:
    def __init__(self, title: str, artist: str, filepath: str, duration: float):
        self.title = title
        self.artist = artist
        self.filepath = filepath
        self.duration = duration
        self.dur_str = f"{int(duration)//60}:{int(duration)%60:02d}"

    def __repr__(self):
        return f"Track({self.title} - {self.artist})"


class MusicLibrary:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init()
        return cls._instance

    def _init(self):
        self.tracks: List[Track] = []
        self.playlists: Dict[str, List[int]] = {}
        self._loaded = False

    def load_from_directory(self, music_dir: str = "/root/music"):
        """Scan directory and load all .mp3 files."""
        if not os.path.exists(music_dir):
            print(f"Music directory not found: {music_dir}")
            return False
        
        if not os.access(music_dir, os.R_OK):
            print(f"No read permission for: {music_dir}")
            return False

        self.tracks.clear()
        
        # Scan for .mp3 files
        for filename in sorted(os.listdir(music_dir)):
            if not filename.endswith('.mp3'):
                continue
            
            filepath = os.path.join(music_dir, filename)
            
            # Extract title from filename (remove _spotdown.org.mp3 suffix)
            title = filename.replace('_spotdown.org.mp3', '').replace('.mp3', '')
            
            # Try to extract artist from metadata or use "Unknown"
            artist = "Unknown Artist"
            try:
                from mutagen.mp3 import MP3
                audio = MP3(filepath)
                if 'TPE1' in audio:
                    artist = str(audio['TPE1'])
            except:
                pass
            
            duration = get_duration(filepath)
            track = Track(title, artist, filepath, duration)
            self.tracks.append(track)

        self._loaded = True
        self._build_playlists()
        print(f"Loaded {len(self.tracks)} tracks from {music_dir}")
        return True

    def _build_playlists(self):
        """Build automatic playlists based on artists."""
        if not self.tracks:
            return

        # All tracks playlist
        self.playlists["ALL"] = list(range(len(self.tracks)))

        # Artist-based playlists
        artists = {}
        for i, track in enumerate(self.tracks):
            if track.artist not in artists:
                artists[track.artist] = []
            artists[track.artist].append(i)

        # Only create playlists for artists with 2+ tracks
        for artist, indices in artists.items():
            if len(indices) >= 2:
                self.playlists[artist.upper()[:10]] = indices

    def get_track(self, index: int) -> Optional[Track]:
        """Get track by index."""
        if 0 <= index < len(self.tracks):
            return self.tracks[index]
        return None

    def get_playlist_tracks(self, playlist_name: str) -> List[Track]:
        """Get all tracks in a playlist."""
        if playlist_name not in self.playlists:
            return []
        indices = self.playlists[playlist_name]
        return [self.tracks[i] for i in indices if i < len(self.tracks)]

    def search(self, query: str) -> List[int]:
        """Search tracks by title or artist."""
        query = query.lower()
        results = []
        for i, track in enumerate(self.tracks):
            if query in track.title.lower() or query in track.artist.lower():
                results.append(i)
        return results
