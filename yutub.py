from yt_dlp import YoutubeDL
import yt_dlp
from colorama import Fore, init
from dotenv import load_dotenv
import os
import re
load_dotenv()  # Carga de el archivo de variables de entorno
init()

#Clase de control de las descargas de audio
class descargarAudio():
    #DATOS DE CLIENTE SPOTIFY for DEVELOPERS

    def __init__(self, url, quality):
        YT_CODEC_AUDIO = os.getenv("YT_CODEC_AUDIO")
        YT_QUALITY_AUDIO = os.getenv("YT_QUALITY_AUDIO")
        self.codec_audio = YT_CODEC_AUDIO
        #cuando no haya indicaciones de audio se toma el por defecto
        self.url = url
        if quality == None:
            self.quality_audio = YT_QUALITY_AUDIO
        else:
            self.quality_audio = quality

    def obtenerTitulo(self):
        ydl_opts = {}
        with YoutubeDL(ydl_opts) as ydl:
            # Extraer información del video
            info = ydl.extract_info(self.url, download=False)
            # Obtener el título
            self.titulo = info.get("title")
            #print("Titulo:", self.titulo)

    def descargar_audio(self):
        self.obtenerTitulo()  # Asegura que self.titulo esté definido antes de usarlo
        folder_name = f"music/{self.titulo}"
        if not os.path.exists(folder_name):
                os.mkdir(folder_name)
        print("descargando audio de: "+self.url)
        opciones = {
            'format': 'bestaudio/best',  # Selecciona el mejor formato de audio disponible
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',  # Usa FFmpeg para extraer el audio
                'preferredcodec': self.codec_audio,     # Convierte el audio a formato MP3
                'preferredquality': self.quality_audio,   # Calidad del audio (192 kbps)
            }],
            'outtmpl': folder_name+"/"+self.titulo,  # Nombre del archivo de salida
        }

        with yt_dlp.YoutubeDL(opciones) as ydl:
            ydl.download([self.url]) # Descarga el audio desde la URL proporcionada

    def run(self):
        self.descargar_audio()
        print("Audio descargado correctamente.")

        print(Fore.WHITE+"\n¿Quieres continuar descargando? ")
        print("s -si")
        print("n -no")
        main_menu = input("opcion: ")
        if main_menu.lower() == 's':
            main()
        else:
            print(Fore.CYAN+"Saliendo del programa. ¡Hasta luego!")

#Clase de control de las descargas de video
class descargarVideo():
    def __init__(self, url):
        #Obtenemos la calidad de video por defecto de el archivo .env
        YT_QUALITY_VIDEO = os.getenv("YT_QUALITY_VIDEO")
        self.quality_video = YT_QUALITY_VIDEO
        self.url = url
    #Obtenemos el nombre del video
    def obtenerTitulo(self):
        ydl_opts = {}
        with YoutubeDL(ydl_opts) as ydl:
            # Extraer información del video
            info = ydl.extract_info(self.url, download=False)
            # Obtener el título
            self.titulo = info.get("title")
            #print("Titulo:", self.titulo)
    #Descarga del video
    def descargar_audio(self):
        self.obtenerTitulo()  #Obtenemos el titulo
        folder_name = f"videos/{self.titulo}"#Creacion del folder donde se descarga la cancion
        if not os.path.exists(folder_name):
                os.mkdir(folder_name)
        print("descargando audio de: "+self.url)
        opciones = {
            'format': self.quality_video,#Mejor calidad posible por defecto
            'outtmpl': folder_name+'/%(title)s.%(ext)s',  # Ruta y nombre del archivo
        }

        with yt_dlp.YoutubeDL(opciones) as ydl:
            ydl.download([self.url]) # Descarga el audio desde la URL proporcionada

    def run(self):
        self.descargar_audio()
        print("video descargado correctamente.")

        print(Fore.WHITE+"\n¿Quieres continuar descargando? ")
        print("s -si")
        print("n -no")
        main_menu = input("opcion: ")
        if main_menu.lower() == 's':
            main()
        else:
            print(Fore.CYAN+"Saliendo del programa. ¡Hasta luego!")


def main():
    print(Fore.WHITE+"Descarga contenido de"+Fore.RED+" Youtube")
    url = input(Fore.WHITE+"\nURL: ")
    #print("Convirtiendo URL en formato valido")
    url = conversionURL(url)

    print("¿Que deseas descargar? ")
    print("1.-audio")
    print("2.-video")
    opcion = int(input(" : "))
    match opcion:
        case 1:
            audio = descargarAudio(url, 320)
            audio.run()
        case 2:
            video = descargarVideo(url)
            video.run()
        case _:
            print("Sin opcion")

def conversionURL(url):
    id = None
    resultado = url.split("/")[-1].split("?")[0]
    print("ID: "+resultado)

    match = re.search(r"(?:v=|youtu\.be/)([A-Za-z0-9_-]{11})", url)
    if match:
        id = match.group(1)
    else:
        id = resultado  # fallback

    URL = "https://www.youtube.com/watch?v="+id
    #print("URL: "+URL)
    return URL

if __name__ == "__main__":
    main()