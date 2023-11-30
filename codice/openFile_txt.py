# questa funzione legge il file txt tempi e restituisce una lista contente stringhe e float corrispondenti
def read_file_txt(file_path):
    # Inizializza una lista vuota per salvare le righe
    data_list = []

    with open(file_path, 'r') as file:
        for line in file:
            # Rimuovi eventuali spazi bianchi iniziali e finali dalla riga
            line = line.strip()

            line = line.strip("['\"]")
            # Dividi la riga utilizzando la virgola come separatore
            elements = [element.strip() for element in line.split(',')]
            if len(elements) == 4:
                # Rimuovi eventuali apici singoli alla fine del primo elemento
                if elements[0].endswith("'"):
                    elements[0] = elements[0][:-1]
                # Converti gli elementi 1, 2 e 3 in float
                for i in range(1, 4):
                    elements[i] = float(elements[i])

                # Aggiungi gli elementi alla lista
                data_list.append(elements)
            elif len(elements) == 5:
                if elements[0].startswith("'"):
                    elements[0] = elements[0][1:]
                if elements[0].endswith("'"):
                    elements[0] = elements[0][:-1]
                if elements[1].startswith("'"):
                    elements[1] = elements[1][1:]
                    elements[1] = elements[1][:-1]
                # Se ci sono 5 elementi nella riga, unisci i primi due elementi in uno
                merged_value = f"{elements[0]} {elements[1]}"
                elements = [merged_value] + [float(elements[i]) for i in range(2, len(elements))]
                data_list.append(elements)
            else:
                # Numero di elementi non valido, ignora questa riga o gestiscila come preferisci
                print("numero elementi tempi non valido")
                continue
    return data_list


