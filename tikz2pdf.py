from os.path import splitext,getmtime
from os import listdir

import time
import subprocess

TIKZ_FOLDER = "tikz/"
PDF_FOLDER = "pdf/"
COMPILER = "lualatex"
FLAGS = f"-interaction=nonstopmode"
TEMPLATE_NAME = "template.txt"
REPLACE_PATTERN = '%REPLACE%'


# Convierte la información de tiempo en un string
def time2str(time_info):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time_info))

# Abre el archivo .changelog y lo convierte a un diccionario
def getModificationInfo():
    with open(".changelog", 'r') as change_file:
        content = change_file.read()
    
    if ':' not in content:
        return {}

    content = content.split('\n')
    dict_info = {}

    for item in content:
        key, value = item.split(':', 1)
        dict_info[key] = value
    
    return dict_info

# Guarda el diccionario en el archivo .changelog
def saveModificationInfo(info_dict):
    content = ""
    for key in info_dict:
        content += key + ":" + info_dict[key] + '\n'
    content = content.strip()

    with open(".changelog", 'w') as change_file:
        change_file.write(content)

# Compara la ultima modificacion del archivo, si hubo cambios o es un archivo nuevo actualiza el diccionario
# Retorna si hubo modificaciones o no
def compareLastModification(doc_name, dict_info):    
    last_mod = time2str(getmtime(TIKZ_FOLDER + doc_name))
    
    if doc_name in dict_info:
        if dict_info[doc_name] != last_mod:
            dict_info[doc_name] = last_mod
            return True
        else:
            return False
    else:
        dict_info[doc_name] = last_mod
        return True


def createTexFile(doc_name):
    # Nombres sin extensiones y nombre completo
    name = splitext(doc_name)[0]
    doc_full_name = TIKZ_FOLDER + doc_name

    # Modificación del archivo de plantilla
    with open(TEMPLATE_NAME, 'r') as template_file:
        content = template_file.read()
    
    replace_string = doc_full_name
    content = content.replace(REPLACE_PATTERN, replace_string)
    
    # Crea un archivo tex por cada tikz
    with open(PDF_FOLDER + f"{name}.tex", 'w') as tex_file:
        tex_file.write(content)

def compileTexFile(doc_name):
    # Nombres sin extensiones y nombre completo
    name = splitext(doc_name)[0]

    command =  f"{COMPILER} {FLAGS} --output-directory={PDF_FOLDER} {PDF_FOLDER}{name}.tex > /dev/null"
    
    result = subprocess.run(command, shell=True)

    if result.returncode == 0:
        print(f"Compilado {doc_name} con éxito")
    else:
        print(f"Problema con {doc_name}")



files_names = listdir(TIKZ_FOLDER)
mod_info = getModificationInfo()

for doc_name in files_names:

    createTexFile(doc_name)

    modified = compareLastModification(doc_name, mod_info)

    if(modified):
        compileTexFile(doc_name)
    else:
        print(f"Archivo {doc_name} sin cambios")


# Guardando info de modificacion
saveModificationInfo(mod_info)

# Delete aux files
print("\nEliminando archivos auxiliares")
subprocess.run(f"rm -f {PDF_FOLDER}*.aux", shell=True)
subprocess.run(f"rm -f {PDF_FOLDER}*.log", shell=True)
subprocess.run(f"rm -f {PDF_FOLDER}*.tex", shell=True)