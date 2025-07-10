import subprocess
import sys
from colorama import Fore, init
import os
init()

"""
09/07/2025

Instalacion en windows:
1-descargar e instalar python desde https://www.python.org/downloads/
2-descargar e instalar git desde https://git-scm.com/downloads
3-ir a la carpeta donde se clonara el repositorio y abrir una terminal
4-clonar el repositorio con el comando: git clone https://github.com/Jorge-Marco5/SpotDownloader.git
5-ingresar a la carpeta del repositorio con el comando: cd SpotDownloader
6-Inicia el instalador de paquetes con el comando: python requirements.py
7-Una ves que termine la instalacion, ejecuta el comado python main.py para iniciar el programa

Instalacion en linux (Los comandos pueden variar dependiendo de la distribucion):
1-abre una terminal y ejecuta los siguientes coomandos:
2-sudo apt update -y && sudo apt upgrade -y
3-sudo apt install python3-dev build-essential -y
4-sudo apt install git -y
4.1 instalar ffmpeg: apt install ffmpeg -y
5-ir a la carpeta donde se clonara el repositorio
6-clonar el repositorio con el comando: git clone https://github.com/Jorge-Marco5/SpotDownloader.git
7-ingresar a la carpeta del repositorio con el comando: cd SpotDownloader
8-Inicia el instalador de paquetes con el comando: python3 requirements.py
9-una vez que termine la instalacion  ejecuta el comando python3 main.py para iniciar el programa

Instalacion en Android con Termux:
1-abre una terminal y ejecuta los siguientes comandos:
2-actualizar terminal: pkg update -y && pkg upgrade -y
3-instalar python: pkg install python -y
4-instalar paqueteria necesaria de python: apt install python build-essential
4.1 instalar ffmpeg: pkg install ffmpeg -y
5-Instalar GIT: pkg install git -y
6-dar permisos a la aplicacion para acceder al almacenamiento interno a traves del comando: termux-setup-storage
7-ingresar a la siguiente ruta con el comando: cd storage/shared/
8-crea una carpeta nueva; mkdir NombreCarpeta
9-ingresar a la carpeta: cd NombreCarpeta
10-clonar el repositorio con el comando: git clone https://github.com/Jorge-Marco5/SpotDownloader.git
11-ingresar a SpotDownloader: cd SpotDownloader
12-Inicia el instalador de paquetes con el comando: python requirements.py
13-Una ves que termine la instalacion, ejecuta el comado python main.py para iniciar el programa
14 instala: pip install colorama
15 si aparece un error al descargar la musica descarga: pip install ffmpeg-python

IMPORTANTE:
En caso de obtener un error al momento de obtener los metadatos de la cancion, descarga el paquete ffmpeg
apt install ffmpeg -y

moverse entre carpetas en la terminal:
para regresar una carpeta   cd ..
para ingresar a una carpeta cd NombreCarpeta
"""

def instalar_paquetes():
    crear_archivo_env()
    try:
        print(Fore.CYAN+"\nIniciando descarga de los paquetes. Esto puede tomar tiempo...\n"+Fore.WHITE)
        # Ejecuta el comando pip para instalar los paquetes
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        if not os.path.exists("music"):
            os.mkdir("music")
        print(Fore.GREEN+"¡Todos los paquetes han sido instalados correctamente!")
        print("Ejecuta el comando 'python main.py' para empezar a descargar tu musica")
    except FileNotFoundError:
        print(Fore.RED+"Error: No se encontró el archivo 'requirements.txt'. Asegúrate de que esté en el directorio actual.")
        print(Fore.WHITE)
    except subprocess.CalledProcessError as e:
        print(Fore.RED+f"Error durante la instalación de paquetes: {e}")
        print(Fore.WHITE)
    except Exception as e:
        print(Fore.RED+f"Ha ocurrido un error inesperado: {e}")
        print(Fore.WHITE)


def crear_archivo_env(nombre_archivo=".env", variables=None):

    """Creacion del archivo de variables de entorno para la configuracion del proyecto.
    """
    print("\n___________________________________")
    print(Fore.CYAN+"Creando archivo de configuración...(.env)\n")
    print(Fore.WHITE+"Si no tienes una cuenta de spotify, puedes crear una en https://www.spotify.com/signup/")
    print("Si no tienes una cuenta de spotify for developers, puedes crear una en https://developer.spotify.com/dashboard/login\n")
    print("En la pagina de spotify for developers, crea una nueva app y obten tu client_id y client_secret, necesarios para acceder a la api de spotify\n")
    print("Tranquilo..., estos datos se almacenan de manera local, ni el creador del programa tiene conocimiento de ellos.\n")
    spotify_client_id = input("Spotify Client ID: ").strip()
    spotify_client_secret = input("Spotify Client Secret: ").strip()

    if variables is None:
        variables = {}
        variables["SPOTIFY_CLIENT_ID"] = spotify_client_id
        variables["SPOTIFY_CLIENT_SECRET"] = spotify_client_secret

    try:
        with open(nombre_archivo, "w") as archivo:
            for clave, valor in variables.items():
                archivo.write(f"{clave}={valor}\n")
        print(Fore.GREEN+f"\nArchivo '{nombre_archivo}' creado exitosamente.\n")
    except Exception as e:
        print(Fore.RED+f"\nError al crear el archivo: {e}\n")

def main():
    print(Fore.CYAN +"\nBienvenido al instalador de paquetes de SpotDownloader\n")
    print(Fore.RED +"DESCARGO DE RESPONSABILIDAD:")
    print(Fore.WHITE +"Recuerda que preferiblemente descargues audios y videos que te pertenezcan o a los que tengas permiso.")
    print("Eres libre de hacer lo que gustes, el uso de este script es bajo TU RESPONSABILIDAD\n")
    print("Si tienes problemas con la instalación, asegúrate de tener pip instalado y actualizado.")
    print("'apt install python3 build-essential' ó 'pip install build-essential'\n")
    print("Este script instalará los siguientes paquetes necesarios y configuraciones para ejecutar el proyecto.\n")
    #mostrar los paquetes a instalar de requirements.txt
    with open("requirements.txt", "r", encoding="utf-8") as archivo:
        contenido = archivo.read()  # Leer todo el contenido
        print(Fore.CYAN +contenido)  # Mostrar el contenido
    print(Fore.WHITE)
    opcion = input("Antes de continuar necesitas una cuenta de spotify y registrarte en spotify for developers.\n ¿Desea continuar?[y/n]: ").strip().lower()
    match opcion:
        case "y":
            instalar_paquetes()
        case "n":
            print(Fore.CYAN+"Saliendo...")
            sys.exit()
        case _:
            print(Fore.RED+"Opción no válida.")
            sys.exit()


if __name__ == "__main__":
    main()
