import os
import re
import zipfile

# Extension de archivo a buscar
extension_to_search = '.jpg'

# ruta de la carpeta a analizar
folder = os.path.dirname(os.path.abspath(__file__))

# Compila una expresión regular para buscar archivos con la extensión especificada
extensions_re = re.compile(extension_to_search + "$")

# Recorre todos los archivos en la carpeta
for zip_file in os.listdir(folder):
    # Verifica si el archivo es un .zip
    if zip_file.endswith('.zip'):
        # Intenta abrir el archivo .zip
        try:
            with zipfile.ZipFile(zip_file) as zf:
                # Recorre todos los archivos dentro del .zip
                for zip_info in zf.infolist():
                    # Verifica si el archivo dentro del .zip tiene la extensión especificada
                    if extensions_re.search(zip_info.filename):
                        # Extraye el archivo dentro de una carpeta con el nombre del archivo .zip
                        zf.extract(zip_info, zip_file.replace('.zip',''))
                        print(f'{zip_info.filename} Extraido de {zip_file}')
        except zipfile.BadZipFile:
            print(f"{zip_file} no es un archivo zip valido")
    else:
        print(f"{zip_file} no es un archivo zip")

print("Proceso finalizado")
