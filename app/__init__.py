from flask import Flask

app = Flask(__name__)

# Import routes (important: import after creating `app` to avoid circular imports)
from api import crearworkflow