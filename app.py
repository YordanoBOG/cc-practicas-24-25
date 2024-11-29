import logging

from app import app  # Import the Flask app from the `app/app.py` file

# Configuración de logging
logging.basicConfig(level=logging.INFO,  # Nivel mínimo para registrar (DEBUG, INFO, WARNING, ERROR, CRITICAL)
                    format='%(asctime)s - %(levelname)s - %(message)s',  # Formato del log
                    handlers=[
                        logging.FileHandler("app.log"),  # Guardar logs en un archivo
                        logging.StreamHandler()          # Mostrar logs en la consola
                    ])

if __name__ == "__main__":
    app.logger.info("Lanzando la API de GeneSys")
    app.run(debug=True, host='0.0.0.0', port=8000)