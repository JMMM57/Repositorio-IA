# EXAMEN TEÓRICO — PERCEPTRÓN, MLP Y CNN

---

## 1. Datos del alumno

|  |  |
| :--- | :--- |
| **Nombre** | Juan Manuel Martinez Martinez |
| **Grupo** | B |
| **Fecha** | 11/03/2026 |

---

## 2. Pregunta 1 — Por qué no basta “una sola neurona”

1. **Regla de decisión:** El perceptrón toma múltiples valores de entrada, multiplica cada uno por un peso que define su importancia, suma estos productos junto a un sesgo (*bias*) y evalúa el total frente a un umbral; si la suma rebasa el umbral emite una decisión (por ejemplo, clase 1), y si no, emite la otra (clase 0).
2. **Frontera lineal:** Es un corte recto y plano que divide el espacio en dos mitades perfectas. Asume que todos los ejemplos de una categoría quedan estrictamente a un lado de la línea y los de la otra categoría en el lado contrario.
3. **Ejemplo donde no alcanza:** Clasificar clientes según edad y gasto en una tienda de ropa: los clientes como los adolescentes con presupuestos bajos y los adultos mayores con presupuestos altos, mientras que la población de mediana edad con gasto medio no compra. Al estar intercalados en diagonales opuestas, ninguna línea recta puede aislar a los compradores de los no compradores.

---

## 3. Pregunta 2 — CNN: de píxeles a mapas

1. **Problema de estructura espacial:** Al aplanar la imagen en un vector unidimensional largo, se pierde por completo la noción de vecindad 2D. Un MLP trata a dos píxeles contiguos igual que a dos píxeles en extremos opuestos, ignorando que los patrones visuales dependen de la relación local entre vecinos.
2. **Aplicar el mismo filtro en toda la imagen:** Significa que el detector de una característica particular usa la misma matriz de pesos sin importar en qué coordenada de la foto se encuentre. Esto confiere *invarianza a la traslación* y reduce exponencialmente el número de parámetros a entrenar.
3. **Dos usos adicionales:**
   - **Imágenes médicas:** Detección y segmentación de lesiones, tumores o microfracturas en radiografías y tomografías computarizadas.

---

## 4. Pregunta 3 — Softmax, clases y decisiones

1. **Binario vs. Multiclase:**
   - En un problema binario se suele usar una sola neurona de salida con activación sigmoide que predice un valor escalar continuo en el intervalo $[0, 1]$.
   - En un problema multiclase mutuamente excluyente se utiliza una capa de salida con tantas neuronas como categorías existan, reguladas por una función Softmax.
2. **Lectura de probabilidades de Softmax:** Indican el nivel de certidumbre o confianza que el modelo le asigna a cada opción. Todos los valores deberian ser positivos y la suma de todas las componentes del vector resultante es igual a 1 (100%).
3. **Arquitectura de salida recomendada:** 

---

## 5. Pregunta 4 — MLP: profundidad con sentido

1. 
2. **Riesgo de una red demasiado grande:** Sobreajuste (*overfitting*). El modelo posee tanta capacidad expresiva que termina memorizando el ruido y los casos particulares del conjunto de entrenamiento, perdiendo la habilidad de generalizar ante datos no vistos.
3. **Representaciones intermedias en palabras simples:** Las capas ocultas actúan como traductores sucesivos: toman variables crudas difíciles de interpretar directamente y las combinan en conceptos o pistas intermedias más sencillos de clasificar para la capa final.

---

## 6. Pregunta 5 — Entrenamiento sin magia

1. **Época a nivel intuitivo:** Es el ciclo completo durante el cual la red neuronal ha revisado, evaluado y ajustado sus pesos pasando por todos y cada uno de los ejemplos del conjunto de entrenamiento exactamente una vez.
2. **Objetivo al minimizar el error:** Los pesos se dirigen hacia el punto mínimo de la superficie de la función de pérdida; es decir, buscan el conjunto de valores que minimiza la distancia entre las predicciones del modelo y las etiquetas reales.
3. **Síntomas de un learning rate inadecuado:**
   - **Demasiado grande:** Los pasos de actualización son gigantes; la función de pérdida oscila caóticamente, no converge y puede dispararse.
   - **Demasiado chico:** La red avanza a pasos microscópicos; el entrenamiento toma demasiado tiempo, el error apenas disminuye entre épocas y corre el riesgo de quedarse atascada en regiones planas.

---

## 7. Pregunta 6 — Bloques de una CNN

1. **Kernel / filtro convolucional:** Funciona como una pequeña ventana deslizante especializada en rastrear y resaltar patrones visuales locales concretos.
2. **Función de activación:**
3. **Max pooling:** Reduce la resolución espacial de los mapas de características al quedarse únicamente con la señal más fuerte de cada región, disminuyendo el costo computacional.
4. **Capa densa + softmax al final:** La capa densa reúne y conecta todas las características aisladas extraídas previamente para construir un razonamiento global, y Softmax transforma esos valores finales en probabilidades para decidir la clase ganadora.

---

## 8. Pregunta 7 — XOR y la historia del aprendizaje

1. **Contraejemplo famoso:**
2. **Elemento del MLP que lo resuelve:** Capas ocultas con funciones de activacion no lineales.
3. **Cuándo usar un perceptrón / modelo lineal:** En problemas tabulares directos donde se necesita maxima rapidez y entender examente que peso tiene cada variable.

---

## 9. Pregunta 8 — De lo simple a lo abstracto en visión

1. **Tempranas vs. Profundas:** Las capas tempranas detectan elementos universales y simples; las capas profundas componen esos elementos en representaciones abstractas de alto nivel (siluetas completas, partes de objetos, rostros).
2. **Intuición para Transfer Learning:** Dado que las características de las capas tempranas normalmente son genéricas para casi cualquier imagen, se pueden congelar los pesos de una red ya entrenada en millones de fotos genéricas y reentrenar únicamente las últimas capas para el problema particular.
3. **CNN “profunda de más”:** Cuando la arquitectura cuenta con millones de parámetros para clasificar imágenes pequeñas o muy simples con pocas muestras.

---