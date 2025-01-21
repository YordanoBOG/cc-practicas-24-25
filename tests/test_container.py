import pytest
import requests

# Testear endpoint que permite subir un archivo a la base de datos
def test_upload_file():
    with open("BVBRC_slatt_protein_small.csv", "rb") as file:
        response = requests.post(
            "http://localhost:8000/upload",
            files={"file": file}  # Creamos la estructura de datos con la etiqueta "file"
                                  # que se espera recibir en el endpoint.
        )
    assert response.status_code == 200
    assert "File stored with ID" in response.json()["message"]

def test_download_file():
    # Upload a file to ensure it exists in the database
    filename = "BVBRC_slatt_protein_small.csv"
    #file_content = b"sample,data,for,testing\n1,2,3,4\n"
    '''with open(filename, "wb") as file:
        file.write(file_content)
    
    with open(filename, "rb") as file:
        upload_response = requests.post(
            "http://localhost:8000/upload",
            files={"file": file}
        )
    
    assert upload_response.status_code == 200
    upload_message = upload_response.json().get("message", "")
    assert "File stored with ID" in upload_message'''

    # Test the download endpoint
    download_response = requests.get(f"http://localhost:8000/download/{filename}")
    
    # Validate the response
    assert download_response.status_code == 200
    assert download_response.headers["Content-Disposition"] == f"attachment; filename={filename}"
    print(download_response.content)

'''
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
    response = requests.post("http://localhost:8000/aniadirtareareducesample", json={"containerized": False, "fasta_pathname": "proteins.fasta", "pathname_to_reduced_proteins": "reduced_proteins.fasta"})
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
    assert response.json()["returned value"] == 0'''
