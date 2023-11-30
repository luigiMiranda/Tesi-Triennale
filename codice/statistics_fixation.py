import pandas as pd

from write_to_file_txt import write_list_to_file

"""
Questa funzione prende in input tre dizionari
dict: è il dizionario che continene le infromazioni sugli stimoli e le fissazioni associate a quegli stioli
pre: è il dizionario che contiene le informazioni sugli stimoli e le relative fissazioni della sola fase pre cognitiva
pre: è il dizionario che contiene le informazioni sugli stimoli e le relative fissazioni della sola fase post cognitiva

La funziona da in output un dataframe con pandas che servirà per creare il file csv per le seguenti informazioni:
- Numero medio, minimo, massimo di fissazioni per la visualizzazione dell'intero
stimolo, della sola fase pre-cognitiva e/o cognitiva.
- Durata media, minima, massima delle fissazioni per la visualizzazione dell'intero
stimolo, della sola fase pre-cognitiva e/o cognitiva.
- Time-to-first fixation medio, minimo, massimo per la visualizzazione dell'intero
stimolo, della sola fase pre-cognitiva e/o cognitiva.

"""
def get_dataframe_statistics(dict, pre, post):
    num_fissazioni_list = [len(fissazioni) for fissazioni in dict.values()]
    selected_keys = [chiave for chiave in dict.keys() if isinstance(chiave, tuple) and len(chiave) > 1 and isinstance(chiave[0], str) and ('T1' in chiave[0] or 'T2' in chiave[0] or 'T3' in chiave[0] or 'T4' in chiave[0] )]
    num_fissazioni_list_solo_stimoli = [len(dict[chiave]) for chiave in selected_keys]


    durata_list = [fissazione[2] for fissazioni in dict.values() for fissazione in fissazioni]
    ttf_list = [(fissazioni[0][0] - chiave[1]) for chiave, fissazioni in dict.items() if fissazioni]  # Calcola il ttf solo per il primo elemento
    
    
    medio_fissazioni = sum(num_fissazioni_list) / len(num_fissazioni_list)
    medio_fissazioni_stimoli = sum(num_fissazioni_list_solo_stimoli) / len(num_fissazioni_list_solo_stimoli)
    min_fissazioni = min(num_fissazioni_list)
    max_fissazioni = max(num_fissazioni_list)
    
    medio_durata = sum(durata_list) / len(durata_list) if durata_list else None
    min_durata = min(durata_list) if durata_list else None
    max_durata = max(durata_list) if durata_list else None
    
    medio_ttf = sum(ttf_list) / len(ttf_list) if ttf_list else None  # Calcola la media solo se ci sono ttf
    min_ttf = min(ttf_list) if ttf_list else None  # Calcola il minimo solo se ci sono ttf
    max_ttf = max(ttf_list) if ttf_list else None  # Calcola il massimo solo se ci sono ttf
    
    # Calcola #fix medio pre
    num_fissazioni_pre_list = [len(fissazioni) for fissazioni in pre.values()]
    medio_fissazioni_pre = sum(num_fissazioni_pre_list) / len(num_fissazioni_pre_list) if num_fissazioni_pre_list else 0

    # Calcola #fix medio post
    num_fissazioni_post_list = [len(fissazioni) for fissazioni in post.values()]
    medio_fissazioni_post = sum(num_fissazioni_post_list) / len(num_fissazioni_post_list) if num_fissazioni_post_list else 0

    # Calcola #fix min e max in pre e post
    min_fissazioni_pre = min(num_fissazioni_pre_list) if num_fissazioni_pre_list else None
    min_fissazioni_post = min(num_fissazioni_post_list) if num_fissazioni_post_list else None
    max_fissazioni_pre = max(num_fissazioni_pre_list) if num_fissazioni_pre_list else None
    max_fissazioni_post = max(num_fissazioni_post_list) if num_fissazioni_post_list else None

    durata_list_pre = [fissazione[2] for fissazioni in pre.values() for fissazione in fissazioni]
    medio_durata_pre = sum(durata_list_pre) / len(durata_list_pre) if durata_list_pre else None
    min_durata_pre = min(durata_list_pre) if durata_list_pre else None
    max_durata_pre = max(durata_list_pre) if durata_list_pre else None

    durata_list_post = [fissazione[2] for fissazioni in post.values() for fissazione in fissazioni]
    medio_durata_post = sum(durata_list_post) / len(durata_list_post) if durata_list_post else None
    min_durata_post = min(durata_list_post) if durata_list_post else None
    max_durata_post = max(durata_list_post) if durata_list_post else None

    ttf_list_pre = [(fissazioni[0][0] - chiave[1]) for chiave, fissazioni in pre.items() if fissazioni]
    medio_ttf_pre = sum(ttf_list_pre) / len(ttf_list_pre) if ttf_list_pre else None  # Calcola la media solo se ci sono ttf
    min_ttf_pre = min(ttf_list_pre) if ttf_list_pre else None  # Calcola il minimo solo se ci sono ttf
    max_ttf_pre = max(ttf_list_pre) if ttf_list_pre else None  # Calcola il massimo solo se ci sono ttf

    ttf_list_post = [(fissazioni[0][0] - chiave[1]) for chiave, fissazioni in post.items() if fissazioni]
    medio_ttf_post = sum(ttf_list_post) / len(ttf_list_post) if ttf_list_post else None  # Calcola la media solo se ci sono ttf
    min_ttf_post = min(ttf_list_post) if ttf_list_post else None  # Calcola il minimo solo se ci sono ttf
    max_ttf_post = max(ttf_list_post) if ttf_list_post else None  # Calcola il massimo solo se ci sono ttf

    df = pd.DataFrame({
        'TotFix': [sum(num_fissazioni_list)],
        'TotFixStimoli': [sum(num_fissazioni_list_solo_stimoli)],
        '#medioFissazioni': [medio_fissazioni],
        '#medioFissazioniStimoli': [medio_fissazioni_stimoli],
        '#minFissazioni': [min_fissazioni],
        '#maxFissazioni': [max_fissazioni],
        '#medioDurata': [medio_durata],
        '#minDurata': [min_durata],
        '#maxDurata': [max_durata],
        '#ttfMedio': [medio_ttf],
        '#ttfmax': [max_ttf],
        '#ttfmin': [min_ttf],
        '#minFixPre': [min_fissazioni_pre],
        '#minFixPost': [min_fissazioni_post],
        '#maxFixPre': [max_fissazioni_pre],
        '#maxFixPost': [max_fissazioni_post],
        '#fixMedioPre': [medio_fissazioni_pre],
        '#fixMedioPost': [medio_fissazioni_post],
        '#medioDurataPre': [medio_durata_pre],
        '#medioDurataPost': [medio_durata_post],
        '#minDurataPre': [min_durata_pre],
        '#minDurataPost': [min_durata_post],
        '#maxDurataPre': [max_durata_pre],
        '#maxDurataPost': [max_durata_post],
        '#ttfMedioPre': [medio_ttf_pre],
        '#ttfMedioPost': [medio_ttf_post],
        '#ttfMinPre': [min_ttf_pre],
        '#ttfMinPost': [min_ttf_post],
        '#ttfMaxPre': [max_ttf_pre],
        '#ttfMaxPost': [max_ttf_post]
    })
    


    return df

