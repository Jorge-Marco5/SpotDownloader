import os
import spotipy
import requests
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
import yt_dlp
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error
import re
from colorama import Fore, init
init()

print(Fore.CYAN +"SpotDownloader"+Fore.WHITE)
load_dotenv()  # Carga de el archivo de variables de entorno

#DATOS DE CLIENTE SPOTIFY for DEVELOPERS
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

def sanitize_filename(name):
        return re.sub(r'[\\/*?:"<>|]', "", name)

#Obtener los datos de la playlist
def get_playlist_songs(playlist_url):
    """Fetch all songs from a Spotify playlist."""
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET
    ))
    #Extraer el id de la playlist de la url
    playlist_id = playlist_url.split("/")[-1].split("?")[0]
    #print("Playlist_URL: "+playlist_url)
    print("Playlist_id: "+playlist_id)
    playlist = sp.playlist(playlist_id) #line 656 client.py

    #print(playlist) #request de la playlist

    #Obtener la lista de pistas de la playlist
    songs = []
    for item in playlist['tracks']['items']:
        track = item['track']
        songs.append({
            'name': track['name'],
            'artist': ", ".join(artist['name'] for artist in track['artists']),
            'spotify_url': track['external_urls']['spotify']
        })
    return songs, playlist['name']

#Obtener los datos de la cancion
def get_song(track_url):
    """Fetch song from a Spotify."""
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET
    ))

    #Extraer el id de la playlist de la url
    track_id = track_url.split("/")[-1].split("?")[0]
    #print("Track_url: "+track_url)
    print("Track: "+track_id)
    track_data = sp.track(track_id) #line 363 client py

    return track_data


#busqueda y descarga de la cancion
def search_and_download(song, artist, folder_name):
    """Search for the song on YouTube and download it as an MP3."""
    query = f"{song} {artist}"
    options = {
        'format': 'bestaudio/best',
        'outtmpl': f'{folder_name}/{song}.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'quiet': True
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        try:
            ydl.download([f"ytsearch1:{query}"])
            print(f"Downloaded: {song}")
        except Exception as e:
            print(f"Failed to download {song}: {e}")

#Funcion para aplicar los metadatos a la cancion descargada
def aplicarMetadatos(folder_name, track):
    # ruta de la cancion: music/{track_name} - {artist_name}/{track_name}.mp3
    # ruta de la caratula: music/{track_name} - {artist_name}/{titulo} - {artista}.jpg
    """Apply metadata and cover art to the downloaded audio file."""
    titulo = sanitize_filename(track['name'])
    artista = sanitize_filename(track['artists'][0]['name'])
    album = sanitize_filename(track.get('album', {}).get('name', 'Unknown Album'))
    genero = sanitize_filename(track.get('album', {}).get('genres', ['Unknown Genre'])[0]) if 'album' in track else 'Unknown Genre'
    # Aseguramos que el título y el artista no contengan caracteres no válidos para nombres de archivos
    mp3_file = os.path.join(folder_name, f"{titulo}.mp3")#Ruta del archivo mp3
    print("Aplicando metadatos a : "+f"{titulo}.mp3")

    # Descargar carátula de la canción
    cover_url = None
    if 'album' in track and 'images' in track['album'] and len(track['album']['images']) > 0:
        cover_url = track['album']['images'][0]['url']

    cover_path = None
    if cover_url:
        # La ruta de la carátula debe ser: music/{track_name} - {artist_name}/{titulo} - {artista}.jpg
        cover_path = os.path.join(folder_name, f"{titulo} - {artista}.jpg")
        descargarCaratula(cover_url, cover_path)
    #aplicar metadatos a la pista
    try:
        audio = EasyID3(mp3_file)
    except Exception:
        audio = MP3(mp3_file, ID3=ID3)
        audio.add_tags()
        audio = EasyID3(mp3_file)

    audio["title"] = track['name']
    audio["artist"] = track['artists'][0]['name']
    audio["album"] = track.get('album', {}).get('name', 'Unknown Album')
    audio["genre"] = genero
    audio.save()

    if cover_path and os.path.exists(cover_path):
        audio = MP3(mp3_file, ID3=ID3)
        with open(cover_path, "rb") as img:
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
        print("Metadatos actualizados correctamente.")
    else:
        print("Metadatos actualizados (sin carátula).")

#descargar caratula de la pista descargada
def descargarCaratula(url, cover_path):
    """Download cover art and save to the specified path."""
    try:
        respuesta = requests.get(url, stream=True)
        respuesta.raise_for_status()
        with open(cover_path, 'wb') as archivo:
            for chunk in respuesta.iter_content(1024):
                archivo.write(chunk)
        return cover_path
    except Exception as e:
        print(f"Error al descargar la imagen: {e}")
        return None

#Funcion principal
def main():
    opcion = int(input("¿Que deseas descargar? [1 playlist| 2 cancion]: "))
    match opcion:
        case 1:
           downloadPlaylist()
        case 2:
            downloadTrack()
        case _:
            print("Sin opcion")

#Funcion de descarga de la playlist
def downloadPlaylist():
    print(Fore.CYAN+"\nDescargar playlist"+Fore.WHITE)
    playlist_url = input("Ingresa la URL de spotify: ")
    songs, playlist_name = get_playlist_songs(playlist_url)

    playlist_name = sanitize_filename(playlist_name)
    folder_name = f"music/{playlist_name}"
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
    #Guardamos los detalles de la descarga de la playlist en un archivo csv
    #save_to_csv(songs, playlist_name)

    #Descargar Musica
    for song in songs:
        search_and_download(song['name'], song['artist'], folder_name)

    print(Fore.GREEN+f"Canciones descargadas en la carpeta: {folder_name}"+Fore.WHITE)
    main_menu = input("¿Deseas volver al menú principal? (s/n): ")
    if main_menu.lower() == 's':
        main()
    else:
        print("Saliendo del programa. ¡Hasta luego!")

#Funcion de descarga de pista individual
def downloadTrack():
    """
    Obtiene la URL de una canción de Spotify, la procesa y la descarga.
    """
    print("\nDescargar canción 🎵")
    track_url = input("Ingresa la URL de Spotify: ")

    # Asumimos que get_song devuelve el objeto completo de la canción y su nombre
    track = get_song(track_url)

    if not track:
        print(Fore.RED+"No se pudo obtener la información de la canción."+Fore.WHITE)
        return

    # Extraer los datos directamente del objeto 'track'
    track_name = track['name']
    # El artista está en una lista, tomamos el primero
    artist_name = track['artists'][0]['name']

    # Creación de la carpeta con el nombre de la cancion
    # Es más seguro usar un nombre de carpeta sanitizado
    track_name = sanitize_filename(track_name)
    artist_name = sanitize_filename(artist_name)
    folder_name = f"music/{track_name} - {artist_name}"
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)

    # Descargar canción (sin bucle)
    print(Fore.CYAN+f"Iniciando descarga de '{track_name}' - {artist_name}..."+Fore.WHITE)
    search_and_download(track_name, artist_name, folder_name)
    #aplicar metadatos de cada cancion
    aplicarMetadatos(folder_name, track)
    print(Fore.GREEN+"¡Descarga completa!")

    main_menu = input(Fore.WHITE+"¿Deseas volver al menú principal? (s/n): ")
    if main_menu.lower() == 's':
        main()
    else:
        print(Fore.CYAN+"Saliendo del programa. ¡Hasta luego!")

if __name__ == "__main__":
    main()
