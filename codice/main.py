from readGazedata import read_gazedata, read_gazedata3d
from openFile_gz import extract_and_return_gz_file
from openFile_txt import read_file_txt
from fixation_detection import fixation, idt, ivt
from detection_fase_cognitiva import img_detection_list, fase_detection_list, fase_detection_dict, img_detection_map
from write_to_file_txt import write_list_to_file, write_map_to_file
from crea_filepath import make_path, get_user
from crea_dataframe import create_df_fix, create_df_img_fix
from statistics_fixation import get_dataframe_statistics
import pandas as pd
import os
import time
import matplotlib.pyplot as plt
import seaborn as sns

# Funzione per calcolare il tempo di esecuzione e stamparlo a video
def measure_execution_time(function, *args, **kwargs):
    start_time = time.time()
    function(*args, **kwargs)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Tempo di esecuzione di {function.__name__}: {execution_time} secondi")

def crea_df_task(df):
    # Filtra le righe in base alla colonna 'stimolo'
    stimolo_values = ['T1', 'T2', 'T3', 'T4']
    df_filtrato = df.loc[df['Stimolo'].str.contains('|'.join(stimolo_values))]
    df_filtrato = df_filtrato.drop('Indice', axis=1)
    # Resetta l'indice
    df_filtrato = df_filtrato.reset_index(drop=True)
    # Ora df contiene solo le righe con 'stimolo' contenente T1, T2, T3 o T4
    # Dividi il DataFrame filtrato in sotto-dataframe
    t1_1 = df_filtrato.iloc[0:4]
    t2_1 = df_filtrato.iloc[4:8]
    t3_1 = df_filtrato.iloc[8:12]
    t4_1 = df_filtrato.iloc[12:28]
    t1_2 = df_filtrato.iloc[28:32]
    t2_2 = df_filtrato.iloc[32:36]
    t3_2 = df_filtrato.iloc[36:40]
    t4_2 = df_filtrato.iloc[40:56]

    # Creazione del DataFrame df_task
    df_task = pd.DataFrame()
    
    # Aggiunta delle colonne con i valori sommati di "#Fissazioni"
    df_task['t1_1_#fix'] = [t1_1['#Fissazioni'].sum()]  
    df_task['t2_1_#fix'] = [t2_1['#Fissazioni'].sum()]
    df_task['t3_1_#fix'] = [t3_1['#Fissazioni'].sum()]
    df_task['t4_1_#fix'] = [t4_1['#Fissazioni'].sum()]
    df_task['t1_2_#fix'] = [t1_2['#Fissazioni'].sum()]
    df_task['t2_2_#fix'] = [t2_2['#Fissazioni'].sum()]
    df_task['t3_2_#fix'] = [t3_2['#Fissazioni'].sum()]
    df_task['t4_2_#fix'] = [t4_2['#Fissazioni'].sum()]

    df_task['t1_1_ttf'] = [t1_1['TTF'].mean()]  
    df_task['t2_1_ttf'] = [t2_1['TTF'].mean()]
    df_task['t3_1_ttf'] = [t3_1['TTF'].mean()]
    df_task['t4_1_ttf'] = [t4_1['TTF'].mean()]
    df_task['t1_2_ttf'] = [t1_2['TTF'].mean()]
    df_task['t2_2_ttf'] = [t2_2['TTF'].mean()]
    df_task['t3_2_ttf'] = [t3_2['TTF'].mean()]
    df_task['t4_2_ttf'] = [t4_2['TTF'].mean()]

    return df_task


def main():
    
    file_path_gaze = make_path(get_user(),"gazedata.gz")
    print(file_path_gaze)
    #file_path_gaze = r"C:\Users\Luigi\Desktop\tesi\user066.17052023.161248\gazedata.gz"  # Sostituisci con il percorso del tuo file .gz
    gazedataFile = extract_and_return_gz_file(file_path_gaze)
    gazedata = read_gazedata(gazedataFile)
    #pd.set_option('display.max_rows', None)  # Visualizza tutte le righe
    #pd.set_option('display.max_columns', None)  # Visualizza tutte le colonne
    #print(gazedata)
    maxDist = 0.01
    minDur = 0.2
    v = 0.3

    data_frequency = 100  # Frequenza dei dati in Hz
    dur = int(minDur * data_frequency)
    dispersion = 0.01

    fix_idt = idt(gazedata['positionX'], gazedata['positionY'], gazedata['Timestamp'],dispersion, dur)
    fix_ivt = ivt(gazedata['positionX'], gazedata['positionY'], gazedata['Timestamp'],v)
    fissazioni = fixation(gazedata['positionX'], gazedata['positionY'], gazedata['Timestamp'], maxDist, minDur)
    """
    for entry in fissazioni:
        start_time, end_time, duration, end_x, end_y = entry
        print(f"[starttime: {start_time}, endtime: {end_time}, duration: {duration}, endx: {end_x}, endy: {end_y}]")
    print(len(fissazioni))
    """
   
    file_path_tempi = make_path(get_user(),"Tempi.txt")
    #file_path_tempi = r"C:\Users\Luigi\Desktop\tesi\user066.17052023.161248\Tempi.txt"
    tempi = read_file_txt(file_path_tempi)


    #fix_img_list = img_detection_list(fissazioni,tempi,False)
    #pre,post = fase_detection_list(fix_img_list)

    fix_img_map = img_detection_map(fix_idt,tempi,False)

    prem,postm = fase_detection_dict(fix_img_map)
    """
    for key, value_list in fix_img_map.items():
        print(f"Chiave: {key}")
        print("Valori:")
        for value in value_list:
            print(f"  - {value}")
    """

    out_dir_fix = "output_fix"
    os.makedirs(out_dir_fix, exist_ok=True)

    fix_path = make_path(out_dir_fix,"fix.txt")
    write_list_to_file(fissazioni,fix_path)
    fix_path_idt = make_path(out_dir_fix,"fix_idt.txt")
    write_list_to_file(fix_idt,fix_path_idt)
    fix_path_ivt = make_path(out_dir_fix,"fix_ivt.txt")
    write_list_to_file(fix_ivt,fix_path_ivt)
    

    #fp_img_list = make_path(out_dir_fix,"img_list.txt")
    fp_img_map = make_path(out_dir_fix,"img_map.txt")
    #fp_pre = make_path(out_dir_fix,"pre.txt")
    #fp_post = make_path(out_dir_fix,"post.txt")
    fp_pre_map = make_path(out_dir_fix,"pre_map.txt")
    fp_post_map = make_path(out_dir_fix,"post_map.txt")
    
    write_map_to_file(fix_img_map,fp_img_map)
    #write_list_to_file(fix_img_list, fp_img_list)
    #write_list_to_file(pre, fp_pre)
    #write_list_to_file(post, fp_post)
    write_map_to_file(prem,fp_pre_map)
    write_map_to_file(postm,fp_post_map)

    
    filepath_csv = make_path(out_dir_fix,"info.csv")
    df = create_df_img_fix(fix_img_map, prem, postm)
    df.to_csv(filepath_csv)

    df = pd.read_csv(filepath_csv)

    df_task = crea_df_task(df)



    df_statistiche = get_dataframe_statistics(fix_img_map,prem,postm)
    filepath_statistiche_csv = make_path(out_dir_fix,"statistiche.csv")
    df_statistiche = pd.concat([df_statistiche, df_task], axis=1)
    df_statistiche.to_csv(filepath_statistiche_csv)

    
    # measure_execution_time(idt, gazedata['positionX'], gazedata['positionY'], gazedata['Timestamp'], dispersion, dur)
    # measure_execution_time(ivt, gazedata['positionX'], gazedata['positionY'], gazedata['Timestamp'], v)
    # measure_execution_time(fixation, gazedata['positionX'], gazedata['positionY'], gazedata['Timestamp'], maxDist, minDur)

    
if __name__ == "__main__":
    main()




#type_str = str(type(fissazioni))
# print(f"La variabile è di tipo {type_str}")

