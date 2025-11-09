#Parte 1: Variabili e tipi di dati:
#Dichiarare e stampare alcune variabili di esempio:
#Titolo di un libro (stringa)
#Numero di copie disponibili(intero)
#Prezzo medio di un libro(float)
#Stato disponibile/non disponibile (booleano)(Es: titolo "Il Sig.degli anelli", copie = 5 ecc.)

libro = "il tesoro segreto dei Nazisti"
N_copie = 5 
P_medio = 15.80 
Stato_disponibile = (N_copie > 0 )
Stato_non_disponibile = (N_copie < 0 )

print(libro)
print(N_copie)
print(P_medio)
print(Stato_disponibile)
print(Stato_non_disponibile)


#Parte 2: Strutture dati
#Creare una lista con almeno 5 titoli di libri.
#Creare un dizionario che mappi il titolo del libro al numero di copie disponibili.
#Creare un insieme (set) che contenga tutti gli utenti registrati alla biblioteca.

libri = ["Signore degli Anelli","Harry Potter","Niente di nuovo sul fronte Occidentale","Viva lo sport","I tesori della WW2"] 

Dizionario = {
    "Signore degli anelli": "8",
    "Harry Potter": "12",
    "Niente di nuovo sul fronte occidentale": "7",
    "Viva lo sport": "1",
    "I tesori della WW2":"6",
}

print(libri)

for titolo, copie in Dizionario.items():
    
    print(f"{titolo}: {copie} copie")


Utenti_registati = {"Lucio Izzo","Luca Martelli","Livio Neri"} 

#Parte 3: Creare una classe Libro con attributi:
#titolo, autore, anno, copie_disponibili.

class Libro:
    def __init__(self,titolo,autore,anno,copie_disponibili):

        self.titolo = titolo

        self.autore = autore

        self.anno = anno

        self.copie_disponibili = copie_disponibili

#Aggiungere un metodo info() che restituisca una stringa descrittiva del libro.

def info(self):
    
    return f"Titolo : {self.titolo}, Autore : {self.autore}, Anno : {self.anno}, copie_disponibili: {self.copie_disponibili}"

#Creare una classe Utente con attributi: nome, età, id_utente

class Utente:

    def __init__(self,nome,età,id_utente):

        self.nome = nome

        self.età = età

        self.id_utente = id_utente

#Aggiungere un metodo scheda() che stampi i dati dell’utente.
#Creare una classe Prestito che colleghi un Utente a un Libro e contenga:
#utente (oggetto Utente)
# libro (oggetto Libro)
# giorni (numero di giorni del prestito)
#Aggiungere un metodo dettagli() che stampi tutte le informazioni sul prestito

def scheda(self):
    
    return (f" Utente: {self.nome}, {self.età}, {self.id_utente}")

class Prestito:

    def __init__(self,utente,libro,giorni):

        self.utente = utente

        self.libro = libro

        self.giorni = giorni

    def dettagli(self):

        return(f"{self.utente.nome} ha preso in prestito {self.libro.titolo} per {self.giorni}")
    
#Parte 4:Creare una funzione presta_libro(utente, libro, giorni) che:
# Verifichi se il libro ha almeno 1 copia disponibile
# Se sì → riduca il numero di copie e crei un nuovo oggetto Prestito
# Se no → stampi un messaggio di errore
# Simulare almeno 3 prestiti con utenti e libri diversi.
# Stampare a video:
#L’elenco aggiornato delle copie disponibili per ciascun libro
#I dettagli di ogni prestito effettuato

def presta_libro(utente,libro,giorni):
    if libro.copie_disponibili > 0:
        libro.copie_disponibili -= 1
        prestito = Prestito(utente,libro,giorni)
        return prestito
    else:
        print(f"Nessuna copia disponibile per il libro {libro.titolo}")
        return None

l1 = Libro("Signore degli Anelli", "J.R.R.", 1988, 8)
l2 = Libro("Harry Potter", "J.K.Rowling", 2001, 12)
l3 = Libro("Niente di nuovo sul fronte Occidentale", "Erich Maria Remarque", 1929, 7)

u1 = Utente("Lucio Izzo", 36, "ut1")
u2 = Utente("Luca Martelli", 26, "ut2")
u3 = Utente("Livio Neri", 44, "ut3")

prestito1 = presta_libro(u1, l1, 6)
prestito2 = presta_libro(u2, l2, 9)
prestito3 = presta_libro(u3, l3, 5)

for p in [prestito1,prestito2,prestito3]:
    if p:
        print(p.dettagli())

def nuove_copie_disponibili(libri):
    for libro in libri:
        print(f"{libro.titolo}: Copie disponibili : {libro.copie_disponibili}")

libri = [l1,l2,l3]
nuove_copie_disponibili(libri)