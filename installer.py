import subprocess
import sys
import os
import platform

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

# Instalacion en Android con Termux:
actualizar terminal:
```
    pkg update -y && pkg upgrade -y
```
instalar python:
```
    pkg install python -y
```
Instalar GIT:
```
    pkg install git -y
```
dar permisos de almacenamiento:
```
    termux-setup-storage
```
Moverse a la siguiente ruta del almacenamiento:
```
    cd storage/shared/
```
crea una carpeta nueva
```
    mkdir NombreCarpeta
```
ingresa a la carpeta y clonar el repositorio:
```
    git clone https://github.com/Jorge-Marco5/SpotDownloader.git
```
ingresar a SpotDownloader y ejecutar el instalador:
```
    cd SpotDownloader && python installer.py
```
Terminando la instalacion inicia el programa:
```
    python main.py
```

IMPORTANTE:
En caso de obtener un error al momento de obtener los metadatos de la cancion, descarga el paquete ffmpeg
apt install ffmpeg -y

moverse entre carpetas en la terminal:
para retroceder una carpeta   cd ..
para ingresar a una carpeta cd NombreCarpeta
"""

#termux-setup-storage
#cd storage/shared/carpeta/SpotDownloader
#python main.py

#Clase para la instalacion de paquetes
class PackageInstaller():
    def __init__(self, requirements_file = "requirements.txt"):
        self.requirements_file = requirements_file
    #instalar dependencias del sistema
    def install_system_dependences(self):
        print("\nIniciando descarga de los paquetes. Esto puede tomar tiempo...\n")
        
        system = platform.system()
        if "com.termux" in os.environ.get("PREFIX", ""):
            print("Instalando 'python' y 'ffmpeg' en Termux...")
            try:
                subprocess.check_call(['pkg', 'update', '-y'])
                subprocess.check_call(['pkg', 'install', 'python', 'ffmpeg', '-y'])
            except Exception as e:
                print(f"Error instalando dependencias en Termux, intente manualmente: {e}")
        elif system == "Linux":
            print("Instalando 'python3', 'build-essential' y 'ffmpeg' en Linux...")
            try:
                subprocess.check_call(['sudo', 'apt', 'update', '-y'])
                subprocess.check_call(['sudo', 'apt', 'install', 'ffmpeg', '-y'])
            except Exception as e:
                print(f"Error instalando dependencias del sistema, intente manualmente: {e}")
        elif system == "windows":
            print("En windows puede ser que necesites instalar ffmpeg manualmente")

    #instalar paquetes de python
    def install_python_packages(self):
        packagesNotInstaller = []
        try:
            print("Instalando paquetes pip...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip', 'setuptools', 'wheel'])

            with open(self.requirements_file, "r") as req_file:
                packages = [line.strip() for line in req_file if line.strip() and not line.startswith("#")]
            for pkg in packages:
                try:
                    subprocess.check_call([sys.executable, '-m', 'pip', 'install', pkg])
                    print("¡Todos los paquetes han sido instalados correctamente!")
                except subprocess.CalledProcessError:
                    print(f"No se pudo instalar el paquete: {pkg}")
                    packagesNotInstaller.append(pkg)
            if packagesNotInstaller:
                print("No se instalaron los siguientes paquetes, intente manualmente:")
                for pkg in packagesNotInstaller:
                    print(f"- {pkg}")
        except Exception as e:
            print("Algunos paquetes puedieron no haberse instalado correctamente")

    #creacion del folder que contiene la musica
    def create_music_folder(self):
        try:
            if not os.path.exists("music"):
                os.mkdir("music")
        except PermissionError:
            print("\nNo se tienen los permisos necesarios para crear la carpeta 'music' en esta ubicacion")
            print("prueba creando el folder maualmente\n")
        except Exception as e:
            print(f"Error al crear la carpeta 'music': "+ e)
    #ejecucion de las clases
    def run(self):
        self.install_system_dependences()
        self.install_python_packages()
        self.create_music_folder()
        print("Ejecuta el comando 'python main.py' para empezar a descargar tu musica")

class EnvCreator:
    def __init__(self, filename = ".env"):
        self.filename = filename

    def create(self, variables = None):
        print("\n___________________________________")
        print("Creando archivo de configuración...(.env)\n")
        print("Si no tienes una cuenta de spotify, puedes crear una en https://www.spotify.com/signup/")
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
            with open(self.filename, "w") as archivo:
                for clave, valor in variables.items():
                    archivo.write(f"{clave}={valor}\n")
            print(f"\nArchivo '{self.filename}' creado exitosamente.\n")
        except Exception as e:
            print(f"\nError al crear el archivo: {e}\n")


def mostrar_requisitos(requirements_file = "requirements.txt"):
    print("Este script instalará los siguientes paquetes necesarios y configuraciones para ejecutar el proyecto en "+platform.system()+".\n")
    with open(requirements_file, "r", encoding="utf-8") as archivo:
        print(archivo.read())  # Mostrar el contenido

def main():
    print("\nBienvenido al instalador de paquetes de SpotDownloader\n")
    print("Sistema Operativo: "+platform.system()+"\n")
    print("DESCARGO DE RESPONSABILIDAD:")
    print("Recuerda que preferiblemente descargues audios y videos que te pertenezcan o a los que tengas permiso.")
    print("Eres libre de hacer lo que gustes, el uso de este script es bajo TU RESPONSABILIDAD\n")
    print("Si tienes problemas con la instalación, asegúrate de tener pip instalado y actualizado.")
    print("'apt install python3 build-essential' ó 'pip install build-essential'\n")
    #mostrar los paquetes a instalar de requirements.txt
    mostrar_requisitos()

    opcion = input("\nAntes de continuar necesitas una cuenta de spotify y registrarte en spotify for developers.\n ¿Desea continuar?[y/n]: ").strip().lower()
    if opcion == "y":
        EnvCreator().create()#creacion de archivo de variables de entorno
        try:
            PackageInstaller().run()#Instalador de paquetes
        except FileNotFoundError:
            print("Error. No se encontro el archivo 'requirements.txt'")
        except subprocess.CalledProcessError as e:
            print("Error durante la instalacion de paquetes")
        except Exception as e:
            print(f"Ha ocurrido un error inesperado"+e)
    elif opcion == "n":
        print("\nSaliendo...")
        sys.exit()
    else:
        print("\nOpción no válida.")
        sys.exit()

if __name__ == "__main__":
    main()
