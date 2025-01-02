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
    response = requests.post("http://localhost:8000/crearworkflowparametros", json={"returned_value": 0, "containerized": false})
    assert response.status_code == 200
    assert response.json()["returned value"] == 0
    assert response.json()["containerized"] == False

def test_aniadirtareaisolatecolumn():
    response = requests.post("http://localhost:8000/aniadirtareaisolatecolumn", json={"csv_path": "BVBRC_slatt_protein_small.csv", "col_name": "BRC ID"})
    assert response.status_code == 200
    assert response.json()["nueva tarea"]['type'] == 'api.modules.PATRIC_protein_processing.isolate_column.IsolateColumn'

def test_aniadirtareageneratefasta():
    response = requests.post("http://localhost:8000/aniadirtareageneratefasta", json={"path_to_protein_codes_csv": "BVBRC_slatt_protein_small_new.csv", "fasta_folder_path": "proteins.fasta"})
    assert response.status_code == 200
    assert response.json()["nueva tarea"]['type'] == 'api.modules.PATRIC_protein_processing.generate_fasta.GenerateFasta'

def test_aniadirtareareducesample():
    response = requests.post("http://localhost:8000/aniadirtareareducesample", json={"fasta_pathname": "proteins.fasta", "pathname_to_reduced_proteins": "reduced_proteins.fasta"})
    assert response.status_code == 200
    assert response.json()["nueva tarea"]['type'] == 'api.modules.PATRIC_protein_processing.reduce_sample.ReduceSample'

def test_aniadirtareaget30kb():
    response = requests.post("http://localhost:8000/aniadirtareaget30kb", json={"pathname_to_reduced_proteins": "reduced_proteins.fasta", "pathname_to_feature_proteins": "feature_regions.fasta"})
    assert response.status_code == 200
    assert response.json()["nueva tarea"]['type'] == 'api.modules.PATRIC_protein_processing.get_30kb_upanddown.Get30KbProteins'

def test_aniadirtareareconocercodones():
    response = requests.post("http://localhost:8000/aniadirtareareconocercodones", json={"pathname_to_feature_proteins": "feature_regions.fasta", "pathname_to_excel_results": "final_results.xlsx"})
    assert response.status_code == 200
    assert response.json()["nueva tarea"]['type'] == 'api.modules.PATRIC_protein_processing.get_codons_from_features.GetCodonsFromFeatures'

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
    response = requests.post("http://localhost:8000/cargarworkflowdesdejson", json={"archivo_json": "workflow.json"})
    assert response.status_code == 200
    assert response.json()["num_tareas"] == 5

def test_ejecutarworkflow():
    response = requests.get("http://localhost:8000/ejecutarworkflow")
    assert response.status_code == 200
    assert response.json()["returned value"] == 0

