import logging

from flask import Flask, request, jsonify
from pymongo import MongoClient
from gridfs import GridFS

from api.modules.PATRIC_protein_processing.isolate_column import IsolateColumn
from api.modules.PATRIC_protein_processing.generate_fasta import GenerateFasta
from api.modules.PATRIC_protein_processing.reduce_sample import ReduceSample
from api.modules.PATRIC_protein_processing.get_30kb_upanddown import Get30KbProteins
from api.modules.PATRIC_protein_processing.get_codons_from_features import GetCodonsFromFeatures
from api.modules.baseobjects import Workflow

###############################################################################
###############################################################################
###############################################################################

app = Flask(__name__)
WORKFLOW:Workflow = Workflow() # Un workflow único para todo el servicio

###############################################################################
###############################################################################
###############################################################################

# MongoDB client setup
client = MongoClient("mongodb://mongo:27017/") # La ruta del contenedor mongo (al app solo funcionará desplegada en el contenedor a partir de ahora)
db = client['mydb']
fs = GridFS(db)

# Configuración de logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("app.log"),  # Guardar logs en un archivo
                        logging.StreamHandler()          # Mostrar logs en la consola
                    ])

###############################################################################
###############################################################################
###############################################################################
# Ejemplo: $curl -F "file=@./BVBRC_slatt_protein_small.csv" http://localhost:8000/upload
@app.route('/upload', methods=['POST'])
def upload_file():
    """Endpoint to upload a file to MongoDB."""
    file = request.files['file']
    file_id = fs.put(file, filename=file.filename)
    app.logger.info(f"File {file.filename} stored with ID {file_id}")
    return jsonify({"message": f"File stored with ID {file_id}"})

###############################################################################
###############################################################################
###############################################################################
# Ejemplo: $curl -O http://localhost:8000/download/BVBRC_slatt_protein_small.csv
@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    """Endpoint to download a file from MongoDB."""
    file = fs.find_one({"filename": filename})
    if not file:
        app.logger.error(f"File {filename} not found in MongoDB.")
        return jsonify({"error": "File not found"}), 404
    response = app.response_class(file.read(), mimetype='application/octet-stream')
    response.headers.set('Content-Disposition', f'attachment; filename={filename}')
    app.logger.info(f"File {filename} downloaded from MongoDB.")
    return response

###############################################################################
###############################################################################
###############################################################################
# Ejemplo: $curl -X DELETE http://localhost:8000/delete/BVBRC_slatt_protein_small.csv
@app.route('/delete/<filename>', methods=['DELETE'])
def delete_file(filename):
    """Endpoint to delete a file from MongoDB."""
    files = fs.find({"filename": filename})
    if not files:
        app.logger.error(f"File {filename} not found in MongoDB.")
        return jsonify({"error": "File not found"}), 404
    for file in files:
        fs.delete(file._id)
        app.logger.info(f"File {filename} deleted from MongoDB.")
    return jsonify({"message": f"File {filename} deleted successfully"})

###############################################################################
###############################################################################
###############################################################################
# Ejemplo: $curl -X GET http://localhost:8000/consultdb
@app.route('/consultdb', methods=['GET'])
def list_files():
    """Endpoint to consult all the alocated file in the database"""
    result_dict = {}
    files = [file.filename for file in fs.find()] # Retrieve and print all filenames in MongoDB GridFS
    if not files:
        result_dict['message'] = 'There are no data in the database'
    else:
        result_dict['Files in database'] = len(files)
        count = 0
        for filename in files:
            count += 1
            result_dict[f'File {count}'] = str(filename)
    app.logger.info("All the stored data of the database were recovered")
    return jsonify(result_dict)

###############################################################################
###############################################################################
###############################################################################
# Ejemplo: $curl -X GET http://localhost:8000/crearworkflow
@app.route('/crearworkflow', methods=['GET'])
def crear_workflow():
    app.logger.info("Llamada a /crearworkflow")
    default_workflow = Workflow()
    WORKFLOW.set_parameters(default_workflow.get_parameters())
    workflow_new_parameters = WORKFLOW.get_parameters()
    return jsonify({"tareas": workflow_new_parameters['tasks'],
                    "returned value": workflow_new_parameters['returned_value'],
                    "results file": workflow_new_parameters['results_file'],
                    "containerized": workflow_new_parameters['containerized']})

###############################################################################
###############################################################################
###############################################################################
''' Ejemplo: $curl -X POST http://localhost:8000/crearworkflowparametros -H "Content-Type: application/json" \
-d '{"tasks": [], "results_file": "workflow_res.txt", "returned_value": 0, "containerized": true}' '''
@app.route('/crearworkflowparametros', methods=['POST'])
def crear_workflow_parametros():
    app.logger.info("Llamada a /crearworkflowparametros")
    parametros = request.get_json()

    # Comprobar si los parámetros incluyen una lista de tareas, un valor de salida y un fichero de resultados
    if "tasks" not in parametros:
        parametros['tasks'] = []
    if "results_file" not in parametros:
        parametros['results_file'] = "workflow_results.txt"
    if "returned_value" not in parametros:
        parametros['returned_value'] = -1
    if "returned_info" not in parametros:
        parametros['returned_info'] = ""
    if "containerized" not in parametros:
        parametros['containerized'] = False

    WORKFLOW.set_parameters(parameters=parametros)
    new_workflow_parameters = WORKFLOW.get_parameters()
    app.logger.info(f"WORKFLOW CREADO: {str(new_workflow_parameters)}")
    print(f"WORKFLOW CREADO: {str(new_workflow_parameters)}")
    return jsonify({"tareas": new_workflow_parameters['tasks'],
                    "returned value": new_workflow_parameters['returned_value'],
                    "results file": new_workflow_parameters['results_file'],
                    "containerized": new_workflow_parameters['containerized']})

###############################################################################
###############################################################################
###############################################################################
''' Ejemplo: $curl -X POST http://localhost:8000/aniadirtareaisolatecolumn -H "Content-Type: application/json" \
-d '{"containerized": true, "csv_path": "BVBRC_slatt_protein_small.csv", "col_name": "BRC ID"}' '''
@app.route('/aniadirtareaisolatecolumn', methods=['POST'])
def aniadir_tarea_isolate_column():
    app.logger.info("Llamada a /aniadirtareaisolatecolumn")
    parametros = request.get_json()
    isolate_column_task = IsolateColumn(containerized=parametros['containerized'], csv_path=parametros['csv_path'], col_name=parametros['col_name'])
    WORKFLOW.add_task(isolate_column_task)
    # Devolver la información de la última tarea añadida al workflow para confirmar que se ha añadido la que hemos creado
    return jsonify({"nueva tarea": WORKFLOW.get_tasks()[-1].to_dict()})

###############################################################################
###############################################################################
###############################################################################
''' Ejemplo: $curl -X POST http://localhost:8000/aniadirtareageneratefasta -H "Content-Type: application/json" \
-d '{"containerized": true, "path_to_protein_codes_csv": "BVBRC_slatt_protein_small_new.csv", "fasta_folder_path": "samples.fasta"}' '''
@app.route('/aniadirtareageneratefasta', methods=['POST'])
def aniadir_tarea_gen_fasta():
    app.logger.info("Llamada a /aniadirtareageneratefasta")
    parametros = request.get_json()
    generate_fasta_task = GenerateFasta(containerized=parametros['containerized'], path_to_protein_codes_csv=parametros['path_to_protein_codes_csv'], fasta_folder_path=parametros['fasta_folder_path'])
    WORKFLOW.add_task(generate_fasta_task)
    # Devolver la información de la última tarea añadida al workflow para confirmar que se ha añadido la que hemos creado
    return jsonify({"nueva tarea": WORKFLOW.get_tasks()[-1].to_dict()})

###############################################################################
###############################################################################
###############################################################################
''' Ejemplo: $curl -X POST http://localhost:8000/aniadirtareaisolatecolumn -H "Content-Type: application/json" \
-d '{"containerized": true, "fasta_pathname": "samples.fasta", "pathname_to_reduced_proteins": "reduced_samples.fasta"}' '''
@app.route('/aniadirtareareducesample', methods=['POST'])
def aniadir_tarea_reduce_sample():
    app.logger.info("Llamada a /aniadirtareareducesample")
    parametros = request.get_json()
    reduce_sample_task = ReduceSample(containerized=parametros['containerized'], fasta_pathname=parametros['fasta_pathname'], pathname_to_reduced_proteins=parametros['pathname_to_reduced_proteins'])
    WORKFLOW.add_task(reduce_sample_task)
    # Devolver la información de la última tarea añadida al workflow para confirmar que se ha añadido la que hemos creado
    return jsonify({"nueva tarea": WORKFLOW.get_tasks()[-1].to_dict()})

###############################################################################
###############################################################################
###############################################################################
''' Ejemplo: $curl -X POST http://localhost:8000/aniadirtareaisolatecolumn -H "Content-Type: application/json" \
-d '{"containerized": true, "pathname_to_reduced_proteins": "reduced_samples.fasta", "pathname_to_feature_proteins": "feature_regions.fasta"}' '''
@app.route('/aniadirtareaget30kb', methods=['POST'])
def aniadir_tarea_get_30kb():
    app.logger.info("Llamada a /aniadirtareaget30kb")
    parametros = request.get_json()
    get_30_kb_task = Get30KbProteins(containerized=parametros['containerized'], pathname_to_reduced_proteins=parametros['pathname_to_reduced_proteins'], pathname_to_feature_proteins=parametros['pathname_to_feature_proteins'])
    WORKFLOW.add_task(get_30_kb_task)
    # Devolver la información de la última tarea añadida al workflow para confirmar que se ha añadido la que hemos creado
    return jsonify({"nueva tarea": WORKFLOW.get_tasks()[-1].to_dict()})

###############################################################################
###############################################################################
###############################################################################
''' Ejemplo: $curl -X POST http://localhost:8000/aniadirtareaisolatecolumn -H "Content-Type: application/json" \
-d '{"containerized": true, "pathname_to_feature_proteins": "feature_regions.fasta", "pathname_to_excel_results": "final_results.xlsx"}' '''
@app.route('/aniadirtareareconocercodones', methods=['POST'])
def aniadir_tarea_recognize_codons():
    app.logger.info("Llamada a /aniadirtareareconocercodones")
    parametros = request.get_json()
    recognize_codons_task = GetCodonsFromFeatures(containerized=parametros['containerized'], pathname_to_feature_proteins=parametros['pathname_to_feature_proteins'], pathname_to_excel_results=parametros['pathname_to_excel_results'])
    WORKFLOW.add_task(recognize_codons_task)
    # Devolver la información de la última tarea añadida al workflow para confirmar que se ha añadido la que hemos creado
    return jsonify({"nueva tarea": WORKFLOW.get_tasks()[-1].to_dict()})

###############################################################################
###############################################################################
###############################################################################
# Ejemplo: $curl -X GET http://localhost:8000/eliminarultimatareaworkflow
@app.route('/eliminarultimatareaworkflow', methods=['GET'])
def eliminar_ultima_tarea():
    app.logger.info("Llamada a /eliminarultimatareaworkflow")
    result = WORKFLOW.remove_last_task()
    return jsonify({"exito": result})

###############################################################################
###############################################################################
###############################################################################
# Ejemplo: $curl -X GET http://localhost:8000/limpiarworkflow
@app.route('/limpiarworkflow', methods=['GET'])
def limpiar_workflow():
    app.logger.info("Llamada a /limpiarworkflow")
    result = WORKFLOW.clean()
    return jsonify({"exito": result})

###############################################################################
###############################################################################
###############################################################################
''' Ejemplo: $curl -X POST http://localhost:8000/guardarworkflowcomojson -H "Content-Type: application/json" \
-d '{"archivo_json": "workflow_api.json"}' '''
@app.route('/guardarworkflowcomojson', methods=['POST'])
def guardar_workflow_como_json():
    app.logger.info("Llamada a /guardarworkflowcomojson")
    parametros = request.get_json()
    ruta_json = parametros['archivo_json']
    result = WORKFLOW.generate_json(path=ruta_json)
    return jsonify({"exito": result})

###############################################################################
###############################################################################
###############################################################################
''' Ejemplo: $curl -X POST http://localhost:8000/cargarworkflowdesdejson -H "Content-Type: application/json" \
-d '{"containerized": true, "archivo_json": "workflow_api.json"}' '''
@app.route('/cargarworkflowdesdejson', methods=['POST'])
def cargar_workflow_desde_json():
    app.logger.info("Llamada a /cargarworkflowdesdejson")
    parametros = request.get_json()
    contenedor = parametros['containerized']
    ruta_json = parametros['archivo_json']
    result = WORKFLOW.get_from_json(containerized=contenedor, json_path=ruta_json)
    if result == 0:
        return jsonify({"num_tareas": WORKFLOW.get_len_workflow()})
    else:
        return jsonify({"num_tareas": -1})

###############################################################################
###############################################################################
###############################################################################
# Ejemplo: $curl -X GET http://localhost:8000/ejecutarworkflow
@app.route('/ejecutarworkflow', methods=['GET'])
def ejecutar_workflow():
    app.logger.info("Llamada a /ejecutarworkflow")
    WORKFLOW.run() # Aquí vas a tener que pasar la conexión a la base de datos como parámetro y
                   # actuar sobre ella. Se asume que ahora el fichero inicial está en la BD (se ha metido manualmente)
                   # Y debes hacer que el workflow manipule archivos dentro de la BD al ejecutarse, tarea a tarea.
                   # Revisa que no se usen archivos de la BD en ninguna otra tarea de la aplicación
    return jsonify({"returned value": WORKFLOW.get_parameters()['returned_value']})

###############################################################################
###############################################################################
###############################################################################
# Ejemplo: $curl -X GET http://localhost:8000/showinfo
@app.route('/showinfo', methods=['GET'])
def show_info_workflow():
    app.logger.info("Llamada a /showinfo")
    return jsonify({"workflow info": WORKFLOW.to_dict()})

###############################################################################
###############################################################################
###############################################################################

if __name__ == "__main__":
    app.logger.info("Lanzando la API de GeneSys")
    app.run(debug=True, host='0.0.0.0', port=8000)
