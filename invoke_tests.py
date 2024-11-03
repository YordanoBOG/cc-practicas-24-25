from invoke import task
import subprocess

@task
def test(ctx): # Se necesita un contexto como argumento obligatorio
    """
    Ejecución de las pruebas unitarias
    """
    tests_result = subprocess.run(['pytest', 'tests/tests_hito2.py']) # Create the fasta file
    if tests_result.returncode == 0:
        print("\n----------------------\nTests ejecutados correctamente")
    else:
        print("\n----------------------\nLos tests fallaron")

'''@task # Borrar archivos temporales creados durante los tests
def clean(c):
    c.run("find . -name '*.pyc' -exec rm -f {} +")'''
