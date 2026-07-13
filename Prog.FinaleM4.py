#Progetto Finale: Riconoscimento Gesti della Mano

#Titolo: Sviluppo di una CNN con Data Augmentation per Sasso, Carta, Forbice

import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image
import numpy as np
import matplotlib.pyplot as plt
import zipfile

with zipfile.ZipFile("rps.zip", "r") as z:
    z.extractall("/content/")

# Sostituiamo i percorsi con le cartelle da dove abbiamo estratto i dati
TRAINING_DIR = "/storage.googleapis.com/laurencemoroney-blog.appspot.com/rps.zip"
VALIDATION_DIR = "/storage.googleapis.com/laurencemoroney-blog.appspot.com/rps-test-set.zip"

# Estrae i dataset direttamente in Colab
unzip = "/storage.googleapis.com/laurencemoroney-blog.appspot.com/rps.zip"
unzip = "/storage.googleapis.com/laurencemoroney-blog.appspot.com/rps-test-set.zip"

# 1. ImageDataGenerator per il Training (con Data Augmentation)
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=40,
    width_shift_range=0.2,
    shear_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)


validation_datagen = ImageDataGenerator(rescale=1./255)

# 2. Caricamento in batch dalle directory
train_generator = train_datagen.flow_from_directory(
    TRAINING_DIR,
    target_size=(150, 150),
    class_mode='categorical',
    batch_size=32
)

validation_generator = validation_datagen.flow_from_directory(
    VALIDATION_DIR,
    target_size=(150, 150),
    class_mode='categorical',
    batch_size=32
)

model = tf.keras.models.Sequential([
    # Input: 150x150 pixel, 3 canali (RGB)
    tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(150, 150, 3)),
    tf.keras.layers.MaxPooling2D(2, 2),
    
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    
    tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    
    tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    
    # Flatten per convertire le matrici in vettori
    tf.keras.layers.Flatten(),
    
    # Livello denso da 512 neuroni
    tf.keras.layers.Dense(512, activation='relu'),
    
    # Output layer: 3 classi (Sasso, Carta, Forbice) con Softmax
    tf.keras.layers.Dense(3, activation='softmax')
])

model.summary() # Stampa l'architettura della rete

# 1. Definizione della Callback personalizzata
class myCallback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs={}):
        if(logs.get('accuracy') is not None and logs.get('accuracy') > 0.98):
            print("\nRaggiunto il 98% di accuratezza sul training set. Interrompo l'addestramento!")
            self.model.stop_training = True

callbacks = myCallback()

# 2. Compilazione del modello
model.compile(
    optimizer='rmsprop', # o 'adam'
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# 3. Addestramento (Training)
history = model.fit(
    train_generator,
    epochs=20,
    validation_data=validation_generator,
    callbacks=[callbacks]
)

def predict_image(image_path):
    # Caricamento e ridimensionamento a 150x150
    img = image.load_img(image_path, target_size=(150, 150))
    
    # Conversione in array e normalizzazione (1/255)
    x = image.img_to_array(img)
    x = x / 255.0 
    x = np.expand_dims(x, axis=0) # Aggiunge la dimensione del batch
    
    # Predizione
    classes = model.predict(x, batch_size=10)
    
    # L'ordine delle classi dipende da come le ha lette il generator (alfabetico)
    # Solitamente: 0=paper, 1=rock, 2=scissors
    class_labels = list(train_generator.class_indices.keys())
    predicted_index = np.argmax(classes[0])
    predicted_class = class_labels[predicted_index]
    
    print(f"\nRisultato predizione: {predicted_class.upper()}")
    
    # Visualizzazione immagine
    plt.imshow(img)
    plt.axis('off')
    plt.show()
