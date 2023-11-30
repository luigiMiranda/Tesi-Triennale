import gzip
import json
import pandas as pd
# legge il file gaze ma per le sole info utili alle fissazioni
def read_gazedata(file_content):
    # Inizializza un DataFrame per gestire i dati in modo più efficiente
    data = {'Timestamp': [], 'positionX': [], 'positionY': []}

    for line in file_content.split('\n'):
        if not line:
            continue  # Ignora le righe vuote
        try:
            json_data = json.loads(line)
            timestamp = json_data.get("timestamp")
            gaze2d = json_data.get("data", {}).get("gaze2d")

            if timestamp is not None and gaze2d is not None:
                data['Timestamp'].append(timestamp)
                data['positionX'].append(gaze2d[0])
                data['positionY'].append(gaze2d[1])

        except json.JSONDecodeError:
            # Ignora le righe che non possono essere analizzate come JSON
            continue
    return pd.DataFrame(data)


def read_gazedata3d(file_content):
    # Inizializza un DataFrame per gestire i dati in modo più efficiente
    data = {'Timestamp': [], 'positionX': [], 'positionY': [], 'positionZ': []}

    for line in file_content.split('\n'):
        if not line:
            continue  # Ignora le righe vuote
        try:
            json_data = json.loads(line)
            timestamp = json_data.get("timestamp")
            gaze3d = json_data.get("data", {}).get("gaze3d")

            if timestamp is not None and gaze3d is not None:
                data['Timestamp'].append(timestamp)
                data['positionX'].append(gaze3d[0])
                data['positionY'].append(gaze3d[1])
                data['positionZ'].append(gaze3d[2])

        except json.JSONDecodeError:
            # Ignora le righe che non possono essere analizzate come JSON
            continue
    return pd.DataFrame(data)


