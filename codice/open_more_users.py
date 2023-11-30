import os
import zipfile
import pandas as pd
from pathlib import Path
from readGazedata import read_gazedata
from openFile_gz import extract_and_return_gz_file
from openFile_txt import read_file_txt
from fixation_detection import fixation, ivt, idt
from detection_fase_cognitiva import fase_detection_dict, img_detection_map
from crea_filepath import make_path, get_user
from crea_dataframe import create_df_fix, create_df_img_fix
from statistics_fixation import get_dataframe_statistics
from write_to_file_txt import write_list_to_file, write_map_to_file
import os
import zipfile
import matplotlib.pyplot as plt
import seaborn as sns

def is_zip_extracted(zip_file, destination_folder):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_info = zip_ref.infolist()
        for info in zip_info:
            extracted_path = os.path.join(destination_folder, info.filename)
            if os.path.exists(extracted_path):
                return True
    return False

def extract_zip_to_folder(root_directory):
    for item in os.listdir(root_directory):
        item_path = os.path.join(root_directory, item)

        if os.path.isfile(item_path) and item.lower().endswith('.zip'):
            if is_zip_extracted(item_path, "Recordings"):
                print(f"Il file '{item}' è già stato estratto nella cartella 'Recordings'. Skipping...")
                continue

            with zipfile.ZipFile(item_path, 'r') as zip_ref:
                zip_ref.extractall("Recordings")


def get_stat_all_mesi(dir_risultati):
    # Inizializza df_all_mesi come DataFrame vuoto
    df_all_mesi = pd.DataFrame()
    
    for nome_cartella in os.listdir(dir_risultati):
        percorso_cartella = os.path.join(dir_risultati, nome_cartella)
        
        if os.path.isdir(percorso_cartella):  # Verifica se è una directory
            df_temp = pd.read_csv(os.path.join(percorso_cartella, 'statistiche.csv'), dtype={'User-ID': str})
            df_all_mesi = pd.concat([df_all_mesi, df_temp], ignore_index=True)
    
    df_all_mesi.to_csv(os.path.join(dir_risultati, 'stat_all_mesi.csv'), index=False)  

# funzione per creare un dizionario che per ogni user associa il path con (1) e senza (1)
# in questo modo si puo decidere quando leggere da un path e quando dall altro
def create_user_path_dict(directory_name):
    user_path_dict = {}  # Dizionario per memorizzare i percorsi degli utenti
    current_directory = os.path.join(Path.cwd(), "Recordings")
    user_directory = os.path.join(current_directory, directory_name)

    for dir_name in os.listdir(user_directory):
        if dir_name.startswith("user") and os.path.isdir(os.path.join(user_directory, dir_name)):
            user_name = dir_name.split(".")[0]  # Estrai il nome dell'utente

            if user_name in user_path_dict:
                user_path_dict[user_name].append(os.path.join(user_directory, dir_name))
            else:
                user_path_dict[user_name] = [os.path.join(user_directory, dir_name)]

    return user_path_dict


def main():
    extract_zip_to_folder(Path.cwd())
    rec_dir = os.path.join(Path.cwd(), "Recordings")
    out_dir_statistiche = os.path.join(Path.cwd(), "risultati")
    os.makedirs(out_dir_statistiche, exist_ok=True)
    
    for cartella_mese in os.listdir(rec_dir):
        out_dir_mese = os.path.join(out_dir_statistiche, cartella_mese)
        os.makedirs(out_dir_mese, exist_ok=True)

        all_df_statistiche = []
        
        users = create_user_path_dict(cartella_mese)
        for user, percorsi in users.items():
            user_directory = os.path.join(out_dir_mese, f"{user}.output")
            if not os.path.exists(user_directory):
                gazedata_presente = False
                tempi_presenti = False
                fissazioni = []
                fix_idt = []
                for percorso in percorsi:
                    percorso_gazedata = os.path.join(percorso, "gazedata.gz")
                    percorso_tempi = os.path.join(percorso, "Tempi.txt")

                    if os.path.exists(percorso_gazedata):
                        gazedata_presente = True
                        # Esegui operazioni relative a gazedata qui
                        print(f"Operazioni per '{user}' con il file gazedata: {percorso_gazedata}")
                        file_path_gaze = os.path.join(percorso, "gazedata.gz")
                        gazedataFile = extract_and_return_gz_file(file_path_gaze)
                        gazedata = read_gazedata(gazedataFile)
                        maxDist = 0.01
                        minDur = 0.2
                        v = 0.5
                        
                        data_frequency = 100  # Frequenza dei dati in Hz
                        dur = int(minDur * data_frequency)
                        dispersion = 0.01
                        
                        fix_idt = idt(gazedata['positionX'], gazedata['positionY'], gazedata['Timestamp'],dispersion, dur)
                        #fix = ivt(gazedata['positionX'], gazedata['positionY'], gazedata['Timestamp'],v)
                        fissazioni = fixation(gazedata['positionX'], gazedata['positionY'], gazedata['Timestamp'], maxDist, minDur)

                    if os.path.exists(percorso_tempi):
                        tempi_presenti = True
                        # Esegui operazioni relative a Tempi qui
                        print(f"Operazioni per '{user}' con il file Tempi: {percorso_tempi}")
                        file_path_tempi = os.path.join(percorso, "Tempi.txt")
                        tempi = read_file_txt(file_path_tempi)
                if len(fix_idt) <= 0:
                    print(f"'{user}' non ha fissazioni")
                if gazedata_presente and tempi_presenti and len(fix_idt) > 0:
                    # Esegui operazioni che richiedono sia gazedata che Tempi
                    print(f"Operazioni per '{user}' che richiedono sia gazedata che Tempi")
                    fix_img_map = img_detection_map(fix_idt, tempi, False)
                    prem, postm = fase_detection_dict(fix_img_map)
                    out_dir_fix = user_directory  # Utilizza la directory dell'utente
                    if not os.path.exists(out_dir_fix):
                        os.makedirs(out_dir_fix, exist_ok=True)
                    
                    filepath_csv = make_path(out_dir_fix,"info.csv")
                    df = create_df_img_fix(fix_img_map, prem, postm)
                    df.to_csv(filepath_csv)
                    

                    df_statistiche = get_dataframe_statistics(fix_img_map,prem,postm)
                    filepath_statistiche_csv = make_path(out_dir_fix,"statistiche.csv")
                    
                    # imposta l user come indice del dataframe
                    indice_personalizzato = user[-3:]
                    df_statistiche.index = [indice_personalizzato] * len(df_statistiche)
                    df_statistiche.index.name = 'User-ID'
                    df_statistiche.to_csv(filepath_statistiche_csv)
                    df_statistiche['Mese'] = cartella_mese
                    all_df_statistiche.append(df_statistiche)

                elif not gazedata_presente or not tempi_presenti:
                    # Nessuno dei file è stato trovato per l'utente
                    print(f"Errore: Nessun file 'gazedata' o 'Tempi' trovato per '{user}'")
    
        if all_df_statistiche:
            combined_df_statistiche = pd.concat(all_df_statistiche, ignore_index=False)
            combined_df_statistiche.index.name = 'User-ID'

            # Crea e salva il file "statistiche.csv" nella cartella del mese
            filepath_statistiche_mese = os.path.join(out_dir_mese, "statistiche.csv")
            if os.path.exists(filepath_statistiche_mese):
                # Se il file "statistiche.csv" esiste già, carica il vecchio DataFrame e concatena i nuovi dati
                old_df_statistiche = pd.read_csv(filepath_statistiche_mese, index_col="User-ID")
                combined_df_statistiche = pd.concat([old_df_statistiche, combined_df_statistiche], ignore_index=False)

            combined_df_statistiche.to_csv(filepath_statistiche_mese)

    get_stat_all_mesi(out_dir_statistiche)    
    #all_mesi_df = pd.read_csv(os.path.join(out_dir_statistiche, 'stat_all_mesi.csv'), index_col="User-ID")
    # sns.barplot(x='User-ID', y='#medioFissazioni', data=all_mesi_df)
    # plt.title('Grafico a barre delle #medioFissazioni per ogni user')
    # plt.show()




# MAIN
if __name__ == "__main__":
    main()
    

            


