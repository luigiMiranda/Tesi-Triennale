import gzip

def extract_and_return_gz_file(file_path):
    try:
        with gzip.open(file_path, 'rt') as gz_file:
            file_contents = gz_file.read()
            return file_contents
    except FileNotFoundError:
        print(f"File non trovato: {file_path}")
    except Exception as e:
        print(f"Errore durante l'apertura del file .gz: {str(e)}")