from flask import render_template, request
from app import app
from app.utils import obtener_info_youtube, obtenerThumbnail, descargar_audio_YT
import webbrowser

#Descarga de contenido de spotify
@app.route("/")
def index():
    return render_template("DYT.html")

#Descarga de contenido de spotify
@app.route("/DSP")
def spot():
    return render_template("DSP.html")

@app.route("/music")
def music():
    return render_template("music.html", audio_file = "Hola")
    #Extraer los datos de la URL
#Descarga de contenido de youtube
@app.route("/DYT")
def youtub():
        mostrar_contenido = False
        return render_template("DYT.html", mostrar_contenido=mostrar_contenido)

#Obtener informacion de la musica
@app.route("/info", methods=["POST"])
def info():
    url = request.form["url"]
    try:
        titulo = obtener_info_youtube(url)
        thumbnail = obtenerThumbnail(url)
        url = url
        mostrar_contenido = True
        return render_template("DYT.html", titulo=titulo, thumbnail=thumbnail, url = url, mostrar_contenido = mostrar_contenido)
    except Exception as e:
        return f"Ocurrió un error: {e}"

@app.route("/descargar", methods=["POST"])
def descargar():
    url = request.form["url"]
    if not url:
        return render_template("DYT.html", mensaje="Por favor, ingresa una URL válida.")

    quality = request.form["quality"]
    try:
        audio_file = descargar_audio_YT(url, quality)
        return render_template("music.html", audio_file=audio_file)
    except Exception as e:
        return f"Ocurrió un error: {e}"



if __name__ == "__main__":
    app.run(debug=True)
