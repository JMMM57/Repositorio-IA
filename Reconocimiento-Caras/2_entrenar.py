import os
import cv2 as cv
import numpy as np

DATA_SET = "dataset"

# Obtiene la lista de personas leyendo las carpetas que creaste
faces = sorted([f for f in os.listdir(DATA_SET) if os.path.isdir(os.path.join(DATA_SET, f))])
print("Personas encontradas para entrenar:", faces)

labels = []
faces_data = []
label = 0

print("\nCargando imágenes...")
for person in faces:
    person_path = os.path.join(DATA_SET, person)
    count = 0
    
    for img_name in os.listdir(person_path):
        img_path = os.path.join(person_path, img_name)
        img = cv.imread(img_path, cv.IMREAD_GRAYSCALE)
        
        if img is None:
            continue
        
        # Aseguramos que todas las imágenes tengan exactamente 150x150
        img = cv.resize(img, (150, 150), interpolation=cv.INTER_AREA)
        
        labels.append(label)
        faces_data.append(img)
        count += 1
        
    print(f"  -> {person} (ID {label}): {count} imágenes cargadas")
    label += 1

print(f"\nTotal de imágenes a procesar: {len(faces_data)}")
print("Entrenando modelo Eigenfaces (esto puede tardar 1 o 2 minutos con 6000 fotos)...")

# Crear y entrenar el modelo
face_recognizer = cv.face.EigenFaceRecognizer_create()
face_recognizer.train(faces_data, np.array(labels))

# Guardar el archivo XML entrenado
face_recognizer.write("laloEigenface.xml")
print("\n¡Entrenamiento completado!")
print("Archivo generado exitosamente: laloEigenface.xml")