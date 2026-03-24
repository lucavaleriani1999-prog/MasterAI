import os
import shutil
import uuid
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# CONFIGURAZIONE
BASE_DIR = "./data_local"
PARQUET_DIR = os.path.join(BASE_DIR, "parquet")
JSON_DIR = os.path.join(BASE_DIR, "json")
N_RECORDS = 500_000   # Modificabile
BATCH_SIZE = 100_000
RANDOM_SEED = 42

np.random.seed(RANDOM_SEED)

def ensure_clean_dirs():
    if os.path.exists(BASE_DIR):
        shutil.rmtree(BASE_DIR)
    os.makedirs(PARQUET_DIR, exist_ok=True)
    os.makedirs(JSON_DIR, exist_ok=True)

def generate_lookup_tables():
    print("Generazione Anagrafiche...")
    # Prodotti
    n_products = 5000
    products = pd.DataFrame({
        "product_id": np.arange(1, n_products+1, dtype=np.int32),
        "category": np.random.choice(["Electronics","Clothing","Home","Books","Beauty","Toys"], size=n_products),
        "price": np.round(np.random.lognormal(mean=3.0, sigma=1.0, size=n_products).astype(np.float32), 2)
    })
    
    # Clienti (Logica originale mantenuta)
    n_customers = 50_000 # Ridotto leggermente per velocità generazione studenti
    customers = pd.DataFrame({
        "customer_id": np.arange(1, n_customers+1, dtype=np.int32),
        "signup_date": pd.to_datetime("2018-01-01") + pd.to_timedelta(np.random.randint(0, 2000, size=n_customers), unit='D'),
        "loyalty_tier": np.random.choice(["bronze","silver","gold","platinum"], size=n_customers, p=[0.6,0.25,0.1,0.05])
    })
    
    # Regioni
    regions = pd.DataFrame({
        "region_id": [1,2,3,4,5],
        "region_name": ["North","South","East","West","Central"]
    })

    # Salvataggio Parquet
    products.to_parquet(os.path.join(PARQUET_DIR, "products.parquet"), index=False)
    customers.to_parquet(os.path.join(PARQUET_DIR, "customers.parquet"), index=False)
    regions.to_parquet(os.path.join(PARQUET_DIR, "regions.parquet"), index=False)
    
    return products, customers, regions

def synthesize_transactions(products, customers, regions):
    print(f"Generazione Transazioni ({N_RECORDS})...")
    n_batches = (N_RECORDS + BATCH_SIZE - 1) // BATCH_SIZE
    start_ts = datetime(2020,1,1)
    
    for b in range(n_batches):
        cur_size = min(BATCH_SIZE, N_RECORDS - b*BATCH_SIZE)
        
        # Campionamento veloce tramite indici
        prod_idx = np.random.randint(0, len(products), size=cur_size)
        cust_idx = np.random.randint(0, len(customers), size=cur_size)
        region_idx = np.random.randint(0, len(regions), size=cur_size)
        
        qty = np.random.randint(1, 6, size=cur_size).astype(np.int8)
        
        df = pd.DataFrame({
            "transaction_id": [str(uuid.uuid4()) for _ in range(cur_size)],
            "customer_id": customers["customer_id"].values[cust_idx],
            "product_id": products["product_id"].values[prod_idx],
            "region_id": regions["region_id"].values[region_idx],
            "quantity": qty,
            "amount": (qty * products["price"].values[prod_idx]).astype(np.float32),
            "ts": [start_ts + timedelta(days=np.random.randint(0, 1000)) for _ in range(cur_size)]
        })
        
        # Colonne derivate
        df["year"] = pd.to_datetime(df["ts"]).dt.year
        df["month"] = pd.to_datetime(df["ts"]).dt.month

        # Salvataggio Parquet (Batch)
        df.to_parquet(os.path.join(PARQUET_DIR, f"transactions_batch_{b:04d}.parquet"), index=False)
        
        # Salvataggio JSON (per esercizio Pandas/Streaming)
        # Convertiamo date in stringhe per JSON standard
        df["ts"] = df["ts"].astype(str)
        df.to_json(os.path.join(JSON_DIR, f"transactions_part_{b:04d}.jsonl"), orient="records", lines=True)
        
        print(f"Batch {b+1}/{n_batches} generato.")

if __name__ == "__main__":
    ensure_clean_dirs()
    p, c, r = generate_lookup_tables()
    synthesize_transactions(p, c, r)
    print("Dataset generato in ./data_local")

#ESERCIZIO 1: Ingestion e Limiti di Memoria (Pandas vs Dask)
#Obiettivo: Leggere file multipli tendendo in conto l’ottimizzazione della RAM
#1. Il blocco di Pandas: Prova a leggere tutti i file contenuti nella cartella dataset/transazioni_json/ usando Pandas. Noterai che è lento o complesso unire tanti file.
#o Task: Scrivi uno script che legge i file JSON uno alla volta (ciclo for), calcola lasomma della colonna amount per ogni file e stampa il totale generale alla fine.
#2. La soluzione Dask: Utilizza la libreria dask.dataframe.
#o Task: Leggi tutti i file JSON in un colpo solo usando il carattere jolly (*.json).
#o Task: Raggruppa le vendite per payment_type e calcola la media degli importi.
#Esegui il calcolo con .compute() e stampa il risultato.

import pandas as pd
import glob
import os
#1. Il blocco di Pandas
path_json = "./data_local/json/*.jsonl"
files = glob.glob(path_json)

totale_generale = 0.0

print(f"Inizio elaborazione di {len(files)} file con Pandas...")

for f in files:
    df_temp = pd.read_json(f, lines=True)
    somma_batch = df_temp['amount'].sum()
    totale_generale += somma_batch
    
    print(f"File {os.path.basename(f)} elaborato. Somma parziale: {somma_batch:.2f}")

print("-" * 30)
print(f"TOTALE GENERALE VENDITE: {totale_generale:.2f}")

#2. La soluzione Dask
import dask.dataframe as dd

ddf = dd.read_json("./data_local/json/*.jsonl")

print("Dati caricati virtualmente con Dask.")

colonna_group = 'region_id' 

print(f"Calcolo della media importi raggruppati per {colonna_group}...")

media_per_gruppo = ddf.groupby(colonna_group)['amount'].mean()
risultato = media_per_gruppo.compute()

print("\nRisultato finale (Dask):")
print(risultato)

#ESERCIZIO 2: Pipeline ETL con PySpark
#Obiettivo: Unire fonti dati diverse (Data Warehousing).
#1. Inizializza una SparkSession.
#2. Extract: Carica le tre tabelle principali dalla cartella parquet/: Transazioni (transactions_batch_*.parquet),Prodotti (products.parquet),Regioni (regions.parquet)
#3. Transform:
#• Unisci (JOIN) le Transazioni con i Prodotti (su product_id) per avere la categoria.
#• Unisci(JOIN) con le Regioni(su region_id) per avere il nome della regione(region_name).
#• Crea un DataFrame finale pulito con: transaction_id, region_name, category, amount,year.

from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder.appName("MegaShop_ETL_Pipeline").getOrCreate()

df_trans = spark.read.parquet("./data_local/parquet/transactions_batch_*.parquet")
df_prod = spark.read.parquet("./data_local/parquet/products.parquet")
df_reg = spark.read.parquet("./data_local/parquet/regions.parquet")

# Uniamo le transazioni ai prodotti per ottenere la 'category'
df_enriched = df_trans.join(df_prod, "product_id", "inner")

# Uniamo alle regioni per ottenere il 'region_name'
df_enriched = df_enriched.join(df_reg, "region_id", "inner")

# Selezione delle colonne richieste dalla traccia
df_final = df_enriched.select(
    "transaction_id",
    "region_name",
    "category",
    "amount",
    "year"
)

df_final.write.mode("overwrite").partitionBy("year").parquet("./data_local/processed_sales")

print("Pipeline ETL completata. Dati salvati in ./data_local/processed_sales")

#ESERCIZIO 3: Data Visualization (Reporting)
#Obiettivo: Creare insight visivi per il management.
#1. Partendo dal DataFrame Spark pulito (creato nell'Esercizio 2):
#o Calcola il Fatturato Totale per Categoria (category).
#o Esegui l'azione .toPandas() per portare questo risultato aggregato (che sarà piccolo, poche righe) in memoria locale.
#2. Utilizza Seaborn o Matplotlib per generare un Grafico a Barre (Bar Chart) che mostri il fatturato per ogni categoria.
#3. Salva il grafico come immagine fatturato_per_categoria.png o mostralo a video.

import seaborn as sns
import matplotlib.pyplot as plt

# 1. Aggregazione: Calcolo Fatturato Totale per Categoria
df_category_revenue = df_final.groupBy("category").sum("amount").withColumnRenamed("sum(amount)", "total_revenue")

# Conversione in Pandas (operazione sicura perché il risultato è piccolo)
pd_report = df_category_revenue.toPandas()

# 2. Visualizzazione con Seaborn
plt.figure(figsize=(12, 6))
sns.set_theme(style="whitegrid")

plot = sns.barplot(data=pd_report, x="category", y="total_revenue", palette="magma")

plt.title("Fatturato Totale per Categoria di Prodotto", fontsize=15)
plt.xlabel("Categoria", fontsize=12)
plt.ylabel("Fatturato (€)", fontsize=12)

# 3. Salvataggio e visualizzazione
plt.savefig("fatturato_per_categoria.png")
plt.show()

print("Grafico salvato come 'fatturato_per_categoria.png'")

#ESERCIZIO 4 (Bonus): Real-Time Streaming
#Obiettivo: Monitoraggio live.
#1. Crea uno script che ascolta la cartella data_local/json/.
#2. Ogni volta che viene aggiunto un file, lo script deve calcolare in tempo reale il numero totale di transazioni per ogni regione.
#3. Stampa l'aggiornamento a video (Console Sink). 

#P.S.Fatto interamente con supporto AI, riscontrate diverse difficoltà, inserito solo per capire se potesse essere corretto.

from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType

schema_json = StructType([
    StructField("transaction_id", StringType(), True),
    StructField("customer_id", IntegerType(), True),
    StructField("product_id", IntegerType(), True),
    StructField("region_id", IntegerType(), True),
    StructField("quantity", IntegerType(), True),
    StructField("amount", DoubleType(), True),
    StructField("ts", StringType(), True),
    StructField("year", IntegerType(), True),
    StructField("month", IntegerType(), True)
])
streaming_df = spark.readStream \
    .schema(schema_json) \
    .option("maxFilesPerTrigger", 1) \
    .json("./data_local/json/")

counts_stream = streaming_df.groupBy("region_id").count()

query = counts_stream.writeStream \
    .outputMode("complete") \
    .format("console") \
    .trigger(processingTime='5 seconds') \
    .start()

print("Streaming avviato. In attesa di nuovi file nella cartella ./data_local/json/...")
