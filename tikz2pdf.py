import os

TIKZ_FOLDER = "./tikz/"
PDF_FOLDER = "./pdf/"

files = os.listdir(TIKZ_FOLDER)

for item in files:
    print(item)