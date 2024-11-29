from flask import Flask

app = Flask(__name__)

# Import routes (important: import after creating `app` to avoid circular imports)
# Se debe poner la ruta absoluta del entorno de ejecución, que parte del fichero raíz
from app.api import crear_workflow, crear_workflow_parametros, aniadir_tarea_isolate_column, aniadir_tarea_gen_fasta, aniadir_tarea_reduce_sample, aniadir_tarea_get_30kb, aniadir_tarea_recognize_codons, eliminar_ultima_tarea, limpiar_workflow, ejecutar_workflow