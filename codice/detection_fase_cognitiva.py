import csv
from collections import OrderedDict

# funzione per associare le fissazioni alle immagini che considera tutte le immagini incluse quelle che non hanno generato fissazioni.
# questa funzione elenca prima le sole immagini che hanno generato fissazionie poi tutte quelle che non hanno generato fissazioni
def img_detection_map2(fixList, tempiList, restrict_choice):
    img_that_gen_fix = {}
    for fix in fixList:
        for i, time in enumerate(tempiList):
            if restrict_choice:
                if fix[0] < time[2] and fix[0] >= time[1]:
                    if tuple(time) in img_that_gen_fix:
                        img_that_gen_fix[tuple(time)].append(fix)
                    else:
                        img_that_gen_fix[tuple(time)] = [fix]
                    break
            else:
                if fix[0] < time[2] and fix[0] < time[1]:
                    if i > 0:
                        prev_time = tempiList[i-1]
                        if tuple(prev_time) in img_that_gen_fix:
                            img_that_gen_fix[tuple(prev_time)].append(fix)
                        else:
                            img_that_gen_fix[tuple(prev_time)] = [fix]
                    break
                if fix[0] < time[2] and fix[0] >= time[1]:
                    if tuple(time) in img_that_gen_fix:
                        img_that_gen_fix[tuple(time)].append(fix)
                    else:
                        img_that_gen_fix[tuple(time)] = [fix]
                    break
    
    # Aggiungi elementi mancanti con valori vuoti
    for time in tempiList:
        if tuple(time) not in img_that_gen_fix:
            img_that_gen_fix[tuple(time)] = []
    
    remove_not_util_map(img_that_gen_fix)
    return img_that_gen_fix



def riallinea_tempi(tempi):
    differenza = tempi[1][-3]
    # Aggiorna i valori in prima e seconda posizione di ciascun elemento
    for elemento in tempi:
        elemento[-3] -= differenza
        elemento[-2] -= differenza

# funzione per associare le fissazioni alle immagini che considera tutte le immagini incluse quelle che non hanno generato fissazioni.
# questa funzione elenca in ordine le immagini
def img_detection_map(fixList, tempiList, restrict_choice):

    riallinea_tempi(tempiList)
    img_that_gen_fix = OrderedDict()  # Usiamo un dizionario ordinato

    for time in tempiList:
        img_that_gen_fix[tuple(time)] = []  # Inizializziamo il dizionario con chiavi vuote

    for fix in fixList:
        for i, time in enumerate(tempiList):
            if restrict_choice:
                if fix[0] < time[2] and fix[0] >= time[1]:
                    img_that_gen_fix[tuple(time)].append(fix)
                    break
            else:
                if fix[0] < time[2] and fix[0] < time[1]:
                    if i > 0:
                        prev_time = tempiList[i-1]
                        img_that_gen_fix[tuple(prev_time)].append(fix)
                    break
                if fix[0] < time[2] and fix[0] >= time[1]:
                    img_that_gen_fix[tuple(time)].append(fix)
                    break

    remove_not_util_map(img_that_gen_fix)
    return img_that_gen_fix

def remove_not_util_map(map):
    chiavi_da_rimuovere = []

    for chiave in map.keys():
        if "Richiesta" in chiave[0] or "Inizio" in chiave[0] or "Pre" in chiave[0] or "Post" in chiave[0]:
            chiavi_da_rimuovere.append(chiave)

    for chiave in chiavi_da_rimuovere:
        del map[chiave]

# funzione che prende in input il dizionario che contiene tutte le immagini con le relative fissazioni
# da in output due dizionari che contengono rispettivamente le sole fissazioni in fase pre e pos cognitiva
def fase_detection_dict(img_that_gen_fix):
    pre_cognitiva = {}
    post_cognitiva = {}

    for chiave, fissazioni in img_that_gen_fix.items():
        pre_fissazioni = []
        post_fissazioni = []
        secondo_valore_chiave = chiave[1]

        for fissazione in fissazioni:
            primo_valore_fissazione = fissazione[0]
            differenza = primo_valore_fissazione - secondo_valore_chiave

            if differenza <= 0.3:
                pre_fissazioni.append(fissazione)
            else:
                post_fissazioni.append(fissazione)

        if pre_fissazioni:
            pre_cognitiva[chiave] = pre_fissazioni
        if post_fissazioni:
            post_cognitiva[chiave] = post_fissazioni

    return pre_cognitiva, post_cognitiva







# queste funzioni fanno le stesse cose di quelle di sopra ma lavorano con liste invece che dizionari
def img_detection_list(fixList, tempiList, restrict_choise):
    img_that_gen_fix = []
    for fix in fixList:
        for i, time in enumerate(tempiList):
            if restrict_choise:
                if fix[0] < time[2] and fix[0] >= time[1]:
                    img_that_gen_fix.append([time,fix])
                    break
            else:
                if fix[0] < time[2] and fix[0] < time[1]:
                    img_that_gen_fix.append([tempiList[i-1],fix])
                    break
                if fix[0] < time[2] and fix[0] >= time[1]:
                    img_that_gen_fix.append([time,fix])
                    break
    remove_not_util_list(img_that_gen_fix)
    return img_that_gen_fix

def remove_not_util_list(list):
    for item in list:
        if "Richiesta" in item[0][0] or "Inizio" in item[0][0] or "Pre" in item[0][0] or "Post" in item[0][0] :
            list.remove(item)

def fase_detection_list(img_that_gen_fix):
    pre_cognitiva = []
    post_cognitiva = []
    

    for el in img_that_gen_fix:
        if el[1][0] - el[0][1] <=0.3:
            pre_cognitiva.append(el)
        else:
            post_cognitiva.append(el)
    return pre_cognitiva, post_cognitiva