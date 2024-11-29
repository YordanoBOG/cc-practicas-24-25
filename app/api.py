import json
import logging
from flask import Flask, request, jsonify
from app import app  # Import the app instance from `app/__init__.py`

from modules.PATRIC_protein_processing.isolate_column import IsolateColumn
from modules.PATRIC_protein_processing.generate_fasta import GenerateFasta
from modules.PATRIC_protein_processing.reduce_sample import ReduceSample
from modules.PATRIC_protein_processing.get_30kb_upanddown import Get30KbProteins
from modules.PATRIC_protein_processing.get_codons_from_features import GetCodonsFromFeatures
from modules.baseobjects import Workflow

# Configuración de logging
logging.basicConfig(level=logging.INFO,  # Nivel mínimo para registrar (DEBUG, INFO, WARNING, ERROR, CRITICAL)
                    format='%(asctime)s - %(levelname)s - %(message)s',  # Formato del log
                    handlers=[
                        logging.FileHandler("app.log"),  # Guardar logs en un archivo
                        logging.StreamHandler()          # Mostrar logs en la consola
                    ])

###############################################################################
###############################################################################
###############################################################################

@app.route('/crearworkflow', methods=['GET'])
def crear_workflow():
    app.logger.info("Llamada a /crearworkflow")
    new_workflow = Workflow()
    new_workflow_parameters = new_workflow.get_parameters()
    return jsonify({"tareas": new_workflow_parameters['tasks'],
                    "returned value": new_workflow_parameters['returned_value'],
                    "results file": new_workflow_parameters['results_file']})

###############################################################################
###############################################################################
###############################################################################

@app.route('/crearworkflowparametros', methods=['POST'])
def crear_workflow_parametros():
    app.logger.info("Llamada a /crearworkflowparametros")
    parametros = request.get_json()

    # Comprobar si los parámetros incluyen una lista de tareas, un valor de salida y un fichero de resultados
    if "tasks" not in parametros:
        parametros['tasks'] = []
    if "results_file" not in parametros:
        parametros['results_file'] = "./workflow_results.txt"
    if "returned_value" not in parametros:
        parametros['returned_value'] = -1
    if "returned_info" not in parametros:
        parametros['returned_info'] = ""

    new_workflow = Workflow()
    new_workflow.set_parameters(parameters=parametros)
    new_workflow_parameters = new_workflow.get_parameters()
    return jsonify({"tareas": new_workflow_parameters['tasks'],
                    "returned value": new_workflow_parameters['returned_value'],
                    "results file": new_workflow_parameters['results_file'],
                    "returned info": new_workflow_parameters['returned_info']})

###############################################################################
###############################################################################
###############################################################################

@app.route('/aniadirtareaisolatecolumn', methods=['POST'])
def aniadir_tarea_isolate_column():
    app.logger.info("Llamada a /aniadirtareaisolatecolumn")
    parametros = request.get_json()
    current_workflow:Workflow = parametros['workflow']
    isolate_column_task = IsolateColumn(csv_path=parametros['csv_path'], col_name=parametros['col_name'])
    current_workflow.add_task(isolate_column_task)
    workflow_parameters = current_workflow.get_parameters()
    return jsonify({"tareas": workflow_parameters['tasks']})

###############################################################################
###############################################################################
###############################################################################

@app.route('/eliminarultimatarea', methods=['POST'])
def eliminar_ultima_tarea():
    parametros = request.get_json()
    current_workflow:Workflow = parametros['workflow']
    current_workflow.remove_last_task()
    workflow_parameters = current_workflow.get_parameters()
    return jsonify({"tareas": workflow_parameters['tasks']})

###############################################################################
###############################################################################
###############################################################################

@app.route('/limpiarworkflow', methods=['POST'])
def limpiar_workflow():
    parametros = request.get_json()
    current_workflow:Workflow = parametros['workflow']
    current_workflow.clean()
    workflow_parameters = current_workflow.get_parameters()
    return jsonify({"tareas": workflow_parameters['tasks']})

###############################################################################
###############################################################################
###############################################################################



###############################################################################
###############################################################################
###############################################################################

