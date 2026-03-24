"""
Progetto#2 — Analisi vendite realistica
Traccia:
Sei un data analyst in un’azienda di e-commerce. Ti vengono forniti:
o Un CSV con ordini clienti (ordini.csv) .
o Un JSON con informazioni prodotto (prodotti.json).
o Un CSV con dati clienti (clienti.csv).
Questo progetto simula una situazione reale in cui occorre integrare fonti dati multiple,
ottimizzare memoria, applicare filtri complessi, aggregazioni avanzate e serializzazione
efficente, come capita quotidianamente in un contesto lavorativo di Data Analyst o
Business Intelligence.
Consegna
"""
#Parte 1:Crea i seguenti DataSet: 
#Ordini.csv: 100.000 righe con ClienteID, ProdottoID, Quantità e DataOrdine.
#prodotti.json: 20 prodotti con Categoria e Fornitore.
# clienti.csv: 5.000 clienti con Regione e Segmento.
import pandas as pd
import numpy as np
import json

#Creazione dei DataSet:

#Cominciamo creando il Dataset attinente a (Prodotti.json)

prodotti_data = [
    {"ProdottoID": i, "Nome": f"Prod_{i}", "Prezzo": round(np.random.uniform(10, 500), 2), 
     "Categoria": np.random.choice(['Tech', 'Casa', 'Libri', 'Moda']), 
     "Fornitore": f"Vendor_{np.random.randint(1, 5)}"} 
    for i in range(1, 21)
]
with open('prodotti.json', 'w') as f:
    json.dump(prodotti_data, f)

#Proseguiamo creando il Dataset attinente a (clienti.csv)
clienti = pd.DataFrame({
    'ClienteID': range(1, 5001),
    'Regione': np.random.choice(['Nord', 'Centro', 'Sud', 'Isole'], 5000),
    'Segmento': np.random.choice(['Retail', 'Corporate', 'VIP'], 5000)
})
clienti.to_csv('clienti.csv', index=False)

#Infine creiamo il Dataset attinente a (Ordini.csv)
ordini = pd.DataFrame({
    'OrdineID': range(1, 100001),
    'ClienteID': np.random.randint(1, 5001, 100000),
    'ProdottoID': np.random.randint(1, 21, 100000),
    'Quantità': np.random.randint(1, 10, 100000),
    'DataOrdine': pd.to_datetime(np.random.choice(pd.date_range('2023-01-01', '2023-12-31'), 100000))
})
ordini.to_csv('ordini.csv', index=False)

print("File generati: ordini.csv, prodotti.json, clienti.csv")

#Parte 2:Creare un DataFrame unificato
# Unisci ordini.
# Unisci prodotti.
# Unisci clienti
df_ordini = pd.read_csv('ordini.csv')
df_clienti = pd.read_csv('clienti.csv')
df_prodotti = pd.read_json('prodotti.json')

# Controllo veloce memoria pre-ottimizzazione
memoria_iniziale = df_ordini.memory_usage(deep=True).sum() + df_clienti.memory_usage(deep=True).sum() + df_prodotti.memory_usage(deep=True).sum()

# Uniamo Ordini con Prodotti (Left Join su ProdottoID)
df_master = df_ordini.merge(df_prodotti, on='ProdottoID', how='left')

# Uniamo il risultato con Clienti
df_master = df_master.merge(df_clienti, on='ClienteID', how='left')

print(df_master.head())

#Parte 3: Ottimizzazione
# Ottimizzare i tipi di dato.
# Ottimizzare l’uso della memoria.

# Controllo memoria PRIMA dell'ottimizzazione
memoria_pre = df_master.memory_usage(deep=True).sum() / 1024**2  # In MB

cols_to_category = ['Regione', 'Segmento', 'Categoria', 'Fornitore', 'Nome']
for col in cols_to_category:
    df_master[col] = df_master[col].astype('category')

df_master['Quantità'] = pd.to_numeric(df_master['Quantità'], downcast='integer') # Diventa int8 o int16
df_master['Prezzo'] = pd.to_numeric(df_master['Prezzo'], downcast='float')       # Diventa float32
df_master['ProdottoID'] = pd.to_numeric(df_master['ProdottoID'], downcast='unsigned')
df_master['ClienteID'] = pd.to_numeric(df_master['ClienteID'], downcast='unsigned')

# C. Gestione Date
df_master['DataOrdine'] = pd.to_datetime(df_master['DataOrdine'])

# Controllo memoria DOPO l'ottimizzazione
memoria_post = df_master.memory_usage(deep=True).sum() / 1024**2 # In MB

print(f"Memoria Pre-Ottimizzazione: {memoria_pre:.2f} MB")
print(f"Memoria Post-Ottimizzazione: {memoria_post:.2f} MB")
print(f"Riduzione: {((memoria_pre - memoria_post) / memoria_pre) * 100:.1f}%")

#Parte 4: Creare colonne e filtra i dati
# Crea una colonna calcolata (ValoreTotale = Prezzo * Quantità).
# Filtrare ordini con ValoreTotale > 100 e clienti

df_master['ValoreTotale'] = df_master['Prezzo'] * df_master['Quantità']

filtro_VTot = (
    (df_master['ValoreTotale'] > 100) & 
    (df_master['Segmento'] == 'Corporate')
)

df_high_value_corporate = df_master.loc[filtro_VTot]

print(f"\nNumero ordini filtrati: {len(df_high_value_corporate)}")
print(df_high_value_corporate[['OrdineID', 'ValoreTotale', 'Segmento', 'Regione']].head())


