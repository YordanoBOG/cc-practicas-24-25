import pytest

from api.modules.PATRIC_protein_processing.isolate_column import IsolateColumn 
from api.modules.PATRIC_protein_processing.generate_fasta import GenerateFasta
from api.modules.PATRIC_protein_processing.reduce_sample import ReduceSample
from api.modules.PATRIC_protein_processing.get_30kb_upanddown import Get30KbProteins
from api.modules.PATRIC_protein_processing.get_codons_from_features import GetCodonsFromFeatures
from api.modules.baseobjects import Workflow

WORKFLOW = Workflow() # Usamos una variable global WORKFLOW

# assert statements: Each test uses an assert statement to check that the result of add()
# matches the expected output. If the assertion fails, pytest will raise an error, marking
# the test as failed.
def test_crear_workflow(): # Comprobar los valores por defecto del flujo de trabajo
    assert len(WORKFLOW.get_tasks())==0 and WORKFLOW.get_parameters()['results_file']=="workflow_results.txt"

def test_aniadir_tareas():
    leer_csv = IsolateColumn(containerized=False, csv_path="BVBRC_slatt_protein_small.csv", col_name="BRC ID")
    generar_fasta = GenerateFasta(containerized=False, path_to_protein_codes_csv="BVBRC_slatt_protein_small_new.csv", fasta_folder_path="proteins.fasta")
    reducir_muestra = ReduceSample(containerized=False, fasta_pathname="proteins.fasta", pathname_to_reduced_proteins="reduced_proteins.fasta", percentage=60)
    obtener_aminoacidos = Get30KbProteins(containerized=False, pathname_to_reduced_proteins="reduced_proteins.fasta", pathname_to_feature_proteins="feature_regions.fasta")
    reconocer_codones = GetCodonsFromFeatures(containerized=False, pathname_to_feature_proteins="feature_regions.fasta", pathname_to_excel_results="final_results.xlsx")
    WORKFLOW.add_task(leer_csv)
    WORKFLOW.add_task(generar_fasta)
    WORKFLOW.add_task(reducir_muestra)
    WORKFLOW.add_task(obtener_aminoacidos)
    WORKFLOW.add_task(reconocer_codones)
    assert len(WORKFLOW.get_tasks())==5

def test_guardar_y_borrar_workflow():
    WORKFLOW.generate_json("workflow.json")
    WORKFLOW.clean()
    assert len(WORKFLOW.get_tasks())==0

def test_cargar_workflow():
    WORKFLOW.get_from_json(json_path="workflow.json", containerized=False)
    assert len(WORKFLOW.get_tasks())==5

def test_ejecutar_workflow():
    WORKFLOW.run()
    assert WORKFLOW.get_returned_value()==0
