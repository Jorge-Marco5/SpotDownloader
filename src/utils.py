import re
import os
import time
from yt_dlp import YoutubeDL

# Configuración de limpieza (en segundos)
MAX_FILE_AGE = 600  # 10 minutos

def obtener_info_youtube(url):
    """
    Obtiene metadatos básicos de un video de YouTube.
    
    :param url: URL del video de YouTube.
    :return: Una tupla con (título, video_id).
    """
    ydl_opts = {"quiet": True}
    with YoutubeDL(ydl_opts) as ydl:
        # Extraer información del video
        info = ydl.extract_info(url, download=False)
        titulo = info.get("title", "Desconocido")
        video_id = info.get("id")
        return titulo, video_id

def obtener_thumbnail(url):
    """
    Genera la URL de la miniatura de un video de YouTube.
    
    :param url: URL del video de YouTube.
    :return: URL de la imagen de miniatura.
    """
    video_id = obtener_id(url)
    if not video_id:
        return None
    return f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"

def obtener_id(url):
    """
    Extrae el ID de un video de YouTube a partir de su URL.
    
    :param url: URL del video de YouTube.
    :return: El ID del video de 11 caracteres o None si no se encuentra.
    """
    # Regex mejorado para cubrir shorts, youtu.be y youtube.com/watch?v=
    match = re.search(r"(?:v=|youtu\.be/|shorts/|embed/)([A-Za-z0-9_-]{11})", url)
    if match:
        return match.group(1)
    return None

def sanitizar_nombre_archivo(nombre):
    """
    Elimina caracteres no permitidos en nombres de archivo por el sistema operativo.
    
    :param nombre: Cadena de texto a sanitizar.
    :return: Cadena de texto limpia.
    """
    return re.sub(r'[\\/*?:"<>|]', "", nombre).strip()

def limpiar_archivos_temporales():
    """
    Elimina archivos de las carpetas de música y video que superen MAX_FILE_AGE.
    """
    directorios = ["src/static/music", "src/static/videos"]
    ahora = time.time()
    
    for directorio in directorios:
        if not os.path.exists(directorio):
            continue
            
        for archivo in os.listdir(directorio):
            ruta_archivo = os.path.join(directorio, archivo)
            # No borrar archivos ocultos o carpetas
            if os.path.isfile(ruta_archivo) and not archivo.startswith('.'):
                try:
                    fecha_creacion = os.path.getmtime(ruta_archivo)
                    if ahora - fecha_creacion > MAX_FILE_AGE:
                        os.remove(ruta_archivo)
                        print(f"Limpieza: Archivo eliminado -> {archivo}")
                except Exception as e:
                    print(f"Error al limpiar {archivo}: {e}")

def descargar_audio_yt(url, format_id):
    """
    Descarga el audio de un video de YouTube dado un format_id específico y lo convierte a MP3.
    Realiza una limpieza previa de archivos antiguos.
    
    :param url: URL del video de YouTube.
    :param format_id: ID del formato de audio seleccionado.
    :return: El nombre del archivo descargado con extensión .mp3.
    """
    limpiar_archivos_temporales() # Ejecutar limpieza antes de una nueva descarga
    
    titulo, _ = obtener_info_youtube(url)
    titulo_limpio = sanitizar_nombre_archivo(titulo)
    
    opciones = {
        'format': format_id,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': "mp3",
            'preferredquality': '320', # Calidad base de conversión
        }],
        'outtmpl': f"src/static/music/{titulo_limpio}.%(ext)s",
        'quiet': True,
        'no_warnings': True,
    }

    with YoutubeDL(opciones) as ydl:
        ydl.download([url])

    return f"{titulo_limpio}.mp3"

def obtener_formatos_audio(url):
    """
    Obtiene la lista de formatos de solo audio disponibles para una URL de YouTube.
    
    :param url: URL del video de YouTube.
    :return: Lista de diccionarios con la información de cada formato de audio.
    """
    ydl_opts = {"quiet": True}
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        formats = info.get("formats", [])
        
        lista_formatos = []
        for f in formats:
            # Filtrar formatos que sean solo audio
            if f.get("vcodec") == "none" and f.get("acodec") != "none":
                ext = f.get("ext")
                fid = f.get("format_id")
                
                # Intentar obtener bitrate de abr (audio bitrate) o tbr (total bitrate)
                abr = f.get("abr") or f.get("tbr")
                
                # Intentar obtener tamaño de múltiples fuentes
                size = f.get("filesize") or f.get("filesize_approx")
                
                # Omitir formatos conocidos por no tener metadatos si no aportan información útil
                if not abr and not size and fid in ['233', '234', '233-0', '234-0']:
                    continue
                
                size_str = f"{round(size / 1024 / 1024, 2)} MB" if size else "Desconocido"
                bitrate_str = f"{int(abr)} kbps" if abr else "Variable"
                
                lista_formatos.append({
                    "id": fid,
                    "ext": ext,
                    "bitrate": bitrate_str,
                    "size": size_str
                })
        
        # Eliminar duplicados y priorizar por calidad de bitrate
        vistos = set()
        resultado = []
        # Sort by bitrate descending, putting "Variable" at the end
        def sort_key(x):
            try:
                if "kbps" in x["bitrate"]:
                    return int(x["bitrate"].split()[0])
            except:
                pass
            return 0

        fix_formats= [
            {
                "id": "248",
                "ext": "mp3",
                "bitrate": "160 kbps",
                "size": "-"
            },
            {
                "id": "249",
                "ext": "mp3",
                "bitrate": "192 kbps",
                "size": "-"
            },
            {
                "id": "250",
                "ext": "mp3",
                "bitrate": "256 kbps",
                "size": "-"
            },
            {
                "id": "251",
                "ext": "mp3",
                "bitrate": "320 kbps",
                "size": "-"
            },
        ]

        for fmt in sorted(lista_formatos, key=sort_key, reverse=True):
            if fmt["bitrate"] not in vistos:
                resultado.append(fmt)
                vistos.add(fmt["bitrate"])
        
        resultado.extend(fix_formats)
        return resultado

def obtener_formatos_video(url):
    """
    Obtiene la lista de formatos de video disponibles para una URL de YouTube.
    
    :param url: URL del video de YouTube.
    :return: Lista de diccionarios con la información de cada formato.
    """
    ydl_opts = {"quiet": True}
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        formats = info.get("formats", [])
        
        lista_formatos = []
        for f in formats:
            # Filtrar formatos que tengan video (vcodec != none)
            if f.get("vcodec") != "none":
                res = f.get("resolution") or f"{f.get('width')}x{f.get('height')}"
                ext = f.get("ext")
                fid = f.get("format_id")
                note = f.get("format_note")
                size = f.get("filesize") or f.get("filesize_approx")
                
                size_str = f"{round(size / 1024 / 1024, 2)} MB" if size else "N/A"
                
                lista_formatos.append({
                    "id": fid,
                    "ext": ext,
                    "resolution": res,
                    "note": note,
                    "size": size_str
                })
        
        # Ordenar por resolución de mayor a menor (aproximadamente)
        return sorted(lista_formatos, key=lambda x: x["resolution"], reverse=True)

def descargar_video_yt(url, format_id):
    """
    Descarga un video de YouTube con un formato específico.
    Realiza una limpieza previa de archivos antiguos.
    
    :param url: URL del video de YouTube.
    :param format_id: ID del formato seleccionado.
    :return: El nombre del archivo descargado con extensión .mp4.
    """
    limpiar_archivos_temporales() # Ejecutar limpieza antes de una nueva descarga
    
    titulo, _ = obtener_info_youtube(url)
    titulo_limpio = sanitizar_nombre_archivo(titulo)
    
    # Asegurar que la carpeta de videos existe
    os.makedirs("src/static/videos", exist_ok=True)
    
    opciones = {
        'format': f"{format_id}+bestaudio/best", # Combina video seleccionado con mejor audio
        'merge_output_format': 'mp4',
        'outtmpl': f"src/static/videos/{titulo_limpio}.%(ext)s",
        'quiet': True,
        'no_warnings': True,
    }

    with YoutubeDL(opciones) as ydl:
        ydl.download([url])

    return f"{titulo_limpio}.mp4"