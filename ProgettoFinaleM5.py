import json
import os
import tensorflow as tf
import tensorflow_datasets as tfds
from tensorflow.keras import layers, models
from sentence_transformers import SentenceTransformer, util
import torch

knowledge_data = {
    "baklava": {
        "name": "Baklava",
        "ingredients": ["Pasta fillo", "Noci tritate", "Pistacchi", "Sciroppo di miele", "Burro chiarificato"],
        "calories": 450,
        "description": "Dolce mediorientale stratificato, croccante e ricco di sciroppo di miele profumato agli agrumi."
    },
    "caesar_salad": {
        "name": "Caesar Salad",
        "ingredients": ["Lattuga romana", "Petto di pollo grigliato", "Crostini di pane", "Parmigiano Reggiano", "Salsa Caesar"],
        "calories": 350,
        "description": "Insalata fresca e leggera con pollo croccante, verdure fresche e una salsa cremosa saporita."
    },
    "lasagna": {
        "name": "Lasagna",
        "ingredients": ["Pasta all'uovo", "Ragù di carne", "Besciamella", "Parmigiano Reggiano"],
        "calories": 600,
        "description": "Piatto tradizionale italiano ricco e confortante a base di sfoglie di pasta, ragù e besciamella."
    },
    "ramen": {
        "name": "Ramen",
        "ingredients": ["Noodles", "Brodo saporito", "Pancia di maiale chashu", "Uovo marinato", "Alghe nori", "Cipollotti"],
        "calories": 520,
        "description": "Zuppa calda e avvolgente con noodles, brodo ricco di umami e condimenti misti."
    },
    "hamburger": {
        "name": "Hamburger",
        "ingredients": ["Pane da hamburger", "Carne di manzo", "Formaggio cheddar", "Lattuga", "Pomodoro", "Salse"],
        "calories": 700,
        "description": "Classico panino ricco e gustoso con carne succosa e formaggio fuso."
    },
    "sushi": {
        "name": "Sushi",
        "ingredients": ["Riso per sushi", "Pesce crudo (salmone/tonno)", "Alga nori", "Aceto di riso", "Wasabi"],
        "calories": 300,
        "description": "Piatto giapponese elegante, fresco e leggero a base di riso acidulato e pesce freschissimo."
    },
    "tiramisu": {
        "name": "Tiramisù",
        "ingredients": ["Savoiardi", "Caffè", "Mascarpone", "Uova", "Zucchero", "Cacao amaro in polvere"],
        "calories": 480,
        "description": "Celebre dolce al cucchiaio italiano cremoso, dolce e con una forte nota di caffè."
    },
    "pizza": {
        "name": "Pizza Margherita",
        "ingredients": ["Farina", "Pomodoro San Marzano", "Mozzarella di bufala", "Olio extravergine d'oliva", "Basilico fresco"],
        "calories": 800,
        "description": "La regina della cucina italiana: soffice base lievitata condita con pomodoro, mozzarella filante e basilico."
    },
    "french_fries": {
        "name": "Patatine Fritte",
        "ingredients": ["Patate", "Olio per frittura", "Sale fino"],
        "calories": 365,
        "description": "Bastoncini di patate dorati, croccanti fuori e morbidi dentro."
    },
    "ice_cream": {
        "name": "Gelato",
        "ingredients": ["Latte", "Panna", "Zucchero", "Frutta fresca o cioccolato"],
        "calories": 250,
        "description": "Dessert fresco, cremoso e dolce ideale per le giornate calde."
    }
}

json_filename = "food_knowledge.json"
with open(json_filename, "w", encoding="utf-8") as f:
    json.dump(knowledge_data, f, ensure_ascii=False, indent=4)

print(f"[OK] Database '{json_filename}' creato con successo.")


IMG_SIZE = 224
BATCH_SIZE = 16

def preprocess(image, label):
    image = tf.image.resize(image, (IMG_SIZE, IMG_SIZE))
    image = tf.cast(image, tf.float32) / 255.0
    return image, label

print("[INFO] Caricamento del dataset Food101 da TFDS (subset ridotto)...")
(ds_train, ds_test), ds_info = tfds.load(
    'food101',
    split=['train[:5%]', 'validation[:5%]'],
    as_supervised=True,
    with_info=True
)

ds_train = ds_train.map(preprocess, num_parallel_calls=tf.data.AUTOTUNE).shuffle(500).batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)
ds_test = ds_test.map(preprocess, num_parallel_calls=tf.data.AUTOTUNE).batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)

num_classes = 10

base_model = tf.keras.applications.MobileNetV2(
    input_shape=(IMG_SIZE, IMG_SIZE, 3),
    include_top=False,
    weights='imagenet'
)
base_model.trainable = False 

model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(num_classes, activation='softmax')
])

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

print("[INFO] Avvio addestramento rapido del modello di Computer Vision...")
history = model.fit(ds_train, validation_data=ds_test, epochs=2)

def get_food_metadata(predicted_label, json_path="food_knowledge.json"):
    with open(json_path, "r", encoding="utf-8") as f:
        db = json.load(f)
    
    return db.get(predicted_label.lower(), {
        "name": predicted_label,
        "ingredients": ["Informazioni non disponibili"],
        "calories": 0,
        "description": "Nessuna descrizione dettagliata trovata nel database."
    })

print("[INFO] Inizializzazione del modello Sentence-Transformer per la Ricerca Semantica...")
embedder = SentenceTransformer('all-MiniLM-L6-v2')

dishes_list = list(knowledge_data.keys())
dish_texts = [knowledge_data[d]["description"] for d in dishes_list]
dish_embeddings = embedder.encode(dish_texts, convert_to_tensor=True)

def semantic_mood_search(user_query, top_k=2):
    query_embedding = embedder.encode(user_query, convert_to_tensor=True)
    cos_scores = util.cos_sim(query_embedding, dish_embeddings)[0]
    top_results = torch.topk(cos_scores, k=min(top_k, len(dishes_list)))
    
    results = []
    for score, idx in zip(top_results.values, top_results.indices):
        dish_key = dishes_list[idx]
        results.append({
            "dish_id": dish_key,
            "similarity_score": round(score.item(), 4),
            "details": knowledge_data[dish_key]
        })
    return results

print("\n" + "="*50)
print("DEMO DI TEST DEL SISTEMA CHEFBOT AI")
print("="*50)

mock_prediction = "baklava"
metadata = get_food_metadata(mock_prediction)
print(f"\n[Modulo Visione + Lookup] Piatto identificato: {mock_prediction.upper()}")
print(f"-> Nome: {metadata['name']}")
print(f"-> Ingredienti: {', '.join(metadata['ingredients'])}")
print(f"-> Calorie: {metadata['calories']} kcal")
print(f"-> Descrizione: {metadata['description']}")

user_input = "voglio qualcosa di fresco e leggero"
print(f"\n[Modulo Ricerca Semantica] Query utente: \"{user_input}\"")
search_results = semantic_mood_search(user_input, top_k=2)
for i, res in enumerate(search_results, 1):
    print(f"  {i}. Suggerimento: {res['details']['name']} (Affinità: {res['similarity_score']})")
    print(f"     Descrizione: {res['details']['description']}")