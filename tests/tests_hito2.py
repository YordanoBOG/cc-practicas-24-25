#import pytest

from modules.PATRIC_protein_processing.isolate_column import IsolateColumn 
from modules.PATRIC_protein_processing.generate_fasta import GenerateFasta
from modules.PATRIC_protein_processing.reduce_sample import ReduceSample
from modules.PATRIC_protein_processing.get_30kb_upanddown import Get30KbProteins
from modules.PATRIC_protein_processing.get_codons_from_features import GetCodonsFromFeatures
from modules.baseobjects import Task, Workflow

workflow = Workflow()

# assert statements: Each test uses an assert statement to check that the result of add()
# matches the expected output. If the assertion fails, pytest will raise an error, marking
# the test as failed.
def test_crear_workflow(): # Crear workflow con valores por defecto, se comprueban los valores por defecto
    assert len(workflow.get_tasks())==0 and workflow.get_parameters['results_file']=="./workflow_results.txt"

def test_aniadir_tarea_leer_csv():
    leer_csv = IsolateColumn(csv_path="./BVBRC_slatt_protein_small.csv",
                             col_name="BRC ID")
    workflow.add_task(leer_csv)
    assert len(workflow.get_tasks())==1

def test_aniadir_tarea_generar_fasta():
    generar_fasta = GenerateFasta(path_to_protein_codes_csv="./BVBRC_slatt_protein_small_new.csv",
                             fasta_folder_path="./proteins.fasta")
    workflow.add_task(generar_fasta)
    assert len(workflow.get_tasks())==2

def test_aniadir_tarea_reducir_muestra():
    reducir_muestra = ReduceSample(fasta_pathname="./proteins.fasta",
                             pathname_to_reduced_proteins="./reduced_proteins.fasta",
                             percentage=60)
    workflow.add_task(reducir_muestra)
    assert len(workflow.get_tasks())==3

def test_aniadir_tarea_obtener_30kb_aminoacidos():
    obtener_aminoacidos = Get30KbProteins(pathname_to_reduced_proteins="./reduced_proteins.fasta",
                             pathname_to_feature_proteins="./feature_regions.fasta")
    workflow.add_task(obtener_aminoacidos)
    assert len(workflow.get_tasks())==4

def test_aniadir_tarea_reconocer_codones():
    reconocer_codones = GetCodonsFromFeatures(pathname_to_feature_proteins="./feature_regions.fasta",
                             pathname_to_excel_results="./final_results.xlsx")
    workflow.add_task(reconocer_codones)
    assert len(workflow.get_tasks())==5

def test_guardar_workflow():
    workflow.generate_json("./workflow.json")
    assert True

def test_limpiar_workflow():
    workflow.clean()
    assert len(workflow.get_tasks())==0

def test_cargar_workflow():
    workflow.get_from_json("./workflow.json")
    assert len(workflow.get_tasks())==5

def test_ejecutar_workflow():
    workflow.run()
    assert workflow.get_returned_value()==0
    