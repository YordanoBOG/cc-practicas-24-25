import logging
import pytest

import requests

# Configuración de logging
logging.basicConfig(level=logging.INFO,  # Nivel mínimo para registrar (DEBUG, INFO, WARNING, ERROR, CRITICAL)
                    format='%(asctime)s - %(levelname)s - %(message)s',  # Formato del log
                    handlers=[
                        logging.FileHandler("app.log"),  # Guardar logs en un archivo
                        logging.StreamHandler()          # Mostrar logs en la consola
                    ])

#WORKFLOW = Workflow() # Usaremos una variable global WORKFLOW para algunos tests

def test_crearworkflow():
    logging.info("Llamada a /crearworkflow")
    response = requests.get("http://localhost:8000/crearworkflow")
    logging.info(f"Respuesta recibida: {str(response)}")
    assert response.status_code == 200
    assert response.json() == {"tareas": [],
                               "returned value": -1,
                               "results file": "./workflow_results.txt"}

def test_crearworkflowparametros():
    response = requests.post("http://localhost:8000/crearworkflowparametros", json={"returned_value": 0})
    assert response.status_code == 200
    assert response.json() == {"Respuesta": "OK"}
    '''assert response.json() == {"tareas": [],
                               "returned value": "0",
                               "results file": "./workflow_results.txt"}'''

'''def test_funcionalidad2():
    response = requests.post("http://localhost:8000/funcionalidad2", json={"parametro1": "valor"})
    assert response.status_code == 200
    assert response.json() == {"resultado": "Funcionalidad2 ejecutada con valor"}'''

