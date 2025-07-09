import subprocess
import sys

def instalar_paquetes():
    crear_archivo_env()
    try:
        # Verifica si existe el archivo requirements.txt
        with open('requirements.txt', 'r') as file:
            print("Instalando paquetes desde requirements.txt, esto puede tomar un tiempo...")
            # Ejecuta el comando pip para instalar los paquetes
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
            print("¡Todos los paquetes han sido instalados correctamente!")
            print("Ejecuta el comando 'python main.py' para empezar a descargar tu musica")
    except FileNotFoundError:
        print("Error: No se encontró el archivo 'requirements.txt'. Asegúrate de que esté en el directorio actual.")
    except subprocess.CalledProcessError as e:
        print(f"Error durante la instalación de paquetes: {e}")
    except Exception as e:
        print(f"Ha ocurrido un error inesperado: {e}")


def crear_archivo_env(nombre_archivo=".env", variables=None):

    """Creacion del archivo de variables de entorno para la configuracion del proyecto.
    """
    print("\n___________________________________")
    print("Creando archivo de configuración...\n")
    print("Si no tienes una cuenta de spotify, puedes crear una en https://www.spotify.com/signup/")
    print("Si no tienes una cuenta de spotify for developers, puedes crear una en https://developer.spotify.com/dashboard/login\n")
    print("En la pagina de spotify for developers, crea una nueva app y obten tu client_id y client_secret, necesarios para acceder a la api de spotify\n")
    print("Tranquilo..., estos datos se almacenan de manera local, ni el creador del programa tiene conocimiento de ellos.")
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
        print(f"\nArchivo '{nombre_archivo}' creado exitosamente.\n")
    except Exception as e:
        print(f"\nError al crear el archivo: {e}\n")

def main():
    print("\nBienvenido al instalador de paquetes de Spotify Playlist Downloader\n")
    print("DESCARGO DE RESPONSABILIDAD:")
    print("Recuerda que preferiblemente descargues audios y videos que te pertenezcan o a los que tengas permiso.")
    print("Eres libre de hacer lo que gustes, el uso de este script es bajo TU RESPONSABILIDAD\n")
    print("Si tienes problemas con la instalación, asegúrate de tener pip instalado y actualizado.")
    print("Este script instalará todos los paquetes necesarios y configuraciones para ejecutar el proyecto.\n")
    opcion = input("Antes de continuar necesitas una cuenta de spotify y registrarte en spotify for developers.\n ¿Desea continuar?[y/n]: ").strip().lower()
    match opcion:
        case "y":
            instalar_paquetes()
        case "n":
            print("Saliendo...")
            sys.exit()
        case _:
            print("Opción no válida.")
            sys.exit()


if __name__ == "__main__":
    main()
