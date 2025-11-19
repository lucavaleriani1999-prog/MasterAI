#Analisi di un Sistema di Prenotazione Viaggi:
# #Un’agenzia di viaggi online vuole realizzare un sistema informatico per gestire le prenotazioni dei clienti.Il sistema deve permettere di memorizzare le informazioni dei clienti e dei viaggi prenotati,calcolare statistiche sulle vendite,analizzare i dati con strumenti avanzati,visualizzare i risultati in forma grafica.

#Parte 1 – Variabili e Tipi di Dati: 
# Definisci variabili per rappresentare le seguenti informazioni di un cliente:nome (stringa),età (intero),saldo conto (float),stato VIP (booleano). Crea una lista di destinazioni disponibili (almeno 5 città).Definisci un dizionario che associa ogni destinazione a un prezzo medio del viaggio.

nome = "Luca"
età = 26
saldo_conto = 5000.22
vip = True
destinazioni_viaggio = ["Siviglia", "Tokio", "Buenos Aires", "Tangeri", "Londra"]
prezzo_medio_viaggio = {
    "Siviglia": 425.99,
    "Tokio": 625.25,
    "Buenos Aires": 333.45,
    "Tangeri": 211.25,
    "Londra": 799.99
}

#Parte 2 – Programmazione ad Oggetti (OOP): Crea una classe Cliente con attributi: nome, età, vip.Aggiungi un metodo per stampare le informazioni.Crea una classe Viaggio con attributi: destinazione, prezzo, durata in giorni.Crea una classe Prenotazione che colleghi un cliente a un viaggio.Deve calcolare l’importo finale, con sconto del 10% se il cliente è VIP.Aggiungi un metodo dettagli() che stampa le informazioni complete.

class Cliente:
    def __init__(self,nome,età,vip):
        self.nome = nome
        self.età = età
        self.vip = vip
    def stampare_info(self):
        persona_vip ="VIP" if self.vip else "Non VIP"
        print(f"Nome: {self.nome}, Età: {self.età}, Stato: {persona_vip}")

class Viaggio:
    def __init__(self,destinazione,prezzo,durata_giorni):
        self.destinazione = destinazione
        self.prezzo = prezzo
        self.durata_giorni = durata_giorni
class Prenotazione:
    def __init__(self,cliente,viaggio):
        self.cliente = cliente
        self.viaggio = viaggio
    def importo_finale(self):
        if self.cliente.vip:
            return self.viaggio.prezzo * 0.9
        return self.viaggio.prezzo
    def dettagli(self):
        self.cliente.stampare_info()
        print(f"Destinazione: {self.viaggio.destinazione}, Prezzo: {self.viaggio.prezzo} €, Durata: {self.viaggio.durata_giorni} giorni")
        print(f"Importo finale (con sconto se VIP): {self.importo_finale()} €")

#Parte 3 – NumPy: Genera un array NumPy di 100 prenotazioni simulate, con prezzi casuali fra 200 e 2000 €.Calcola e stampa:prezzo medio,prezzo minimo e massimo,deviazione standard,percentuale di prenotazioni sopra la media.

import numpy as np

np.random.seed(0)
prenotazioni_sim_prezzi = np.random.uniform(200,2000,100)
prezzo_medio = np.mean(prenotazioni_sim_prezzi)
prezzo_minimo = np.min(prenotazioni_sim_prezzi)
prezzo_massimo = np.max(prenotazioni_sim_prezzi)
deviazione_standard = np.std(prenotazioni_sim_prezzi)
percentuale_prenotazioni_sopra_media = np.sum(prenotazioni_sim_prezzi > prezzo_medio) / len(prenotazioni_sim_prezzi) *100

print(f"Prezzo Medio: {prezzo_medio} €")
print(f"Prezzo Minimo: {prezzo_minimo} €")
print(f"Prezzo Massimo: {prezzo_massimo} €")
print(f"Deviazione Standard: {deviazione_standard} €")
print(f"Percentuale di Prenotazioni sopra la Media: {percentuale_prenotazioni_sopra_media} %")

#Parte 4 – Pandas: Crea un DataFrame Pandas con colonne:Cliente, Destinazione, Prezzo, Giorno_Partenza, Durata, Incasso.Calcola con Pandas:incasso totale dell’agenzia,incasso medio per destinazione,top 3 destinazioni più vendute.

import pandas as pd

clienti = ["Luca","Marco","Franco","Elia","Giovanni"]
destinazioni = ["Siviglia","Tokio","Buenos Aires","Tangeri","Londra"]
prezzi = [425.99, 625.25, 333.45, 211.25, 799.99]
giorno_della_partenza = ["2024-08-06","2024-12-26","2025-05-19","2025-06-30","2025-08-19"]
durata_giorni =  [10, 3, 5, 7, 9]
incasso_euro = [150.22, 166.48, 522.16, 0.52, 33.24]
df = pd.DataFrame({
    "Cliente": clienti,
    "Destinazione": destinazioni,
    "Prezzo": prezzi,
    "Giorno_della_partenza": giorno_della_partenza,
    "Durata": durata_giorni,
    "Incasso": incasso_euro
})

incasso_totale = df["Incasso"].sum()
incasso_medio_per_destinazione = df.groupby("Destinazione")["Incasso"].mean()
top_3_destinazioni_piu_vendute = df["Destinazione"].value_counts().head(3)  
print(f"Incasso Totale dell'Agenzia: {incasso_totale} €")
print("Incasso Medio per Destinazione:")
print(incasso_medio_per_destinazione)
print("Top 3 Destinazioni più Vendute:")
print(top_3_destinazioni_piu_vendute)

#Parte 5 – Matplotlib: Crea un grafico a barre che mostri l’incasso per ogni destinazione.Crea un grafico a linee che mostri l’andamento giornaliero degli incassi.Crea un grafico a torta che mostri la percentuale di vendite per ciascuna destinazione.

import matplotlib.pyplot as plt

incasso_per_destinazione = df.groupby("Destinazione")["Incasso"].sum()
plt.figure(figsize=(18,6))
plt.subplot(1,3,1)
plt.title("Grafico a Barre: Incasso per Destinazione")
plt.bar(incasso_per_destinazione.index, incasso_per_destinazione.values)
plt.xlabel("Destinazione")
plt.ylabel("Incasso (€)")
plt.show()

df['Giorno_della_partenza'] = pd.to_datetime(df['Giorno_della_partenza'])
incasso_giornaliero = df.groupby('Giorno_della_partenza')['Incasso'].sum()
plt.subplot(1,3,2)
plt.title("Grafico a Linee: Andamento Giornaliero degli Incassi")
plt.plot(incasso_giornaliero.index, incasso_giornaliero.values, marker='o')
plt.xlabel("Giorno della Partenza")
plt.ylabel("Incasso (€)")
plt.show()

#Parte 6 – Analisi Avanzata: Raggruppa i viaggi in categorie: "Europa", "Asia", "America", "Africa".(Puoi usare un dizionario che associa ogni destinazione a una categoria).Calcola con Pandas:incasso totale per categoria,durata media dei viaggi per categoria.Salva il DataFrame aggiornato in un CSV chiamato prenotazioni_analizzate.csv.

Categoria_Destinazione = {
    "Siviglia": "Europa",
    "Tokio": "Asia",
    "Buenos Aires": "America",
    "Tangeri": "Africa",
    "Londra": "Europa"
}

df['Categoria'] = df['Destinazione'].map(Categoria_Destinazione)
incasso_per_categoria = df.groupby('Categoria')['Incasso'].sum()
durata_media_per_categoria = df.groupby('Categoria')['Durata'].mean()
print("Incasso Totale per Categoria:")
print(incasso_per_categoria)
print("Durata Media dei Viaggi per Categoria:")
print(durata_media_per_categoria)
df.to_csv("prenotazioni_analizzate.csv", index=False)

#Parte 7 – Estensioni:Crea una funzione che restituisce i N clienti con più prenotazioni.Realizza un grafico combinato (barre + linea) che mostri:barre = incasso medio per categoria,linea = durata media per categoria.

def top_n_clienti_con_piu_prenotazioni(df, n):
    clienti_top = df['Cliente'].value_counts().head(n)
    return clienti_top
    print("Top 3 Clienti con più Prenotazioni:")
    print(top_n_clienti_con_piu_prenotazioni(df, 3))  

    incasso_medio_per_categoria = df.groupby('Categoria')['Incasso'].mean()
    durata_media_per_categoria = df.groupby('Categoria')['Durata'].mean()
    figura_ax1 = plt.subplots()
    ax1.bar(incasso_medio_per_categoria.index, incasso_medio_per_categoria.values, color='blue', marker= "o", label='Incasso Medio (€)')
    ax1.set_xlabel('Categoria')
    ax1.set_ylabel('Incasso Medio (€)', color='blue')
    ax2 = ax1.twinx()
    ax2.plot(durata_media_per_categoria.index, durata_media_per_categoria.values, color='red', marker='o', label='Durata Media (giorni)')
    ax2.set_ylabel('Durata Media (giorni)', color='red')
    plt.title('Incasso Medio e Durata Media per Categoria') 
    plt.show()