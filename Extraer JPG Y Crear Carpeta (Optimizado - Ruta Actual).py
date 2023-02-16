import os
import re
import zipfile
import concurrent.futures
import logging

logging.basicConfig(filename='extraction.log', level=logging.INFO,
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

# Extension de archivo a buscar
extension_to_search = '.jpg'

# Compila una expresión regular para buscar archivos con la extensión especificada
extensions_re = re.compile(extension_to_search + "$")


def extract_zip(zip_file):
    try:
        with zipfile.ZipFile(zip_file) as zf:
            for zip_info in zf.infolist():
                if extensions_re.search(zip_info.filename):
                    zf.extract(zip_info, zip_file.replace('.zip', ''))
                    logging.info(f'{zip_info.filename} Extraido de {zip_file}')
                    print("Ha sido procesado: ", zip_file)
    except zipfile.BadZipFile:
        logging.error(f"{zip_file} no es un archivo zip valido")


def search_zip_files(folder):
    # Recorre todos los archivos en la carpeta
    for item in os.scandir(folder):
        if item.is_file() and item.name.endswith('.zip'):
            yield item.path
        elif item.is_dir():
            yield from search_zip_files(item.path)


if __name__ == '__main__':
    folder = os.path.dirname(os.path.abspath(__file__))
    zip_files = list(search_zip_files(folder))
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(extract_zip, zip_files)

    logging.info("Proceso finalizado")
