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

# Probar a descargar un documento de la base de datos
def test_download_file():
    filename = "BVBRC_slatt_protein_small.csv"
    download_response = requests.get(f"http://localhost:8000/download/{filename}")
    assert download_response.status_code == 200
    assert download_response.headers["Content-Disposition"] == f"attachment; filename={filename}"
    print(download_response.content)

# Consultar base de datos
def test_list_files():
    list_response = requests.get("http://localhost:8000/consultdb")
    assert list_response.status_code == 200
    response_json = list_response.json()
    assert response_json.get("Files in database") == 1
    
    # Subir y validar varios archivos de una vez
    '''files_to_upload = {
        "file1.csv": b"file1,content,for,test\n1,2,3,4\n",
        "file2.csv": b"file2,more,content\n5,6,7,8\n"
    }
    
    for filename, content in files_to_upload.items():
        with open(filename, "wb") as file:
            file.write(content)
        
        with open(filename, "rb") as file:
            upload_response = requests.post(
                "http://localhost:8000/upload",
                files={"file": file}
            )
        assert upload_response.status_code == 200
        assert "File stored with ID" in upload_response.json().get("message", "")
    
    assert list_response.status_code == 200
    response_json = list_response.json()
    assert response_json.get("Files in database") == len(files_to_upload)
    
    for idx, filename in enumerate(files_to_upload.keys(), start=1):
        assert response_json.get(f"File {idx}") == filename'''

# Otros tests

# Borrar archivos de la base de datos
def test_delete_file():
    filename = "test_delete_file.csv"
    #file_content = b"delete,test,file,content\n123,456,789,0\n"
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

    # Step 2: Delete the file
    delete_response = requests.delete(f"http://localhost:8000/delete/{filename}")
    
    # Step 3: Validate the response
    assert delete_response.status_code == 200
    delete_message = delete_response.json().get("message", "")
    assert delete_message == f"File {filename} deleted successfully"

    # Step 4: Verify the file no longer exists by attempting to download it
    download_response = requests.get(f"http://localhost:8000/download/{filename}")
    assert download_response.status_code == 404
    assert download_response.json().get("error", "") == "File not found"

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
