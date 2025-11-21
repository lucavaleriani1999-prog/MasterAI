#Progetto finale – Analisi di Vendite in una Catena di Negozi

#Parte 1 – Dataset di base: Creare un file CSV chiamato vendite.csv con almeno 30 righe che contenga le seguenti colonne: Data (formato YYYY-MM-DD),Negozio (stringa: es. Milano, Roma, Napoli…),Prodotto (stringa: es. Smartphone, Laptop, TV…),Quantità (intero),Prezzo_unitario (float).Esempio riga: 2023-09-01, Milano, Smartphone, 5, 499.99

import csv
with open("vendite.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Data", "Negozio", "Prodotto", "Quantità", "Prezzo_unitario"])
    writer.writerow([2024-12-18, "Milano", "Notebook", 4, 999.99])
    writer.writerow([2024-12-22, "Napoli", "Airpods", 7, 779.99])
    writer.writerow([2024-12-28, "Milano", "Tv", 3, 299.99])
    writer.writerow([2024-12-30, "Roma", "Smartphone", 1, 189.99])
    writer.writerow([2024-12-11, "Avellino", "Mac", 2, 662.99])
    writer.writerow([2024-12-13, "Vercelli", "Tv", 1, 562.99])
    writer.writerow([2024-12-15, "Roma", "Smartphone", 3, 762.99])
    writer.writerow([2024-12-17, "Firenze", "Mac", 2, 662.90])
    writer.writerow([2024-12-19, "Torino", "Airpods", 2, 62.99])
    writer.writerow([2024-12-18, "Padova", "Mac", 6, 992.99])
    writer.writerow([2024-12-13, "Verona", "Airpods", 4, 92.99])
    writer.writerow([2024-12-13, "Caltanisetta", "Tv", 3, 250.99])
    writer.writerow([2024-12-14, "Roma", "Tv", 2, 66.99])
    writer.writerow([2024-12-16, "Ancona", "Notebook", 1, 111.99])
    writer.writerow([2024-12-18, "Amelia", "Notebook", 2, 888.99])
    writer.writerow([2024-12-17, "Empoli", "Aspirapolvere", 9, 100.99])
    writer.writerow([2024-12-17, "Chieti", "Ferro da stiro", 11, 22.99])
    writer.writerow([2024-12-11, "Milano", "Tv", 2, 442.99])
    writer.writerow([2024-12-11, "Napoli", "Mac", 2, 462.99])
    writer.writerow([2024-12-18, "Rovigo", "Notebook", 3, 862.99])
    writer.writerow([2024-12-19, "Avellino", "Airpods", 1, 562.99])
    writer.writerow([2024-12-22, "Genova", "Airpods", 3, 55.99])
    writer.writerow([2024-12-23, "Palermo", "Mac", 12, 662.99])
    writer.writerow([2024-12-20, "Perugia", "Smartphone", 2, 999.99])
    writer.writerow([2024-12-28, "Terni", "Tv", 1, 862.99])
    writer.writerow([2024-12-29, "Arezzo", "Mac", 6, 888.99])
    writer.writerow([2024-12-31, "Avellino", "Mac", 4, 855.99])
    writer.writerow([2024-12-12, "Roma", "Smartphone", 5, 499.99])
    writer.writerow([2024-12-14, "Milano", "Notebook", 7, 799.99])


#Parte 2 – Importazione con Pandas: Importare il file CSV in un DataFrame Pandas e stampare:le prime 5 righe (head())il numero di righe e colonne (shape),le informazioni generali (info()).
import pandas as pd

dati_prodotti= {
    "Negozio": ["Milano","Napoli","Firenze","Roma","Avellino","Vercelli","Torino"],
    "Prodotto": ["Notebook","Airpods","Tv","Smartphone","Mac","Tv","Airpods"],
    "Quantità": ["10","20","15","25","30","12","18"],
    "Prezzo_unitario": ["662.99","779.99","299.99","189.99","999.99","100.99","22.99"]
}

df = pd.read_csv("vendite.csv")

print(df.head())
print("Numero di righe e colonne:", df.shape)
print(df.info())

#Parte 3 – Elaborazioni con Pandas: Aggiungere una colonna Incasso calcolata come Quantità * Prezzo_unitario. Calcolare con Pandas:l’incasso totale di tutta la catena,l’incasso medio per negozio,i 3 prodotti più venduti (in termini di quantità totale),Raggruppare i dati per Negozio e Prodotto e mostrare l’incasso medio.
df["Incasso"] = df["Quantità"] * df["Prezzo_unitario"]

Incasso_totale = df["Incasso"].sum()
print("Incasso totale:", Incasso_totale)

incasso_medio_negozio = df.groupby("Negozio")["Incasso"].mean().reset_index()
incasso_medio_negozio.rename(columns={"Incasso" : "Media_prodotto"}, inplace=True)

prodotti_top_3 = incasso_medio_negozio.loc[incasso_medio_negozio["Media_prodotto"].idxmax()]

incasso_medio_np = df.groupby(["Negozio","Prodotto"])["Incasso"].mean().reset_index()

print("Incasso Totale:",{Incasso_totale})
print("incasso_medio_negozio \n", incasso_medio_negozio)
print(f"\n i 3 prodotti più venduti: {prodotti_top_3['Negozio']} ([{prodotti_top_3['Media_prodotto']:.2f}])")
print("Incasso medio per negozio e prodotto \n", incasso_medio_np)

#Parte 4 – Uso di NumPy: Estrarre la colonna Quantità come array NumPy e calcolare:media, minimo, massimo e deviazione standard, percentuale di vendite sopra la media,Esempio parziale:import numpy as np,q = df["Quantità"].to_numpy(),media = np.mean(q),massimo = np.max(q)
import numpy as np
Quantità = df["Quantità"].to_numpy()
media = np.mean(Quantità)
minimo = np.min(Quantità)
massimo = np.max(Quantità)
deviazione_standard = np.std(Quantità)
percentuale_sopra_media = np.sum(Quantità > media) / len(Quantità) * 100
print(f"Media Quantità: {media:.2f}")
print(f"Minimo Quantità: {minimo}")
print(f"Massimo Quantità: {massimo}")
print(f"Deviazione Standard Quantità: {deviazione_standard:.2f}")
print(f"Percentuale di vendite sopra la media: {percentuale_sopra_media:.2f}%")

#Creare un array NumPy 2D che contenga solo Quantità e Prezzo_unitario e calcolare per ogni riga l’incasso. Confrontare i risultati con la colonna Incasso del DataFrame per verificarne la correttezza.

Numpy_2D = df[["Quantità","Prezzo_unitario"]].to_numpy()
incasso_calcolato = Numpy_2D[:,0] * Numpy_2D[:,1]
confronto = np.allclose(incasso_calcolato, df["Incasso"].to_numpy())
print(f"Confronto tra incasso calcolato e colonna Incasso del DataFrame: {confronto}")

#Parte 5 – Visualizzazioni con Matplotlib: Creare i seguenti grafici: Grafico a barre: incasso totale per ogni negozio. Grafico a torta: percentuale di incassi per ciascun prodotto. Grafico a linee: andamento giornaliero degli incassi totali della catena. Esempio parziale (grafico a barre): import matplotlib.pyplot as plt, df.groupby("Negozio")["Incasso"].sum().plot(kind="bar"), plt.show()

import matplotlib.pyplot as plt
incasso_per_negozio = df.groupby("Negozio")["Incasso"].sum()
incasso_per_negozio.plot(kind="bar", title="Incasso Totale per Negozio", color="orange")
plt.xlabel("Negozio")
plt.ylabel("Incasso")
plt.show()

incasso_per_prodotto = df.groupby("Prodotto")["Incasso"].sum()
plt.pie(incasso_per_prodotto, labels=incasso_per_prodotto.index, autopct='%1.1f%%')
plt.title ("Grafico a torta percentuale di incassi per ciascun prodotto")
plt.show()

plt.plot(df["Data"], df["Incasso"], marker = "o", color = "blue")
plt.title ("Andamento giornaliero degli incassi totali della catena")
plt.xlabel("Data")
plt.ylabel("Incasso")
plt.show()

#Parte 6 – Analisi Avanzata: Creare una nuova colonna Categoria che raggruppi i prodotti in grandi famiglie (es. Smartphone e Laptop → Informatica, TV → Elettrodomestici). Calcolare per ogni categoria: incasso totale, quantità media venduta, Salvare il DataFrame aggiornato con le nuove colonne in un nuovo file vendite_analizzate.csv.

def assegna_categoria(prodotto):
    if prodotto in ["Smartphone", "Laptop", "Mac", "Notebook"]:
        return "Informatica"
    elif prodotto in ["Tv", "Aspirapolvere", "Ferro da stiro"]:
        return "Elettrodomestici"
    elif prodotto in ["Airpods"]:
        return "Accessori"
    else:
        return "Altro"
df["Categoria"] = df["Prodotto"].apply(assegna_categoria)
incasso_per_categoria = df.groupby("Categoria")["Incasso"].sum().reset_index()
quantità_media_per_categoria = df.groupby("Categoria")["Quantità"].mean().reset_index
df.to_csv("vendite_analizzate.csv", index=False)
print("Incasso per Categoria \n", incasso_per_categoria)
print("Quantità media per Categoria \n", quantità_media_per_categoria)


#Parte 7 – Estensioni (per i più bravi): Creare un grafico combinato: incasso medio per categoria (grafico a barre) + linea della quantità media venduta. Creare una funzione top_n_prodotti(n) che restituisca i n prodotti più venduti in termini di incasso totale.

import matplotlib.pyplot as plt
incasso_medio_categoria = df.groupby("Categoria")["Incasso"].mean()
quantità_media_categoria = df.groupby("Categoria")["Quantità"].mean()
figura, ax1 = plt.subplots()
ax1.bar(incasso_medio_categoria.index, incasso_medio_categoria, color="green", label="Incasso Medio")
ax2 = ax1.twinx()
ax2.plot(quantità_media_categoria.index, quantità_media_categoria, color="orange", marker ="o", label="Quantità Media")
ax1.set_xlabel("Categoria")
ax1.set_ylabel("Incasso Medio")
ax2.set_ylabel("Quantità Media")
plt.title("Incasso Medio e Quantità Media per Categoria")
figura.legend(loc="upper right", bbox_to_anchor=(1,1), bbox_transform=ax1.transAxes)
plt.show()
def top_n_prodotti(n):
    incasso_per_prodotto = df.groupby("Prodotto")["Incasso"].sum().reset_index()
    top_n = incasso_per_prodotto.nlargest(n,"Incasso")
    return top_n
n = 3
top_prodotti = top_n_prodotti(n)
print(f"I {n} prodotti più venduti in termini di incasso totale:\n", top_prodotti)  