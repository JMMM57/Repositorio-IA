# 10 Preguntas Redes Neuronales Convolucionales (CNN)

**Materia:** Inteligencia Artificial  
**Tema:** Redes Neuronales Convolucionales (CNN)  

---

## Evidencia de trabajo en clase (Preguntas 1 a 3)

A continuación se muestra el avance realizado en clase:

![Avance clase 1](<../images/Actividad 10 preguntas 1.jpg>)
![Avance clase 2](<../images/Actividad 10 preguntas 2.jpg>)

*(En caso de que las imágenes requieran codificación URL directa: `![Avance](../images/Actividad%2010%20preguntas%201.jpg)`)*

---

## Pregunta 4 — Formas: de volumen a vector

### Contexto
Tensor justo antes del Flatten: `(7, 7, 64)`.

### 1. Elementos resultantes del Flatten
$$\text{Total} = 7 \times 7 \times 64 = \mathbf{3{,}136\text{ valores}}$$

### 2. Parámetros de la siguiente Dense(32) con bias
* Entradas ($n_{in}$): $3{,}136$
* Salidas ($n_{out}$): $32$
* Pesos de conexión: $3{,}136 \times 32 = 100{,}352$
* Biases (uno por neurona de salida): $32$

$$\text{Total de parámetros} = 100{,}352 + 32 = \mathbf{100{,}384\text{ parámetros}}$$

### 3. Global Average Pooling (GAP)
* **Forma y valores:** Reduce cada matriz de características bidimensional de $7 \times 7$ a un único valor medio por canal. La salida tiene forma `(64,)` (un vector de **64 valores**).
* **Ventaja frente a Flatten:** 
  1. **Independencia de la resolución de entrada:** Permite que el modelo reciba imágenes de distintas dimensiones sin que cambie el tamaño de entrada a la siguiente capa densa.
  2. **Reducción masiva de parámetros:** Pasa de $3{,}136$ conexiones a solo $64$, eliminando el riesgo de sobreajuste severo en la transición espacial-vectorial.

---

## Pregunta 5 — Softmax y el error “casi seguro”

### Contexto
* Vector Softmax predicho: $P = [0.10, 0.05, 0.85]$  
* Clases: $[0: \text{inundación}, 1: \text{incendio}, 2: \text{tornado}]$  
* Etiqueta real (one-hot): $[0, 1, 0]$ ($\text{clase verdadera} = \text{incendio}$)

### 1. Clase predicha (`argmax`)
$$\operatorname{argmax}([0.10, 0.05, 0.85]) = 2 \implies \mathbf{Tornado}$$

### 2. Grado de certidumbre numérico
El modelo está **muy seguro de su error**:
* Asignó un **85%** ($0.85$) de probabilidad a la clase incorrecta (*tornado*).
* A la clase verdadera (*incendio*) solo le asignó un **5%** ($0.05$).
* La diferencia entre la clase predicha y la segunda opción es de 75 puntos porcentuales ($0.85 - 0.10 = 0.75$), lo que demuestra que no está dudando ni repartiendo probabilidad uniformemente.

### 3. Comportamiento de la Categorical Crossentropy
La pérdida será **muy alta**.  
*Justificación:* La pérdida de entropía cruzada para la muestra es:
$$\mathcal{L} = -\sum_{i} y_i \ln(P_i) = -\ln(P_{\text{incendio}}) = -\ln(0.05) \approx 2.996$$
La función $-\ln(p)$ crece asintóticamente a infinito conforme $p \to 0$. Al haber asignado una probabilidad casi nula ($0.05$) a la clase real, el castigo numérico impuesto por el logaritmo es elevado.

---

## Pregunta 6 — Padding, stride y “se me achicó la imagen”

### Contexto
Entrada: $32 \times 32$, Kernel: $5 \times 5$, 1 filtro, 1 canal.

### 1. Tabla de dimensiones de salida

| padding | stride | salida (alto×ancho) | Justificación matemática |
| :--- | :---: | :---: | :--- |
| **valid** | 1 | **28×28** | $\lfloor (32 - 5)/1 \rfloor + 1 = 27 + 1 = 28$ |
| **valid** | 2 | **14×14** | $\lfloor (32 - 5)/2 \rfloor + 1 = \lfloor 13.5 \rfloor + 1 = 14$ |
| **same** | 1 | **32×32** | Con $S=1$ y padding adecuado conserva la dimensión original: $32$ |

### 2. Problema con tres MaxPool(2×2) seguidos
Reducción de dimensiones espaciales:
$$32 \times 32 \xrightarrow{\text{Pool 1}} 16 \times 16 \xrightarrow{\text{Pool 2}} 8 \times 8 \xrightarrow{\text{Pool 3}} 4 \times 4$$
* **Problema:** Ocurre una **pérdida crítica de resolución espacial**. Un objeto pequeño o detalle fino que en la imagen original ocupaba un área de $4 \times 4$ píxeles colapsa a menos de $1 \times 1$ píxel en el tercer mapa de activación, provocando que la red pierda por completo la información de contornos locales y texturas necesarias para su clasificación.

---

## Pregunta 7 — Dropout: ¿dónde y para qué?

### 1. Dropout(0.5) en entrenamiento
En cada paso de optimización (propagación hacia adelante y hacia atrás), desactiva aleatoriamente el 50% de las conexiones de la capa.  
* En una capa de 32 neuronas, sobreviven en promedio:
$$32 \times (1 - 0.5) = \mathbf{16\text{ neuronas}}$$

### 2. Dropout durante inferencia (`predict`)
**No se apagan neuronas**. Durante la prueba o producción se utilizan todas las neuronas activas para aprovechar la capacidad global del ensamble implícito y asegurar resultados reproducibles y deterministas. Las activaciones se reescalan automáticamente para compensar el 100% de presencia.

### 3. Crítica al Dropout solo en la última época
No tiene sustento teórico ni práctico. Dropout previene la **co-adaptación compleja** obligando a que las neuronas aprendan representaciones independientes a lo largo de todo el proceso de optimización. Encenderlo de golpe en la última época únicamente distorsiona las representaciones consolidadas sin darle al optimizador el tiempo necesario para ajustar los pesos ante dicha restricción estocástica.

---

## Pregunta 8 — Diseño: 5 clases de animales

### 1. Última capa Dense y activación
* **Configuración:** **5 neuronas** con activación **Softmax**.
* **Justificación:** Se trata de un problema multiclase mutuamente excluyente. Softmax mapea los valores continuos (logits) a una distribución de probabilidades que suman exactamente $1$, donde cada salida representa la probabilidad condicional de pertenecer a una de las 5 especies.

### 2. Discrepancia de tamaño de entrada ($224 \times 224 \times 3$ vs $21 \times 28 \times 3$)
**Acción requerida antes del `fit`:**  
Se deben redimensionar (*resize*) y recortar (*crop*) todas las imágenes del conjunto de datos a una resolución de $21 \times 28$ píxeles mediante una tubería de preprocesamiento antes de suministrarlas al modelo.

### 3. Propuesta de mejora y síntoma
* **Mejora:** Implementar **Batch Normalization** tras cada convolución.
* **Síntoma en curvas train/val:** Oscilaciones drásticas en la pérdida o estancamiento temprano del entrenamiento debido a gradientes inestables y desajuste interno de covariables.

---

## Pregunta 9 — CNN vs MLP vs RNN

### 1. Elección de arquitectura por escenario
1. **Tabla de notas, faltas y horas:** **MLP**. Los datos son tabulares independientes sin una estructura secuencial ni relaciones de adyacencia espacial 2D.
2. **Fotos de semáforo:** **CNN**. La información crítica reside en la relación espacial local bidimensional entre píxeles y colores.
3. **Autocompletar código:** **RNN / Transformer**. El código es una secuencia lineal unidireccional con dependencias temporales y sintácticas de largo alcance.

### 2. MLP sobre la imagen del semáforo
* **¿Puede aprender?** Sí, un MLP con suficiente capacidad puede sobreajustar y memorizar las muestras de entrenamiento.
* **Qué se sacrifica:**
  * **Explosión de parámetros:** Se requieren matrices de pesos completas por cada píxel de entrada.
  * **Pérdida de invariancia a traslaciones:** Si el semáforo cambia levemente de posición dentro del encuadre, el MLP no lo reconocerá sin ejemplos idénticos en esas coordenadas exactas.

---

## Pregunta 10 — Experimento mental: mover un gato

### 1. CNN vs MLP ante traslaciones
La CNN cuenta con la propiedad de **equivarianza a traslaciones** gracias al mecanismo de **pesos compartidos**: el mismo kernel recorre toda la imagen buscando características locales (ojos, bigotes, bordes). Al desplazarse el gato 10 píxeles a la derecha, las mismas neuronas convolucionales se activarán exactamente igual, produciendo un mapa idéntico simplemente corrido en el espacio, el cual es integrado por el pooling final. Un MLP trata cada coordenada como una variable aislada con pesos desconectados del resto.

### 2. Rotación de 90° sin datos rotados
La CNN **no garantiza el acierto**. Las operaciones de convolución estándar son equivariantes ante traslaciones espaciales, pero no son invariantes a rotaciones significativas.  
* **Solución necesaria:** Aplicar **Data Augmentation** que incluya rotaciones aleatorias en el entrenamiento o ampliar el dataset con ejemplos reales en múltiples orientaciones.

### 3. Pregunta propuesta para evaluar a un compañero
> *"Si aumentamos al doble la resolución de la imagen de entrada (por ejemplo de $64 \times 64$ a $128 \times 128$), ¿cuántos parámetros adicionales tiene que aprender una capa Conv2D(32, kernel 3×3)? Justifica tu respuesta."*  
> *(Respuesta esperada: Cero parámetros adicionales; los pesos de un kernel dependen únicamente del tamaño del filtro y de los canales, no del tamaño de la imagen).*