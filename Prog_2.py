#Scenario reale
#Un centro di analisi mediche deve informatizzare parte della gestione dei pazienti, dei medici e dei referti di laboratorio. Si richiede la progettazione e la realizzazione di un programma in Python che permetta di gestire i dati in maniera strutturata, utilizzando programmazione a oggetti (OOP) e la libreria NumPy per l’elaborazione numerica dei dati clinici.
#Parte 1 – Variabili e Tipi di Dati
#Definire le variabili necessarie per rappresentare:Nome, cognome e codice fiscale di un paziente (stringhe).Età e peso del paziente (interi e float).Lista delle analisi effettuate (lista di stringhe).
#Esempio:nome = "Mario" cognome = "Rossi" eta = 45 peso = 78.5 analisi = ["emocromo", "glicemia", "colesterolo"]
#Scrivere almeno 3 pazienti diversi con queste variabili.
#Creare una classe Paziente con:Attributi: nome, cognome, codice_fiscale, eta, peso, analisi_effettuate.Metodo scheda_personale() che restituisca una stringa con i dati principali del paziente.Creare una classe Medico con:Attributi: nome, cognome, specializzazione.Metodo visita_paziente(paziente) che stampi quale medico sta visitando quale paziente.Creare una classe Analisi che contenga:Tipo di analisi (es. glicemia, colesterolo).Risultato numerico.Metodo valuta() che stabilisca se il valore è nella norma (criteri inventati da voi).
#Supponiamo che il centro raccolga i risultati di un certo esame per 10 pazienti.Rappresentare i valori in un array NumPy.Calcolare con NumPy: media, valore massimo, valore minimo e deviazione standard.
#Aggiornare la classe Paziente inserendo un attributo risultati_analisi che sia un array NumPy contenente i valori numerici delle analisi svolte.Creare un metodo statistiche_analisi() che calcoli:Media dei valoriMinimo e massimoDeviazione standard utilizzando NumPy.
#Creare un piccolo programma principale (main) che:Inserisca almeno 3 medici e 5 pazienti.Ogni paziente deve avere almeno 3 risultati di analisi.Stampi la scheda di ogni paziente.Mostri quale medico visita quale paziente.Stampi le statistiche delle analisi per ciascun paziente.

import numpy as np

class Paziente:
    def __init__(self,nome,cognome,codice_fiscale,età,peso,analisi_effettuate):
        self.nome = nome
        self.cognome = cognome
        self.codice_fiscale = codice_fiscale
        self.età = età
        self.peso = peso
        self.analisi_effettuate = analisi_effettuate
        self.risultati_analisi = np.array([])

    def scheda_personale(self):
        return f"Nome: {self.nome}, Cognome: {self.cognome}, Codice fiscale: {self.codice_fiscale}, età: {self.età}"

class Medico:
    def __init__(self,nomeMedico,cognomeMedico,specializzazione):
        self.nomeMedico = nomeMedico
        self.cognomeMedico = cognomeMedico
        self.specializzazione = specializzazione


    def visita_paziente(self,paziente):
        return f"Visita effettuata da {self.nomeMedico} {self.cognomeMedico} al paziente {paziente.nome} {paziente.cognome}"
    
class Analisi:
    def __init__(self,tipo_analisi,risultati):
        self.tipo_analisi = tipo_analisi
        self.risultati = risultati

    def mostra_risultati(self):
        return f"Tipo di analisi: {self.tipo_analisi}, Risultati: {self.risultati}"
    
    def valuta(self):
        valutazione = []
        for risultato in self.risultati:
            if risultato < 50:
                valutazione.append("Basso")
            elif 50 <= risultato <= 100:
                valutazione.append("Normale")
            else:
                valutazione.append("Alto")
            return valutazione
        
    def statistiche_analisi(self):
        medio = np.median(self.risultati)
        massimo = np.max(self.risultati)
        minimo = np.min(self.risultati)
        deviazione_standard = np.std(self.risultati)

        return {
            "Media": medio,
            "Massimo": massimo,
            "Minimo": minimo,
            "Deviazione Standard": deviazione_standard
        }

def main():
    medici = []
    pazienti = []

    medico1 = Medico("Dr.Mario", "Bernini", "Radiologia")
    medico2 = Medico("Dott.sa Elisa", "Neri", "Urologia")
    medico3 = Medico("Dott. Filippo","Marcellini", "Endocrinologo")
    medici.extend([medico1, medico2, medico3])

    paziente1 = Paziente("Giacomo", "Bianchetti" "GCMBCT88FG1M893W", 36, 88.8, ["emocromo", "glicemia", "colesterolo"])
    paziente2 = Paziente("Mario", "Giustini", "GSTMRO77H04M082W", 45, 81.2, ["diabete", "glicemia", "colesterolo"])
    paziente3 = Paziente("Gino", "Verdi", "VRDGNO99H15L987I", 44, 72.4, ["emocromo", "glicemia", "colesterolo"])
    paziente4 = Paziente("Luca","Valeriani","VLRLCU99H15M082W", 26, 79.6, ["emocromo", "glicemia", "diabete"])
    pazienti.extend([paziente1, paziente2, paziente3, paziente4])

    if(len(medici) < 3 or len(pazienti) < 4):
        print("Errore: Medici o pazienti non sufficenti")
        return
    
    for paziente in pazienti:
        print(paziente.scheda_personale())
        for medico in medici:
            print(medico.visita_paziente(paziente))

            paziente.risultati_analisi = np.random.randint(40, 130, size=4)
        
        analisi = Analisi("Generale", paziente.risultati_analisi)
        print(analisi.mostra_risultati())
        print("Valutazione:", analisi.valuta())
        print("Statistiche:", analisi.statistiche_analisi())
    
    if __name__ =="__main__":
        main()
    
