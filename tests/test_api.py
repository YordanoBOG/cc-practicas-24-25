import pytest
import requests

from modules.baseobjects import Workflow

WORKFLOW = Workflow() # Usaremos una variable global WORKFLOW para algunos tests

def test_crearworkflow():
    response = requests.get("http://localhost:8000/crearworkflow")
    assert response.status_code == 200
    assert response.json()["tareas"] == []
    assert response.json()["returned value"] == -1
    assert response.json()["results file"] == "./workflow_results.txt"

def test_crearworkflowparametros():
    response = requests.post("http://localhost:8000/crearworkflowparametros", json={"returned_value": 0})
    assert response.status_code == 200
    assert response.json()["returned value"] == 0

def test_aniadirtareaisolatecolumn():
    response = requests.post("http://localhost:8000/crearworkflowparametros", json={"workflow": WORKFLOW, "csv_path": "./BVBRC_slatt_protein_small.csv", "col_name": "BRC ID"})
    assert response.status_code == 200
    assert response.json()["tareas"] == WORKFLOW.get_parameters['tasks'] # La API modifica el workflow, por lo que comprobamos si su estado ha cambiado

'''def test_funcionalidad2():
    response = requests.post("http://localhost:8000/funcionalidad2", json={"parametro1": "valor"})
    assert response.status_code == 200
    assert response.json() == {"resultado": "Funcionalidad2 ejecutada con valor"}'''

