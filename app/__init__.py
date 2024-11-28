from flask import Flask

app = Flask(__name__)

# Import routes (important: import after creating `app` to avoid circular imports)
from app.api import crearworkflow # Se debe poner la ruta absoluta del entorno de ejecución, que parte del fichero raíz