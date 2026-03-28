import os
import sys
from colorama import Fore, init, Style

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.spotify import SpotifyClient
from core.youtube import YouTubeDownloader
from utils.metadata import MetadataApplier
from utils.sanitation import sanitize_filename

init(autoreset=True)

class SpotDownloaderApp:
    def __init__(self):
        self.spotify = SpotifyClient()
        self.downloader = YouTubeDownloader()

    def run(self):
        while True:
            self.print_header()
            print("1. Descargar Playlist de Spotify")
            print("2. Descargar Canción de Spotify")
            print("3. Descargar Audio/Video de YouTube")
            print("0. Salir")
            
            try:
                choice = input("\nElige una opción: ").strip()
            except KeyboardInterrupt:
                 print("\nSaliendo...")
                 break

            if choice == '1':
                self.download_spotify_playlist()
            elif choice == '2':
                self.download_spotify_track()
            elif choice == '3':
                self.download_youtube_content()
            elif choice == '0':
                print(Fore.CYAN + "¡Hasta luego!")
                break
            else:
                print(Fore.RED + "Opción no válida.")
            
            input(Fore.YELLOW + "\nPresiona Enter para continuar...")

    def print_header(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Fore.GREEN + Style.BRIGHT + r"""
  ____  ____   ___  _____ ____   _____        __  _   _ 
 / ___||  _ \ / _ \|_   _|  _ \ / _ \ \      / / | \ | |
 \___ \| |_) | | | | | | | | | | | | \ \ /\ / /  |  \| |
  ___) |  __/| |_| | | | | |_| | |_| |\ V  V /   | |\  |
 |____/|_|    \___/  |_| |____/ \___/  \_/\_/    |_| \_|
                                                        
        """ + Fore.WHITE + "Spotify & YouTube Downloader\n")

    def download_spotify_playlist(self):
        print(Fore.GREEN + "\n--- Descargar Playlist de Spotify ---")
        url = input("Ingresa la URL de la playlist: ").strip()
        if not url: return

        songs, playlist_name = self.spotify.get_playlist_songs(url)
        if not songs:
            print(Fore.RED + "No se encontraron canciones o hubo un error.")
            return

        print(Fore.GREEN + f"Playlist encontrada: {playlist_name} ({len(songs)} canciones)")
        
        safe_playlist_name = sanitize_filename(playlist_name)
        folder_path = os.path.join("music", safe_playlist_name)
        
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        for i, song in enumerate(songs, 1):
            print(f"\n[{i}/{len(songs)}] Procesando: {song['name']} - {song['artist']}")
            query = f"{song['name']} {song['artist']}"
            
            safe_title = sanitize_filename(song['name'])
            # Pass filename explicitly to ensure we can find it for metadata
            filename = safe_title 
            
            downloaded_path = self.downloader.download_by_query(query, folder_path, filename)
            
            if downloaded_path:
                print(Fore.BLUE + "Aplicando metadatos...")
                # We need to reconstruct the MetadataApplier. 
                # Note: download_by_query returns path without extension? 
                # No, I implemented it to return joined path or None. 
                # Wait, my implementation of download_by_query used: os.path.join(output_folder, filename)
                # And the outtmpl added .%(ext)s.
                # So the file on disk is filename + ".mp3" (assuming preferredcodec is mp3).
                
                # MetadataApplier expects folder_name and track dict.
                # It constructs mp3 path internally as: os.path.join(self.folder_name, f"{self.title}.mp3")
                # where self.title = sanitize_filename(track['name']).
                # This matches 'safe_title' used above. 
                
                meta = MetadataApplier(folder_path, song)
                meta.run()
        
        print(Fore.GREEN + f"\n¡Descarga de playlist completada en: {folder_path}!")

    def download_spotify_track(self):
        print(Fore.GREEN + "\n--- Descargar Canción de Spotify ---")
        url = input("Ingresa la URL de la canción: ").strip()
        if not url: return

        track = self.spotify.get_song(url)
        if not track:
            print(Fore.RED + "No se pudo obtener la canción.")
            return

        track_name = track['name']
        artist_name = track['artists'][0]['name']
        
        print(Fore.GREEN + f"Canción encontrada: {track_name} - {artist_name}")

        safe_track_name = sanitize_filename(track_name)
        safe_artist_name = sanitize_filename(artist_name)
        
        folder_name = f"{safe_track_name} - {safe_artist_name}"
        folder_path = os.path.join("music", folder_name)

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        query = f"{track_name} {artist_name}"
        self.downloader.download_by_query(query, folder_path, safe_track_name)
        
        print(Fore.BLUE + "Aplicando metadatos...")
        meta = MetadataApplier(folder_path, track)
        meta.run()
        print(Fore.GREEN + "¡Descarga completada!")

    def download_youtube_content(self):
        print(Fore.RED + "\n--- Descargar de YouTube ---")
        url = input("Ingresa la URL de YouTube: ").strip()
        if not url: return

        print("1. Audio (MP3)")
        print("2. Video")
        type_choice = input("Opción: ").strip()

        video_id = self.downloader.extract_video_id(url)
        if not video_id:
             print(Fore.RED + "URL inválida.")
             return
             
        # Reconstruct valid URL (optional, but good for standardization)
        clean_url = f"https://www.youtube.com/watch?v={video_id}"

        if type_choice == '1':
            title = self.downloader.extract_video_id(url) # Temporary, cleaner would be to let yt-dlp handle name
            # yutub.py logic was doing extra request to get title. 
            # My core/youtube.py logic in _download_direct gets title via ytdlp.
            # folder logic: music/{title} 
            # I need to fetch title first if I want to create a specific folder for it, 
            # OR just download to a generic folder.
            # The original code created a folder per video.
            # Let's keep it simple for now and download to 'music/downloads' or similar, 
            # OR try to replicate the folder-per-song behavior if really needed.
            # yutub.py: folder_name = f"music/{self.titulo}"
            
            # To get title beforehand I'd need an extra call. 
            # Let's simplify and just download to 'music' or 'videos' for now to save API calls/time, 
            # or use a generic "YouTube Downloads" folder.
            # User experience: "music/{Title}" is nice but creates many folders.
            
            output_folder = "music/YouTube"
            self.downloader.download_audio_direct(clean_url, output_folder)
            
        elif type_choice == '2':
            output_folder = "videos/YouTube"
            self.downloader.download_video_direct(clean_url, output_folder)
        else:
            print("Opción inválida")

if __name__ == "__main__":
    try:
        app = SpotDownloaderApp()
        app.run()
    except Exception as e:
        print(f"Error fatal: {e}")
        input("Presiona Enter para salir...")
