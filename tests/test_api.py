import pytest

import requests

#WORKFLOW = Workflow() # Usaremos una variable global WORKFLOW para algunos tests

def test_crearworkflow():
    response = requests.get("http://localhost:8000/crearworkflow")
    assert response.status_code == 200
    assert response.json() == {"tareas": [],
                               "returned value": -1,
                               "results file": "./workflow_results.txt"}

def test_crearworkflowparametros():
    response = requests.post("http://localhost:8000/crearworkflowparametros", json={"returned_value": 0})
    assert response.status_code == 200
    assert response.json() == {"tareas": [],
                               "returned value": "0",
                               "results file": "./workflow_results.txt"}

'''def test_funcionalidad2():
    response = requests.post("http://localhost:8000/funcionalidad2", json={"parametro1": "valor"})
    assert response.status_code == 200
    assert response.json() == {"resultado": "Funcionalidad2 ejecutada con valor"}'''

