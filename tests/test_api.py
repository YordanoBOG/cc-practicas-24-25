import pytest

import requests

def test_crearworkflow():
    response = requests.get("http://localhost:8000/crearworkflow")
    assert response.status_code == 200
    assert response.json() == {"resultado": "Workflow"}

'''def test_funcionalidad2():
    response = requests.post("http://localhost:8000/funcionalidad2", json={"parametro1": "valor"})
    assert response.status_code == 200
    assert response.json() == {"resultado": "Funcionalidad2 ejecutada con valor"}'''

