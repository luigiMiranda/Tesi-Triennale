# scfrive una lista su file txt
def write_list_to_file(my_list, file_path):
    try:
        with open(file_path, 'w') as file:  
            for item in my_list:
                file.write(str(item) + '\n')
        print(f"Il file {file_path} è stato creato o aggiornato e i dati sono stati scritti con successo.")
    except Exception as e:
        print(f"Si è verificato un errore: {e}")

# scfrive un dizionario su file txt
def write_map_to_file(my_map, file_path):
    try:
        with open(file_path, 'w') as file:  
            for key, value_list in my_map.items():
                file.write(f"Chiave: {key}\n")
                file.write("Fissazioni:\n")
                for value in value_list:
                    file.write(f"  - {value}\n")
        print(f"Il file {file_path} è stato creato o aggiornato e i dati sono stati scritti con successo.")
    except Exception as e:
        print(f"Si è verificato un errore: {e}")