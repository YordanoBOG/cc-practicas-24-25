import pytest
import requests

#from api.modules.baseobjects import Workflow

def test_crearworkflow():
    response = requests.get("http://localhost:8000/crearworkflow")
    assert response.status_code == 200
    assert response.json()["tareas"] == []
    assert response.json()["returned value"] == -1
    assert response.json()["results file"] == "workflow_results.txt"

def test_crearworkflowparametros():
    response = requests.post("http://localhost:8000/crearworkflowparametros", json={"containerized": False, "returned_value": 0})
    assert response.status_code == 200
    assert response.json()["returned value"] == 0
    assert response.json()["containerized"] == False

def test_aniadirtareaisolatecolumn():
    response = requests.post("http://localhost:8000/aniadirtareaisolatecolumn", json={"containerized": False, "csv_path": "BVBRC_slatt_protein_small.csv", "col_name": "BRC ID"})
    assert response.status_code == 200
    assert response.json()["nueva tarea"]['type'] == 'api.modules.PATRIC_protein_processing.isolate_column.IsolateColumn'

def test_aniadirtareageneratefasta():
    response = requests.post("http://localhost:8000/aniadirtareageneratefasta", json={"containerized": False, "path_to_protein_codes_csv": "BVBRC_slatt_protein_small_new.csv", "fasta_folder_path": "proteins.fasta"})
    assert response.status_code == 200
    assert response.json()["nueva tarea"]['type'] == 'api.modules.PATRIC_protein_processing.generate_fasta.GenerateFasta'

def test_aniadirtareareducesample():
    response = requests.post("http://localhost:8000/aniadirtareareducesample", json={"containerized": False, "fasta_pathname": "proteins.fasta", "pathname_to_reduced_proteins": "reduced_proteins.fasta", "percentage": 85})
    assert response.status_code == 200
    assert response.json()["nueva tarea"]['type'] == 'api.modules.PATRIC_protein_processing.reduce_sample.ReduceSample'

def test_guardarworkflowcomojson():
    response = requests.post("http://localhost:8000/guardarworkflowcomojson", json={"archivo_json": "workflow.json"})
    assert response.status_code == 200
    assert response.json()["exito"] == 0

def test_eliminarultimatareaworkflow():
    response = requests.get("http://localhost:8000/eliminarultimatareaworkflow")
    assert response.status_code == 200
    assert response.json()["exito"] == 0

def test_limpiarworkflow():
    response = requests.get("http://localhost:8000/limpiarworkflow")
    assert response.status_code == 200
    assert response.json()["exito"] == 0

def test_cargarworkflowdesdejson():
    response = requests.post("http://localhost:8000/cargarworkflowdesdejson", json={"containerized": False, "archivo_json": "workflow.json"})
    assert response.status_code == 200
    assert response.json()["num_tareas"] == 3

def test_ejecutarworkflow():
    response = requests.get("http://localhost:8000/ejecutarworkflow")
    assert response.status_code == 200
    assert response.json()["returned value"] == 0

