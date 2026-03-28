from flask import render_template, request, redirect, url_for
from app import app
from app.utils import obtener_info_youtube, obtener_thumbnail, descargar_audio_yt, obtener_id, obtener_formatos_video, descargar_video_yt, obtener_formatos_audio

@app.route("/")
@app.route("/DYT")
def youtub():
    """Ruta principal para la descarga de YouTube."""
    return render_template("DYT.html", mostrar_contenido=False)

@app.route("/info", methods=["POST"])
def info():
    """Obtiene información de un video de YouTube y sus formatos de audio antes de descargar."""
    url = request.form.get("url")
    if not url:
        return render_template("DYT.html", mensaje="Por favor, ingresa una URL válida.", mostrar_contenido=False)
    
    try:
        titulo, _ = obtener_info_youtube(url)
        thumbnail = obtener_thumbnail(url)
        formatos_audio = obtener_formatos_audio(url)
        return render_template("DYT.html", titulo=titulo, thumbnail=thumbnail, url=url, formatos_audio=formatos_audio, mostrar_contenido=True)
    except Exception as e:
        return render_template("DYT.html", mensaje=f"Error al obtener info: {str(e)}", mostrar_contenido=False)

@app.route("/get_formats", methods=["POST"])
def get_formats():
    """Obtiene la lista de formatos de video disponibles para un video."""
    url = request.form.get("url")
    if not url:
        return render_template("DYT.html", mensaje="URL no proporcionada.", mostrar_contenido=False)
    
    try:
        titulo, _ = obtener_info_youtube(url)
        thumbnail = obtener_thumbnail(url)
        formatos = obtener_formatos_video(url)
        formatos_audio = obtener_formatos_audio(url)
        return render_template("DYT.html", titulo=titulo, thumbnail=thumbnail, url=url, formatos=formatos, formatos_audio=formatos_audio, mostrar_contenido=True)
    except Exception as e:
        return render_template("DYT.html", mensaje=f"Error al obtener formatos: {str(e)}", mostrar_contenido=False)

@app.route("/descargar", methods=["POST"])
def descargar():
    """Inicia la descarga del audio de YouTube."""
    url = request.form.get("url")
    format_id = request.form.get("format_id")
    
    if not url or not format_id:
        return render_template("DYT.html", mensaje="Datos insuficientes para la descarga.", mostrar_contenido=False)

    try:
        audio_file = descargar_audio_yt(url, format_id)
        return render_template("music.html", audio_file=audio_file, url=url)
    except Exception as e:
        return render_template("DYT.html", mensaje=f"Error en la descarga: {str(e)}", mostrar_contenido=False)

@app.route("/descargar_video", methods=["POST"])
def descargar_video():
    """Inicia la descarga del video de YouTube."""
    url = request.form.get("url")
    format_id = request.form.get("format_id")
    
    if not url or not format_id:
        return render_template("DYT.html", mensaje="Datos insuficientes para la descarga.", mostrar_contenido=False)

    try:
        video_file = descargar_video_yt(url, format_id)
        return render_template("music.html", audio_file=video_file, url=url)
    except Exception as e:
        return render_template("DYT.html", mensaje=f"Error en la descarga del video: {str(e)}", mostrar_contenido=False)

if __name__ == "__main__":
    app.run(debug=True)
