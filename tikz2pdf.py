import os
import re

TIKZ_FOLDER = "./tikz/"
PDF_FOLDER = "./pdf/"
COMPILER = "latexmk"
FLAGS = "-interaction=nonstopmode -lualatex"
TEMPLATE_NAME = "main.tex"
REPLACE_PATTERN = r'\\input\{[^{}]*?\.tikz\}'



files_names = os.listdir(TIKZ_FOLDER)




for doc_name in files_names:

    # Nombres sin extensiones
    name = os.path.splitext(doc_name)[0]
    template_name = os.path.splitext(TEMPLATE_NAME)[0]
    
    # Modificación del archivo de plantilla
    doc_full_name = TIKZ_FOLDER + doc_name
    with open(TEMPLATE_NAME, 'r') as template_file:
        content = template_file.read()
    
    replace_string = r"\\input{" + doc_full_name + '}'
    content = re.sub(REPLACE_PATTERN, replace_string, content)
    
    with open(TEMPLATE_NAME, 'w') as template_file:
        template_file.write(content)
    
    # Compilado
    doc_full_name = TIKZ_FOLDER + doc_name
    command = f"{COMPILER} {FLAGS} {TEMPLATE_NAME}"
    os.system(command)

    # Copiar los archivos en la carpeta correspondiente
    os.system(f"mv {template_name}.pdf {PDF_FOLDER}/{name}.pdf" )



