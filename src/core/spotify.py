import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from src.config import Config

class SpotifyClient:
    def __init__(self):
        Config.validate()
        self.sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
            client_id=Config.SPOTIFY_CLIENT_ID,
            client_secret=Config.SPOTIFY_CLIENT_SECRET
        ))

    def get_playlist_songs(self, playlist_url: str):
        """Fetch all songs from a Spotify playlist."""
        try:
            # Extract ID more robustly if needed, but keeping original logic for now
            playlist_id = playlist_url.split("/")[-1].split("?")[0]
            print(f"Fetching playlist: {playlist_id}")
            
            playlist = self.sp.playlist(playlist_id)
            
            songs = []
            for item in playlist['tracks']['items']:
                track = item['track']
                if track: # Ensure track is not None
                    songs.append({
                        'name': track['name'],
                        'artist': ", ".join(artist['name'] for artist in track['artists']),
                        'spotify_url': track['external_urls']['spotify'],
                        'album': track['album'], # Store full album object for metadata
                        'original_track': track # Store full track object for metadata
                    })
            return songs, playlist['name']
        except Exception as e:
            print(f"Error fetching playlist: {e}")
            return [], None

    def get_song(self, track_url: str):
        """Fetch song metadata from Spotify."""
        try:
            track_id = track_url.split("/")[-1].split("?")[0]
            print(f"Fetching track: {track_id}")
            track_data = self.sp.track(track_id)
            return track_data
        except Exception as e:
            print(f"Error fetching track: {e}")
            return None
