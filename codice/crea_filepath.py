from pathlib import Path
import os
import re
# funzione per creare il file path partendo dalla directory principale del progetto
# viene passata la dir a cui voler accedere e il file di interesse
def make_path(dir,file):
    current_directory = Path.cwd()
    file_path = os.path.join(current_directory, dir, file)
    return file_path


def get_user():
    current_directory = Path.cwd()
    pattern = re.compile(r"user.*")  # Correggi il pattern regex
    for dir in current_directory.iterdir():
        if dir.is_dir() and pattern.match(dir.name):
            return dir.name  # Restituisci il nome della cartella utente trovata
    return None  # Nessuna cartella utente trovata
