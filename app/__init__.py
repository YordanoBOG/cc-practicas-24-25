from flask import Flask

app = Flask(__name__)

# Se debe poner la ruta absoluta del entorno de ejecución, que parte del fichero raíz
from app.api import crear_workflow
from app.api import crear_workflow_parametros
from app.api import aniadir_tarea_isolate_column
from app.api import aniadir_tarea_gen_fasta
from app.api import aniadir_tarea_reduce_sample
from app.api import aniadir_tarea_get_30kb
from app.api import aniadir_tarea_recognize_codons
from app.api import eliminar_ultima_tarea
from app.api import limpiar_workflow
from app.api import guardar_workflow_como_json
from app.api import cargar_workflow_desde_json
from app.api import ejecutar_workflow