# SP_PlaylistDownloader

Script de Python para descargar playlists o canciones individuales de Spotify y videos/audio de YouTube de manera automática.

> [!WARNING]
> Este proyecto utiliza librerías de terceros que pueden dejar de funcionar en cualquier momento debido a cambios en las políticas de YouTube o Spotify.

**Descargo de Responsabilidad**:
Este software es para fines educativos únicamente. Asegúrate de tener los derechos necesarios sobre el contenido que descargues.

## Requisitos Previos

1.  **Python 3.8+** instalado.
2.  **Git** instalado.
3.  **FFmpeg** instalado en tu sistema (necesario para la conversión de audio).
    - **Linux (Debian/Ubuntu)**: `sudo apt install ffmpeg`
    - **Windows**: [Descargar e instalar FFmpeg](https://ffmpeg.org/download.html) (y agregar al PATH).
    - **Termux**: `pkg install ffmpeg`

4.  **Cuenta de Spotify Developers**:
    - Ve a [Spotify Dashboard](https://developer.spotify.com/dashboard/).
    - Crea una App y obtén tu `Client ID` y `Client Secret`.

## Instalación

1.  Clona el repositorio:

    ```bash
    git clone https://github.com/Jorge-Marco5/SpotDownloader.git
    cd SpotDownloader
    ```

2.  Instala las dependencias de Python:

    ```bash
    pip install -r requirements.txt
    ```

3.  Configura tus credenciales:
    - Crea un archivo llamado `.env` en la raíz del proyecto.
    - Agrega tus claves de Spotify como se muestra a continuación:

    ```env
    SPOTIFY_CLIENT_ID=tu_client_id_aqui
    SPOTIFY_CLIENT_SECRET=tu_client_secret_aqui
    YT_CODEC_AUDIO=mp3
    YT_QUALITY_AUDIO=192
    YT_QUALITY_VIDEO=best
    ```

## Uso

Ejecuta el script principal:

```bash
python3 src/main.py
```

Sigue las instrucciones en pantalla para:

1.  Descargar una playlist completa de Spotify.
2.  Descargar una sola canción de Spotify.
3.  Descargar audio o video desde un enlace directo de YouTube.
