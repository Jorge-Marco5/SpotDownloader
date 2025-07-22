from flask import Flask

app = Flask(__name__)

from app import routes  # importa las rutas al inicializar la app

