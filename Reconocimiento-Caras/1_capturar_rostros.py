import os
import cv2 as cv

# -------------------------------------------------------------
# CAMBIA ESTE NOMBRE PARA CADA PERSONA: 'persona1', 'persona2' o 'persona3'
NOMBRE_PERSONA = "persona4"
# -------------------------------------------------------------

CARPETA_DESTINO = os.path.join("dataset", NOMBRE_PERSONA)
os.makedirs(CARPETA_DESTINO, exist_ok=True)

# Cargamos el archivo XML que acabamos de descargar en la misma carpeta
XML_PATH = "haarcascade_frontalface_default.xml"
face_cascade = cv.CascadeClassifier(XML_PATH)

if face_cascade.empty():
    print("ERROR: No se pudo cargar el archivo haarcascade_frontalface_default.xml local.")
    exit()

# En Windows cv.CAP_DSHOW acelera el inicio de la webcam
cap = cv.VideoCapture(0, cv.CAP_DSHOW)

if not cap.isOpened():
    print("ERROR: No se detectó ninguna cámara.")
    exit()

contador = 0
LIMITE_FOTOS = 1500

print(f"--> Capturando para: {NOMBRE_PERSONA}")
print("Mira a la cámara y mueve la cabeza lentamente...")

while True:
    ret, frame = cap.read()
    if not ret:
        print("No se pudo leer imagen de la cámara.")
        break

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(60, 60))

    for (x, y, w, h) in faces:
        rostro = gray[y:y+h, x:x+w]
        rostro_redimensionado = cv.resize(rostro, (150, 150), interpolation=cv.INTER_AREA)

        ruta_foto = os.path.join(CARPETA_DESTINO, f"rostro_{contador}.jpg")
        cv.imwrite(ruta_foto, rostro_redimensionado)
        contador += 1

        cv.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv.putText(frame, f"Fotos: {contador}/{LIMITE_FOTOS}", (x, y - 10),
                   cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    cv.imshow("Captura de Rostros (ESC para salir)", frame)

    if cv.waitKey(1) == 27 or contador >= LIMITE_FOTOS:
        break

cap.release()
cv.destroyAllWindows()
print(f"Completado: {contador} fotos guardadas en {CARPETA_DESTINO}")