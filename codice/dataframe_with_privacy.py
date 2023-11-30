import pandas as pd

dfstat = pd.read_csv(r"C:\Users\Luigi\Desktop\tesi\risultati\Marzo 2023\statistiche.csv")
df = pd.read_csv(r"C:\Users\Luigi\Desktop\tesi\scheda pazienti eye tracker - Foglio1.csv")
colonne_selezionate = ['User-ID', 'Sesso', 'Stato lavorativo']
df_filtrato = df[colonne_selezionate]

df_merged = dfstat.merge(df_filtrato[['User-ID', 'Sesso', 'Stato lavorativo']], on='User-ID', how='left')

# Riempi le celle vuote con valori vuoti
df_merged.fillna({'Sesso': '', 'Stato lavorativo': ''}, inplace=True)

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
# Visualizza il DataFrame risultante
print(df_merged)
