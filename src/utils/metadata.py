import os
import requests
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
from src.utils.sanitation import sanitize_filename

class MetadataApplier:
    def __init__(self, folder_name: str, track: dict):
        self.folder_name = folder_name
        self.track = track
        self.title = sanitize_filename(track['name'])
        
        # Safe extraction of artist
        artists = track.get('artists', [])
        self.artist = sanitize_filename(artists[0]['name']) if artists else "Unknown Artist"
        
        # Safe extraction of album data
        album_data = track.get('album', {})
        self.album = sanitize_filename(album_data.get('name', 'Unknown Album'))
        
        genres = album_data.get('genres', [])
        self.genre = sanitize_filename(genres[0]) if genres else 'Unknown Genre'
        
        self.cover_url = None
        self.cover_path = None
        self.mp3_file = os.path.join(self.folder_name, f"{self.title}.mp3")

    def apply_metadata(self):
        """Applies ID3 tags to the MP3 file."""
        if not os.path.exists(self.mp3_file):
            print(f"Error: File not found {self.mp3_file}")
            return

        try:
            audio = EasyID3(self.mp3_file)
        except Exception:
            try:
                # If EasyID3 fails (no tags), create them
                audio = MP3(self.mp3_file, ID3=ID3)
                audio.add_tags()
                audio = EasyID3(self.mp3_file)
            except Exception as e:
                print(f"Error initializing tags for {self.mp3_file}: {e}")
                return

        audio["title"] = self.track['name']
        audio["artist"] = self.artist
        audio["album"] = self.album
        audio["genre"] = self.genre
        audio.save()

    def _get_cover_url(self):
        """Extracts cover URL from track data."""
        album_data = self.track.get('album', {})
        images = album_data.get('images', [])
        if images:
            self.cover_url = images[0]['url']

    def _download_cover(self):
        """Downloads the cover image."""
        if not self.cover_url:
            print("No cover URL available.")
            return

        self.cover_path = os.path.join(self.folder_name, f"{self.title} - {self.artist}.jpg")
        
        try:
            response = requests.get(self.cover_url, stream=True, timeout=10)
            response.raise_for_status()
            with open(self.cover_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
        except Exception as e:
            print(f"Error downloading cover image: {e}")
            self.cover_path = None

    def apply_cover(self):
        """Embeds the cover image into the MP3."""
        if self.cover_path and os.path.exists(self.cover_path):
            try:
                audio = MP3(self.mp3_file, ID3=ID3)
                with open(self.cover_path, "rb") as img:
                    audio.tags.add(
                        APIC(
                            encoding=3,
                            mime="image/jpeg",
                            type=3,
                            desc="Cover",
                            data=img.read(),
                        )
                    )
                audio.save()
                print("Cover art updated successfully.") # In Spanish: Carátula actualizada correctamente
            except Exception as e:
                 print(f"Error embedding cover art: {e}")
        else:
            print("Metadata updated (no cover art).")

    def run(self):
        self.apply_metadata()
        self._get_cover_url()
        self._download_cover()
        self.apply_cover()
        # Clean up the jpg file after embedding if desired? leaving it for now as per original logic.
