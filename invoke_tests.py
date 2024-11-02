from invoke import task
import subprocess

print("Invocando tests...")

# -> BV-BRC CLI 1.040. Go to https://github.com/BV-BRC/BV-BRC-CLI/releases and install the .deb version in Ubuntu. Authomatize the process via a bash/yaml/python script

@task
def test():
    """
    Ejecución de las pruebas unitarias
    """
    tests_result = subprocess.run(['pytest', 'tests/tests_hito2.py']) # Create the fasta file
    if tests_result.returncode == 0:
        print("\n----------------------\nTests ejecutados correctamente")

'''@task # Borrar archivos temporales creados durante los tests
def clean(c):
    c.run("find . -name '*.pyc' -exec rm -f {} +")'''
