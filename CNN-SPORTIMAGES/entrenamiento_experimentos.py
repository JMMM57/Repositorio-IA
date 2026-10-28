import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import tensorflow as tf

# Importar directo desde keras (resuelve el error de líneas 8 a 13)
import keras
from keras.models import Sequential
from keras.layers import (
    Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
)
from keras.utils import to_categorical
from keras import regularizers

# ==========================================
# 1. CARGA Y PREPROCESAMIENTO DEL DATASET
# ==========================================
# Ruta relativa directa dentro de CNN-SPORTIMAGES
DATASET_DIR = os.path.join("sportimages", "sportimages")
IMG_SIZE = (21, 28)  # Alto (filas), Ancho (columnas) según arquitectura original

images = []
labels = []

# Obtener carpetas de clases ignorando directorios de sistema como __MACOSX
class_names = [
    d for d in sorted(os.listdir(DATASET_DIR))
    if os.path.isdir(os.path.join(DATASET_DIR, d)) and not d.startswith(".") and not d.startswith("__")
]

print(f"Clases detectadas ({len(class_names)}): {class_names}")

for class_idx, class_name in enumerate(class_names):
    class_folder = os.path.join(DATASET_DIR, class_name)
    file_list = [f for f in os.listdir(class_folder) if not f.startswith(".")]
    print(f"Cargando {len(file_list)} imágenes de la clase: {class_name}...")
    
    for filename in file_list:
        file_path = os.path.join(class_folder, filename)
        img = cv2.imread(file_path)
        if img is not None:
            # Redimensionar al tamaño esperado por el modelo
            img_resized = cv2.resize(img, (IMG_SIZE[1], IMG_SIZE[0]))
            images.append(img_resized)
            labels.append(class_idx)

X = np.array(images, dtype="float32") / 255.0  # Normalización [0, 1]
y = np.array(labels)
y_cat = to_categorical(y, num_classes=len(class_names))

print(f"\nTotal imágenes procesadas: {X.shape[0]} con dimensiones {X.shape[1:]}")

# División Train / Test (80% entrenamiento, 20% prueba)
X_train, X_test, y_train, y_test = train_test_split(
    X, y_cat, test_size=0.20, random_state=42, stratify=y
)

# ==========================================
# 2. DEFINICIÓN DE LAS 5 VARIANTES DE CNN
# ==========================================
def construir_experimento(variante, input_shape, num_classes):
    model = Sequential()
    
    if variante == 1:
        # EXPERIMENTO 1: Base (Convolución 3x3 simple, Dropout estándar)
        model.add(Conv2D(32, (3, 3), padding='same', activation='relu', input_shape=input_shape))
        model.add(MaxPooling2D((2, 2)))
        model.add(Conv2D(64, (3, 3), padding='same', activation='relu'))
        model.add(MaxPooling2D((2, 2)))
        model.add(Flatten())
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.25))
        optimizer = keras.optimizers.Adam(learning_rate=0.001)

    elif variante == 2:
        # EXPERIMENTO 2: Convolución con Kernel más amplio (5x5) y mayor profundidad (128 filtros)
        model.add(Conv2D(32, (5, 5), padding='same', activation='relu', input_shape=input_shape))
        model.add(MaxPooling2D((2, 2)))
        model.add(Conv2D(64, (3, 3), padding='same', activation='relu'))
        model.add(MaxPooling2D((2, 2)))
        model.add(Conv2D(128, (3, 3), padding='same', activation='relu'))
        model.add(MaxPooling2D((2, 2)))
        model.add(Flatten())
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.25))
        optimizer = keras.optimizers.Adam(learning_rate=0.001)

    elif variante == 3:
        # EXPERIMENTO 3: Estabilización con Batch Normalization y Dropout agresivo (0.5)
        model.add(Conv2D(32, (3, 3), padding='same', activation='relu', input_shape=input_shape))
        model.add(BatchNormalization())
        model.add(MaxPooling2D((2, 2)))
        model.add(Conv2D(64, (3, 3), padding='same', activation='relu'))
        model.add(BatchNormalization())
        model.add(MaxPooling2D((2, 2)))
        model.add(Flatten())
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.5))
        optimizer = keras.optimizers.Adam(learning_rate=0.001)

    elif variante == 4:
        # EXPERIMENTO 4: Dinámica de pesos con Optimizador SGD + Momentum
        model.add(Conv2D(32, (3, 3), padding='same', activation='relu', input_shape=input_shape))
        model.add(MaxPooling2D((2, 2)))
        model.add(Conv2D(64, (3, 3), padding='same', activation='relu'))
        model.add(MaxPooling2D((2, 2)))
        model.add(Flatten())
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.25))
        optimizer = keras.optimizers.SGD(learning_rate=0.01, momentum=0.9)

    elif variante == 5:
        # EXPERIMENTO 5: Regularización L2 en los pesos de la capa densa ampliada (256 neuronas)
        model.add(Conv2D(32, (3, 3), padding='same', activation='relu', input_shape=input_shape))
        model.add(MaxPooling2D((2, 2)))
        model.add(Conv2D(64, (3, 3), padding='same', activation='relu'))
        model.add(MaxPooling2D((2, 2)))
        model.add(Flatten())
        model.add(Dense(256, activation='relu', kernel_regularizer=regularizers.l2(0.001)))
        model.add(Dropout(0.3))
        optimizer = keras.optimizers.Adam(learning_rate=0.0005)

    model.add(Dense(num_classes, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])
    return model

# ==========================================
# 3. BUCLE DE EJECUCIÓN (5 CORRIDAS)
# ==========================================
EPOCHS = 15
BATCH_SIZE = 64
input_shape = (IMG_SIZE[0], IMG_SIZE[1], 3)
num_classes = len(class_names)

resultados = {}
historiales = {}

nombres_experimentos = {
    1: "Exp 1: Baseline Adam",
    2: "Exp 2: Kernel 5x5 + Bloque 128",
    3: "Exp 3: Batch Normalization + Dropout 0.5",
    4: "Exp 4: SGD con Momentum",
    5: "Exp 5: Regularización L2 + Densa 256"
}

for i in range(1, 6):
    print(f"\n{'='*50}")
    print(f"Iniciando {nombres_experimentos[i]} (Corrida {i}/5)")
    print(f"{'='*50}")
    
    modelo = construir_experimento(i, input_shape, num_classes)
    
    history = modelo.fit(
        X_train, y_train,
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        validation_split=0.15,
        verbose=1
    )
    
    # Evaluación en conjunto de prueba independiente
    loss_test, acc_test = modelo.evaluate(X_test, y_test, verbose=0)
    resultados[nombres_experimentos[i]] = (loss_test, acc_test)
    historiales[nombres_experimentos[i]] = history.history
    
    print(f"--> Resultado {nombres_experimentos[i]}: Test Loss = {loss_test:.4f}, Test Accuracy = {acc_test:.4f}")

# ==========================================
# 4. TABLA COMPARATIVA FINAL
# ==========================================
print("\n" + "="*60)
print(f"{'EXPERIMENTO':<42} | {'TEST LOSS':<10} | {'TEST ACCURACY':<12}")
print("="*60)
for exp_name, (loss_t, acc_t) in resultados.items():
    print(f"{exp_name:<42} | {loss_t:<10.4f} | {acc_t * 100:<11.2f}%")
print("="*60)

# ==========================================
# 5. GENERACIÓN DE GRÁFICAS COMPARATIVAS
# ==========================================
plt.figure(figsize=(14, 5))

# Gráfica de Precisión de Validación
plt.subplot(1, 2, 1)
for exp_name, hist in historiales.items():
    plt.plot(hist['val_accuracy'], label=exp_name)
plt.title('Precisión en Validación (Val Accuracy)')
plt.xlabel('Época')
plt.ylabel('Accuracy')
plt.grid(True)
plt.legend()

# Gráfica de Pérdida de Validación
plt.subplot(1, 2, 2)
for exp_name, hist in historiales.items():
    plt.plot(hist['val_loss'], label=exp_name)
plt.title('Pérdida en Validación (Val Loss)')
plt.xlabel('Época')
plt.ylabel('Loss')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.savefig('comparativa_experimentos_cnn.png')
print("\nGráfica guardada como 'comparativa_experimentos_cnn.png'.")
plt.show()