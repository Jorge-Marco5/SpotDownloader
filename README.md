
# SpotDownloader

Script que permite descargar musica y playlists a partir de una url de spotify, por la cual se obtienen los datos de la cancion y se descarga a traves de youtube en formato mp3 






## Instalacion

Requisitos:
**Windows**
* python

Requisitos: **Linux**
* python3
* git
* ffmpeg

Resuisitos: **Android (Termux)** 
* python3
* git
* ffmpeg

---
\
Clone el projecto en una carpeta con:

```bash
  git clone url
```

## Ejemplo de uso

Una vez dentro de la carpeta raiz del proyecto, la primera vez obtenemos los paquetes necesarios de python con:
```bash
  python requirements.py
```
* Despues de la instalacion iniciamos el programa con:
```bash
  python main.py
```
* Seleccionas si quieres descargar una playlist o una cancion

```bash
  ¿Que deseas descargar? [1 playlist| 2 cancion]: [opcion]
```

* Copias la url de tu cancion o playlist de spotify y la pegas en el programa

```bash
  Ingresa la URL de Spotify: [url]
```

* esperas la descarga y listo

```bash
  ¡Descarga completa!
```

## ¡Importante!

No es necesario iniciar _requirements.py_ siempre, solo la primera vez

Dentro del archivo _requirements.py_ vienen instrucciones mas detalladas para su instalacion dependiendo de tu sistema operativo

Las canciones se guardan dentro de la carpeta _/music_ la cual se crea al terminar de configurar el proyecto