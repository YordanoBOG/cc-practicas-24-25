import pytest

from modules.PATRIC_protein_processing.isolate_column import IsolateColumn 
from modules.PATRIC_protein_processing.generate_fasta import GenerateFasta
from modules.PATRIC_protein_processing.reduce_sample import ReduceSample
from modules.PATRIC_protein_processing.get_30kb_upanddown import Get30KbProteins
from modules.PATRIC_protein_processing.get_codons_from_features import GetCodonsFromFeatures
from modules.baseobjects import Task, Workflow

WORKFLOW = Workflow() # Usamos una variable global WORKFLOW

# assert statements: Each test uses an assert statement to check that the result of add()
# matches the expected output. If the assertion fails, pytest will raise an error, marking
# the test as failed.
def test_crear_workflow(): # Comprobar los valores por defecto del flujo de trabajo
    assert len(WORKFLOW.get_tasks())==0 and WORKFLOW.get_parameters['results_file']=="./workflow_results.txt"

def test_aniadir_tarea_leer_csv():
    #global WORKFLOW # Declarar la variable global dentro de la función para poder modificarla
    leer_csv = IsolateColumn(csv_path="./BVBRC_slatt_protein_small.csv",
                             col_name="BRC ID")
    WORKFLOW.add_task(leer_csv)
    assert len(WORKFLOW.get_tasks())==1

def test_aniadir_tarea_generar_fasta():
    generar_fasta = GenerateFasta(path_to_protein_codes_csv="./BVBRC_slatt_protein_small_new.csv",
                             fasta_folder_path="./proteins.fasta")
    WORKFLOW.add_task(generar_fasta)
    assert len(WORKFLOW.get_tasks())==2

def test_aniadir_tarea_reducir_muestra():
    reducir_muestra = ReduceSample(fasta_pathname="./proteins.fasta",
                             pathname_to_reduced_proteins="./reduced_proteins.fasta",
                             percentage=60)
    WORKFLOW.add_task(reducir_muestra)
    assert len(WORKFLOW.get_tasks())==3

def test_aniadir_tarea_obtener_30kb_aminoacidos():
    obtener_aminoacidos = Get30KbProteins(pathname_to_reduced_proteins="./reduced_proteins.fasta",
                             pathname_to_feature_proteins="./feature_regions.fasta")
    WORKFLOW.add_task(obtener_aminoacidos)
    assert len(WORKFLOW.get_tasks())==4

def test_aniadir_tarea_reconocer_codones():
    reconocer_codones = GetCodonsFromFeatures(pathname_to_feature_proteins="./feature_regions.fasta",
                             pathname_to_excel_results="./final_results.xlsx")
    WORKFLOW.add_task(reconocer_codones)
    assert len(WORKFLOW.get_tasks())==5

def test_guardar_WORKFLOW():
    WORKFLOW.generate_json("./workflow.json")
    assert True

def test_limpiar_WORKFLOW():
    WORKFLOW.clean()
    assert len(WORKFLOW.get_tasks())==0

def test_cargar_WORKFLOW():
    WORKFLOW.get_from_json("./workflow.json")
    assert len(WORKFLOW.get_tasks())==5

def test_ejecutar_WORKFLOW():
    WORKFLOW.run()
    assert WORKFLOW.get_returned_value()==0
