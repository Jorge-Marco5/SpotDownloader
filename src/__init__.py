from flask import Flask
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

from src import routes  # importa las rutas al inicializar la app

