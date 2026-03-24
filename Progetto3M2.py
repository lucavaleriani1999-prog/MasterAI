#Progetto 3 — Creare una Dashboard Avanzata di Visualizzazione
#Traccia: Realizzare una dashboard interattiva per analizzare i dati di vendita e redditività di un negozio online, usando Python (Pandas + Plotly Dash / Streamlit / Matplotlib /Seaborn).
#Struttura del dataset:
#• Order Date → Data dell’ordine
#• Ship Date → Data di spedizione
#• Category → Categoria prodotto (es. Furniture, O'ice Supplies, Technology)
#• Sub-Category → Sottocategoria prodotto
#• Sales → Vendite (€)
#• Profit → Utile (€)
#• Region → Area geografica
#• State → Stato/Regione
#• Quantity → Quantità venduta
#Consegna
# Parte 1 – Pulizia dati: 1. Convertire le colonne data (Order Date, Ship Date) in formato datetime. 2. Controllare valori nulli e duplicati. 3. Creare una nuova colonna Year dall’Order Date.
#Parte 2 – Analisi Esplorativa (EDA): 4. Totale vendite e profitti per anno. 5. Top 5 sottocategorie più vendute. 6. Mappa interattiva delle vendite

import pandas as pd
import streamlit as st
import plotly.express as px

# Configurazione della pagina Streamlit
st.set_page_config(page_title="Dashboard Vendite", layout="wide")
st.title("Dashboard Analisi Vendite e Redditività")

# --- CARICAMENTO DATI ---
# Usa il decorator st.cache_data per non ricaricare il dataset a ogni interazione
@st.cache_data
def load_data():
    # Sostituisci 'tuo_dataset.csv' con il percorso del tuo file
    # df = pd.read_csv('tuo_dataset.csv')
    
    # Per permetterti di testare il codice, ecco un piccolo dataset fittizio simulato
    data = {
        'Order Date': ['2022-01-15', '2022-06-20', '2023-03-10', '2023-11-05', '2023-12-12'],
        'Ship Date': ['2022-01-18', '2022-06-23', '2023-03-12', '2023-11-08', '2023-12-15'],
        'Category': ['Furniture', 'Technology', 'Office Supplies', 'Furniture', 'Technology'],
        'Sub-Category': ['Chairs', 'Phones', 'Paper', 'Tables', 'Accessories'],
        'Sales': [500, 1200, 50, 800, 300],
        'Profit': [50, 400, 10, -50, 80],
        'Region': ['East', 'West', 'East', 'South', 'West'],
        'State': ['NY', 'CA', 'NY', 'TX', 'CA'], # Usiamo le sigle per la mappa USA
        'Quantity': [2, 1, 10, 1, 3]
    }
    return pd.DataFrame(data)

df = load_data()

# ==========================================
# PARTE 1 - PULIZIA DATI
# ==========================================

st.header("1. Pulizia e Preparazione Dati")

# 1. Convertire le colonne data in formato datetime
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Ship Date'] = pd.to_datetime(df['Ship Date'])

# 2. Controllare valori nulli e duplicati
null_counts = df.isnull().sum().sum()
duplicate_counts = df.duplicated().sum()

# Mostriamo i risultati della pulizia
col1, col2 = st.columns(2)
with col1:
    st.info(f"Valori nulli trovati (e rimossi): **{null_counts}**")
with col2:
    st.info(f"Righe duplicate trovate (e rimosse): **{duplicate_counts}**")

# Rimozione effettiva (opzionale, ma consigliata)
df = df.dropna()
df = df.drop_duplicates()

# 3. Creare una nuova colonna 'Year' dall'Order Date
df['Year'] = df['Order Date'].dt.year

st.write("Anteprima del dataset pulito:", df.head())
st.divider()

# ==========================================
# PARTE 2 - ANALISI ESPLORATIVA (EDA)
# ==========================================

st.header("2. Analisi Esplorativa (EDA)")

# 4. Totale vendite e profitti per anno
st.subheader("Totale Vendite e Profitti per Anno")
# Raggruppiamo i dati
sales_profit_year = df.groupby('Year')[['Sales', 'Profit']].sum().reset_index()

# Grafico a barre raggruppate con Plotly
fig_year = px.bar(
    sales_profit_year, 
    x='Year', 
    y=['Sales', 'Profit'], 
    barmode='group',
    labels={'value': 'Importo (€)', 'variable': 'Metrica'},
    color_discrete_sequence=['#1f77b4', '#2ca02c'] # Blu per le vendite, verde per i profitti
)
# Forziamo l'asse X a mostrare gli anni come numeri interi
fig_year.update_layout(xaxis=dict(tickmode='linear')) 
st.plotly_chart(fig_year, use_container_width=True)

st.divider()

col_eda1, col_eda2 = st.columns(2)

with col_eda1:
    # 5. Top 5 sottocategorie più vendute
    st.subheader("Top 5 Sottocategorie per Vendite")
    top5_sub = df.groupby('Sub-Category')['Sales'].sum().nlargest(5).reset_index()
    
    fig_top5 = px.bar(
        top5_sub, 
        x='Sales', 
        y='Sub-Category', 
        orientation='h', # Orizzontale per leggere meglio i nomi
        color='Sales',
        color_continuous_scale='Blues'
    )
    fig_top5.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_top5, use_container_width=True)

with col_eda2:
    # 6. Mappa interattiva delle vendite
    st.subheader("Mappa Interattiva delle Vendite")
    # Raggruppiamo le vendite per stato
    state_sales = df.groupby('State')['Sales'].sum().reset_index()
    
    # NOTA: Usiamo locationmode="USA-states". 
    # Assicurati che la colonna 'State' contenga le sigle degli stati USA (es. 'CA', 'NY', 'TX').
    # Se hai dati italiani/europei, sarà necessario usare un file GeoJSON per i confini.
    fig_map = px.choropleth(
        state_sales, 
        locations='State', 
        locationmode="USA-states", 
        color='Sales', 
        scope="usa",
        color_continuous_scale='Reds'
    )
    st.plotly_chart(fig_map, use_container_width=True)