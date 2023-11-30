import pandas as pd

"""
Questa funzione prende in input tre dizionari
dict: è il dizionario che continene le infromazioni sugli stimoli e le fissazioni associate a quegli stioli
pre: è il dizionario che contiene le informazioni sugli stimoli e le relative fissazioni della sola fase pre cognitiva
pre: è il dizionario che contiene le informazioni sugli stimoli e le relative fissazioni della sola fase post cognitiva

La funziona da in output un dataframe con pandas che servirà per creare il file csv con questa struttura:
'Stimolo',
'#Fissazioni',
'#Fissazioni Pre',
'#Fissazioni Post',
'Durata Minima',
'Durata Massima',
'Durata Media Fissazioni',
'Start-End-Dur-X-Y'

quindi avremo un file csv con n righe dove n è il numero di stimoli, e per ogni stimolo ci saranno le informazioni sopralencate.
"""
def create_df_img_fix(data_dict, pre, post):
    immagini = [chiave[0] for chiave in data_dict.keys()]
    num_fissazioni = [len(fissazioni) for fissazioni in data_dict.values()]
    durata_minimo = [min([fissazione[2] for fissazione in fissazioni]) if fissazioni else 0 for fissazioni in data_dict.values()]
    duarata_massimo = [max([fissazione[2] for fissazione in fissazioni]) if fissazioni else 0 for fissazioni in data_dict.values()]

    info_fissazioni = [fissazioni for fissazioni in data_dict.values()]

    # Calcola la durata media delle fissazioni
    durata_media = [sum([fissazione[2] for fissazione in fissazioni]) / len(fissazioni) if len(fissazioni) > 0 else 0 for fissazioni in data_dict.values()]

    num_fissazioni_pre = [len(pre.get(chiave, [])) if chiave in pre else 0 for chiave in data_dict]
    num_fissazioni_post = [len(post.get(chiave, [])) if chiave in post else 0 for chiave in data_dict]

    
    durata_minimo_pre = [min([fissazione[2] for fissazione in pre.get(chiave, [])]) if chiave in pre else 0 for chiave in data_dict]
    durata_massimo_pre = [max([fissazione[2] for fissazione in pre.get(chiave, [])]) if chiave in pre else 0 for chiave in data_dict]

    durata_minimo_post = [min([fissazione[2] for fissazione in post.get(chiave, [])]) if chiave in post else 0 for chiave in data_dict]
    durata_massimo_post = [max([fissazione[2] for fissazione in post.get(chiave, [])]) if chiave in post else 0 for chiave in data_dict]

    durata_media_pre = [sum([fissazione[2] for fissazione in pre.get(chiave, [])]) / len(pre.get(chiave, [])) if chiave in pre and len(pre.get(chiave, [])) > 0 else 0 for chiave in data_dict]
    durata_media_post = [sum([fissazione[2] for fissazione in post.get(chiave, [])]) / len(post.get(chiave, [])) if chiave in post and len(post.get(chiave, [])) > 0 else 0 for chiave in data_dict]


    ttf = [fissazioni[0][0] - chiave[1] if fissazioni else 0 for chiave, fissazioni in data_dict.items()]

    ttf_pre = [pre[chiave][0][0] - chiave[1] if chiave in pre and pre[chiave] else 0 for chiave in data_dict]
    ttf_post = [post[chiave][0][0] - chiave[1] if chiave in post and post[chiave] else 0 for chiave in data_dict]

    # Crea un DataFrame con le colonne richieste
    df = pd.DataFrame({
        'Stimolo': immagini,
        '#Fissazioni': num_fissazioni,
        '#Fissazioni Pre': num_fissazioni_pre,
        '#Fissazioni Post': num_fissazioni_post,
        'Durata Minima': durata_minimo,
        'Durata Massima': duarata_massimo,
        'Durata Media': durata_media,
        'Durata Minima Pre': durata_minimo_pre,
        'Durata Minima Post': durata_minimo_post,
        'Durata Massima Pre': durata_massimo_pre,
        'Durata Massima Post': durata_massimo_post,
        'Durata Media Pre': durata_media_pre,
        'Durata Media Post': durata_media_post,
        'TTF': ttf,
        'TTF Pre': ttf_pre,
        'TTF Post': ttf_post,
        'Start-End-Dur-X-Y': info_fissazioni
    })
    df.index.name = 'Indice'
    return df



def create_df_fix(list):
    # Estrai le prime liste da ciascun elemento
    prime_liste = [elemento[0] for elemento in list]
    seconde_liste = [elemento[1] for elemento in list]
    # Crea un DataFrame con le prime liste
    df= pd.DataFrame(prime_liste, columns=['Nome Immagine', 'Inizio', 'Fine', 'Durata'])
    df['Inizio Fix'] = [sublist[0] for sublist in seconde_liste]
    df['Fine Fix'] = [sublist[1] for sublist in seconde_liste]
    df['Durata Fix'] = [sublist[2] for sublist in seconde_liste]
    df['Posx'] = [sublist[3] for sublist in seconde_liste]
    df['Posy'] = [sublist[4] for sublist in seconde_liste]

    return df
