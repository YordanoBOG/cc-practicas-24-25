from invoke import task
import subprocess

#print("Invocando tests...")

# -> BV-BRC CLI 1.040. Go to https://github.com/BV-BRC/BV-BRC-CLI/releases and install the .deb version in Ubuntu. Authomatize the process via a bash/yaml/python script
'''
Traceback (most recent call last):
  File "/home/runner/work/CC-Practicas-24-25/CC-Practicas-24-25/invoke_tests.py", line 9, in <module>
    def test():
  File "/opt/hostedtoolcache/Python/3.10.15/x64/lib/python3.10/site-packages/invoke/tasks.py", line 312, in task
    return klass(args[0], **kwargs)
  File "/opt/hostedtoolcache/Python/3.10.15/x64/lib/python3.10/site-packages/invoke/tasks.py", line 76, in __init__
    self.positional = self.fill_implicit_positionals(positional)
  File "/opt/hostedtoolcache/Python/3.10.15/x64/lib/python3.10/site-packages/invoke/tasks.py", line 167, in fill_implicit_positionals
    args, spec_dict = self.argspec(self.body)
  File "/opt/hostedtoolcache/Python/3.10.15/x64/lib/python3.10/site-packages/invoke/tasks.py", line 162, in argspec
    raise TypeError("Tasks must have an initial Context argument!")
TypeError: Tasks must have an initial Context argument!
'''
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
