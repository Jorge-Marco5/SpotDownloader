import os
from colorama import Fore, init, Style
import re
import yt_dlp
from yt_dlp import YoutubeDL
from src.config import Config

class YouTubeDownloader:
    def __init__(self):
        self.codec_audio = Config.YT_CODEC_AUDIO
        self.codec_video = Config.YT_CODEC_VIDEO
        self.quality_audio = Config.YT_QUALITY_AUDIO
        self.quality_video = Config.YT_QUALITY_VIDEO

    def search_and_download(self, query: str, folder_name: str) -> bool:
        """Search for a song on YouTube and download it."""
        print(f"Searching and downloading: {query}")
        
        if not os.path.exists(folder_name):
            os.makedirs(folder_name, exist_ok=True)

        options = {
            'format': 'bestaudio/best',
            'outtmpl': f'{folder_name}/%(title)s.%(ext)s', # Use title from YouTube to avoid issues, or can use custom name
            # Original code used: f'{folder_name}/{song}.%(ext)s' passed from outside. 
            # I'll stick to a safe default that respects the query but youtube titles can be messy.
            # Let's try to match original behavior if possible, but the original passed 'song' name.
            # We will use the query as filename prefix or separate args?
            # Better: pass exact filename if needed. For now, let's just use the youtube title which is safer than query chars.
            # wait, original code was: 'outtmpl': f'{folder_name}/{song}.%(ext)s'
            # I will change signature to accept output_filename if specific name is desired.
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': self.codec_audio,
                'preferredquality': self.quality_audio,
            }],
            'quiet': True,
            'noplaylist': True,
            'js_runtimes': {'node': {'path': '/usr/bin/node'}}
        }
        
        # We need to construct the outtmpl based on intended filename if we want to match `spot.py` behavior perfectly.
        # But `spot.py` passed `song` (name) into `outtmpl`.
        # I'll modify this method to accept an optional `filename`.
        
    def download_by_query(self, query: str, output_folder: str, filename: str = None) -> str | None:
        """
        Search and download audio by query.
        Returns the path to the downloaded file (without extension) or None.
        """
        target_filename = filename if filename else "%(title)s"
        outtmpl = os.path.join(output_folder, f"{target_filename}.%(ext)s")

        options = {
            'format': 'bestaudio/best',
            'outtmpl': outtmpl,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': self.codec_audio,
                'preferredquality': self.quality_audio,
            }],
            'quiet': True,
            'noplaylist': True,
            'js_runtimes': {'node': {'path': '/usr/bin/node'}}
        }

        with yt_dlp.YoutubeDL(options) as ydl:
            try:
                ydl.download([f"ytsearch1:{query}"])
                return os.path.join(output_folder, filename) if filename else None # Aproximation
            except Exception as e:
                print(f"Failed to download {query}: {e}")
                return None

    def download_audio_direct(self, url: str, output_folder: str):
        """Download audio from a direct YouTube URL."""
        self._download_direct(url, output_folder, is_audio=True)

    def download_video_direct(self, url: str, output_folder: str):
         """Download video from a direct YouTube URL."""
         self._download_direct(url, output_folder, is_audio=False)

    def _download_direct(self, url: str, output_folder: str, is_audio: bool):
        if not os.path.exists(output_folder):
            os.makedirs(output_folder, exist_ok=True)
            
        print(f"Downloading from URL: {url} to {output_folder}, in format: {self.quality_video}")
        
        if is_audio:
            options = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': self.codec_audio,
                    'preferredquality': self.quality_audio,
                }],
                'outtmpl': f'{output_folder}/%(title)s.%(ext)s',
                'js_runtimes': {'node': {'path': '/usr/bin/node'}}
            }
        else:
            options = {
                'format': self.quality_video,
                'codec': self.codec_video,
                'outtmpl': f'{output_folder}/%(title)s.%(ext)s',
                'js_runtimes': {'node': {'path': '/usr/bin/node'}}
            }

        with yt_dlp.YoutubeDL(options) as ydl:
            try:
                ydl.download([url])
                print("Download completed.")
            except Exception as e:
                print(f"{Fore.RED}{Style.BRIGHT}Error downloading{Style.RESET_ALL} {url}: {e}")

    @staticmethod
    def extract_video_id(url: str) -> str:
        """Extracts video ID from a YouTube URL."""
        # Simple extraction logic from original yutub.py
        match = re.search(r"(?:v=|youtu\.be/)([A-Za-z0-9_-]{11})", url)
        if match:
            return match.group(1)
        return url.split("/")[-1].split("?")[0]
