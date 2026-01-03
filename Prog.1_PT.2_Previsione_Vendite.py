#Progetto #1 — Previsioni vendite
#Lavorare su un dataset di vendite storiche per comprendere i dati, pulirli, trasformarli e produrre delle previsioni di base usando metodi semplici e direttamente implementabili con Pandas e Python “puro”.
#Dataset (esempio di struttura), Data — data della vendita
#Prodotto — nome o codice prodotto,Vendite — quantità venduta quel giorno,Prezzo — prezzo unitario (opzionale),I dati possono contenere valori mancanti, duplicati o inconsistenze.
#Consegna, Parte 1 - Caricamento e esplorazione dati: Leggere il dataset con Pandas.Visualizzare le prime righe, la struttura (.info()), e statistiche descrittive (.describe()).
#Parte 2 - Pulizia: Gestire valori mancanti (es. sostituire con 0 o media).Rimuovere duplicati.Verificare che i tipi di dato siano corretti (date come datetime, quantità come numeri, ecc.).
#Parte 3 - Analisi esplorativa: Calcolare vendite totali per prodotto. Individuare il prodotto più venduto e quello meno venduto. Calcolare vendite medie giornaliere.

import pandas as pd
import numpy as np
#Parte 1: 
data = {
    "Data": pd.date_range(start = "2025-01-01", periods = 31),
    "Prodotto": ["A","B","C","B","A","C","A","B","C","B","A","C","A","B","C","B","A","C","A","B","C","B","A","C","A","B","C","B","A","C","A"],
    "Vendite":[10,2,5,8,3,5,4,7,8,9,6,2,4,np.nan,7,5,6,8,4,3,8,4,4,7,8,9,5,2,6,7,12],
    "Prezzo":[50,75,59,62,100,150,111,235,98,111,236,222,25,50,75,59,62,100,111,155,166,124,98,111,222,369,754,259,333,111,101],
}

df= pd.DataFrame(data)
print(df.head())
print(df.info())
print(df.describe())

#Parte 2:
df["Vendite"]=df["Vendite"].fillna(df["Vendite"].mean())
df=df.drop_duplicates()
df["Data"]= pd.to_datetime(df["Data"])
df["Vendite"]= df["Vendite"].astype(float)
df["Prezzo"]= df["Prezzo"].astype(float)
print(df.info())

#Parte 3:
Tot_per_prodotto= df.groupby("Prodotto")["Vendite"].sum()
print("Tot_per_prodotto:", Tot_per_prodotto)
print("Prodotto con più vendite:", Tot_per_prodotto.idxmax())
print("Prodotto con meno vendite:", Tot_per_prodotto.idxmin())
Vendite_medie_giornaliere= df.groupby("Data")["Vendite"].sum()
print("Vendite medie giornaliere:", Vendite_medie_giornaliere.mean())
print(Vendite_medie_giornaliere)



