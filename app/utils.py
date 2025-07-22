import re
from yt_dlp import YoutubeDL
import yt_dlp

def obtener_info_youtube(url):
    ydl_opts = {}
    with YoutubeDL(ydl_opts) as ydl:
        # Extraer información del video
        info = ydl.extract_info(url, download=False)
        # Obtener el título
        titulo = info.get("title")
        print("Título: " + titulo)
        return titulo

def obtenerThumbnail(url):
    id = obtenerID(url)
    thumbnail = "https://img.youtube.com/vi/"+id+"/maxresdefault.jpg"
    print("Thumbnail: " + thumbnail)
    return thumbnail

def obtenerID(url):
    id = None
    resultado = url.split("/")[-1].split("?")[0]
    print("ID: "+resultado)

    match = re.search(r"(?:v=|youtu\.be/)([A-Za-z0-9_-]{11})", url)
    if match:
        id = match.group(1)
    else:
        id = resultado  # fallback

    return id

def descargar_audio_YT(url, quality):
    
    titulo = obtener_info_youtube(url)
    opciones = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': "mp3",
            'preferredquality': quality,
        }],
        'outtmpl': f"app/static/music/{titulo}.%(ext)s",  # Guarda en la carpeta seleccionada
    }

    with yt_dlp.YoutubeDL(opciones) as ydl:
        ydl.download([url])

    return titulo