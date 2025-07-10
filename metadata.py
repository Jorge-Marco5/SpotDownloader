from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error
from sanitize import sanitize_filename
import os
import requests

class aplicarMetadatos():
    #obtenemos informacion de la cancion
    def __init__(self, folder_name, track):
        self.folder_name = folder_name
        self.track = track
        self.titulo = sanitize_filename(track['name'])
        self.artista = sanitize_filename(track['artists'][0]['name'])
        self.album = sanitize_filename(track.get('album', {}).get('name', 'Unknown Album'))
        self.genero = sanitize_filename(track.get('album', {}).get('genres', ['Unknown Genre'])[0]) if 'album' in track and 'genres' in track['album'] else 'Unknown Genre'
        self.cover_url = None
        self.cover_path = f"music/{self.titulo} - {self.artista}"
        self.mp3_file = os.path.join(self.folder_name, f"{self.titulo}.mp3")


#aplicamos metadatos a la cancion
    def aplicar_metadatos(self):
        mp3_file = os.path.join(self.folder_name, f"{self.titulo}.mp3")#Ruta del archivo mp3
        try:
            audio = EasyID3(mp3_file)
        except Exception:
            audio = MP3(mp3_file, ID3=ID3)
            audio.add_tags()
            audio = EasyID3(mp3_file)

        audio["title"] = self.track['name']
        audio["artist"] = self.track['artists'][0]['name']
        audio["album"] = self.track.get('album', {}).get('name', 'Unknown Album')
        audio["genre"] = self.genero
        audio.save()

#obtenemos el url de la caratula
    def url_caratula(self):
        # Descargar carátula de la canción
        if 'album' in self.track and 'images' in self.track['album'] and len(self.track['album']['images']) > 0:
            self.cover_url = self.track['album']['images'][0]['url']
            #print(self.cover_url)

#Damos nombre a la caratula de la cancion
    def obtenerNombreCaratula(self, ):
        if self.cover_url:
            # La ruta de la carátula debe ser: music/{track_name} - {artist_name}/{titulo} - {artista}.jpg
            self.cover_path = os.path.join(self.folder_name, f"{self.titulo} - {self.artista}.jpg")
            #descargarCaratula(self.cover_url, self.cover_path)

#Descarga de la caratula y aplicamos el nombre
    def descargarCaratula(self):
        """Descarga la carátula y la guarda en la ruta especificada."""
        if not self.cover_url:
            print("No hay URL de carátula disponible.")
            return None
        self.obtenerNombreCaratula()
        try:
            respuesta = requests.get(self.cover_url, stream=True, timeout=10)
            respuesta.raise_for_status()
            with open(self.cover_path, 'wb') as archivo:
                for chunk in respuesta.iter_content(1024):
                    archivo.write(chunk)
            return self.cover_path
        except Exception as e:
            print(f"Error al descargar la imagen: {e}")
            return None

    def aplicar_caratula(self):
        if self.cover_path and os.path.exists(self.cover_path):
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
            print("Metadatos actualizados correctamente.")
        else:
            print("Metadatos actualizados (sin carátula).")

    def run(self):
        self.aplicar_metadatos()
        self.url_caratula()
        self.descargarCaratula()
        self.aplicar_caratula()