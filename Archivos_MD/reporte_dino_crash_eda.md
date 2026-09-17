# Reporte EDA — Operación Dino Crash

## 1. Planteamiento del problema y captura de datos (Misión 1)

### Estrategia de Obtención del Dataset
Para programar un modelo Perceptrón, el dataset no nos lo inventamos, lo debemos obtener mediante **telemetría/scripts de captura de eventos**:
* Se registra un estado por cada frame.
* Cada fila guarda las condiciones exactas del entorno en ese instante ($X$) y la acción/consecuencia observada ($Y$).

---

### Definición de Escenarios para la Red Neuronal

#### P1 — ¿Morirá en el siguiente frame?
* **Entradas (X - Nodos de Entrada del Perceptrón):**
  1. `distancia_obstaculo`: Distancia al obstáculo normalizada (0 a 1).
  2. `velocidad`: Velocidad actual del juego.
  3. `dino_y`: Posición vertical del dinosaurio (para saber si está en el aire o en el suelo).
  4. `altura_obstaculo`: Altura del obstáculo (distingue pájaros voladores de cactus).
  5. `agachado`: Variable binaria (0 = normal, 1 = agachado).
* **Salida (Y - Nodo de Salida):**
  * `tiempo_muerte`: Binario (0 = Sobrevive, 1 = Muere en el siguiente frame).
* **Granularidad:** 1 fila por frame.
* **Tamaño mínimo:** ~100,000 filas (aprox. 300 partidas).

#### P2 — ¿Cuántos puntos alcanzará esta partida al morir?
* **Entradas (X):**
  1. `tiempo_reaccion`: Tiempo promedio de reacción del jugador o bot.
  2. `frecuencia_saltos`: Número de saltos por minuto.
  3. `velocidad_inicial`: Velocidad con la que comenzó la sesión.
  4. `obstaculos_pasados`: Cantidad de obstáculos superados exitosamente.
  5. `experiencia_jugador`: Nivel o categoría del jugador.
* **Salida (Y):**
  * `puntuacion_final`: Valor numérico continuo (Puntuación final al chocar).
* **Granularidad:** 1 fila por partida completa.
* **Tamaño mínimo:** ~1,000 a 2,000 partidas finalizadas.

#### P3 — ¿Qué tipo de obstáculo viene próximo?
* **Entradas (X):**
  1. `puntuacion_actual`: Puntuación actual (a mayor score, cambia el generador aleatorio).
  2. `tiempo_desde_ultimo_obstaculo`: Tiempo transcurrido desde la última aparición de un obstáculo.
  3. `velocidad_global`: Velocidad del mapa.
  4. `ultimo_obstaculo_tipo`: Tipo de obstáculo que acaba de pasar.
  5. `nivel_dificultad`: Nivel interno de dificultad configurado.
* **Salida (Y):**
  * `siguiente_obstaculo`: Categórica codificada (Ej. 0 = Ninguno, 1 = Cactus Pequeño, 2 = Cactus Grande, 3 = Pájaro).
* **Granularidad:** 1 fila por cada evento de generación de obstáculo.
* **Tamaño mínimo:** ~5,000 eventos registrados.

---

## 2. Análisis del Diccionario y Muestra de Datos (Misión 2)

* **Análisis de la colisión (Frame 82 - `tiempo_muerte = 1`):** 
  En el frame 82 vemos que `distancia_obstaculo = 12 px` (muy cerca), `velocidad = 6.8`, el obstáculo es un `cactus_pequeno` y `salto = 0`. El dinosaurio colisionó porque estaba en el suelo cuando el obstáculo ya estaba encima.
* **¿Es `puntuacion_actual` útil para predecir la muerte inmediata?**
  No. La puntuación es simplemente un contador de tiempo acumulado. Un Perceptrón que use la puntuación como peso principal aprenderá falsamente que "a mayor puntaje, mayor probabilidad de morir", cuando en realidad la muerte es provocada por la falta de espacio físico para saltar (`distancia_obstaculo` y `salto`).
* **Variables críticas faltantes para alimentar el Perceptrón:**
  1. `dino_y`: Posición en el eje Y del dinosaurio.
  2. `altura_obstaculo`: Posición en el eje Y o altura del obstáculo.
  3. `agachado`: Si el personaje está agachado.

---

## 3. Consideraciones de Analista de Datos (Misión 3)

### Respuestas al Checklist EDA
1. **Valores Faltantes (NA):** Cuando no hay un obstáculo visible en pantalla, `distancia_obstaculo` no puede ser `null` o `0` (un 0 indicaría choque). Se debe imputar un valor máximo fijo (ej. `999 px`) antes de escalar a la red neuronal.

### El problema de los datos NO i.i.d.
Los frames de una partida tienen dependencia temporal estricta. Si mezclamos de forma aleatoria frames de la misma partida entre el grupo de entrenamiento (*Train*) y validación (*Test*), el Perceptrón simplemente memorizará la secuencia lineal de esa partida específica. 
* **Solución para la preparación:** La división entre *Train* y *Test* debe hacerse por partidas completas (`id_sesion`), nunca por filas sueltas.

### Ejemplo de Data Leakage
Si agregamos `total_frames_partida` o un indicador de "partida activa" como variable de entrada $X$ para predecir $Y$ (`tiempo_muerte`), el Perceptrón detectará que en la última fila ese estado cambia y "predecirá" la muerte con 100% de precisión sin haber aprendido nada sobre los cactus o el salto.

---

## 4. Interpretación Estadística del Dataset (Misión 4)

* **Desbalance Extremo de Clases:**
  De ~12,000 frames analizados, el dinosaurio solo muere en 50 frames ($tiempo\_muerte = 1$). Esto significa que el evento de interés es mu pequeño.
* **Comportamiento de `distancia_obstaculo`:**
  Las muertes se concentran en $distancia < 20 px$, mientras que la media global es $95 px$. Esto confirma que es la variable de entrada más determinante para activar la neurona de salida.

---

## 5. Justificación y Selección del Modelo (Misiones 5–6)

### Selección del Modelo: ¿Perceptrón Simple o Perceptrón Multicapa (MLP)?

| Escenario | Clasificación / Problema | Modelo Seleccionado | Justificación de la Red Neuronal |
| :--- | :--- | :--- | :--- |
| **P1 (Muerte en siguiente frame)** | Clasificación Binaria | **Perceptrón Multicapa (MLP)** | **No es linealmente separable.** La decisión de morir depende de la combinación no lineal de `distancia_obstaculo`, `velocidad` y `salto`. Un Perceptrón Simple no puede resolver este problema (falla tipo XOR). |
| **P2 (Puntaje final)** | Regresión Numérica | **Perceptrón Multicapa (MLP)** | La relación entre la habilidad del jugador, los saltos y el puntaje final presenta curvaturas y rendimientos decrecientes que requieren capas ocultas con funciones de activación relu/sigmoide. |
| **P3 (Tipo de obstáculo)** | Clasificación Multiclase | **Perceptrón Multicapa (MLP)** | Requiere múltiples nodos en la capa de salida (Softmax) para clasificar entre varias categorías independientes (`cactus`, `pájaro`, `ninguno`). |

---

## Opnicion Final

Para la realización de esta práctica, el dataset se obtendría mediante un **script de telemetría** que capture el estado de las variables por cada frame. 

Dado que la decisión para sobrevivir no se puede separar mediante una línea recta, el **Perceptrón Simple es insuficiente**, por lo que **se utilizará un Perceptrón Multicapa (MLP)** con variables previamente normalizadas ($0$ a $1$) debido al alto desbalance de las muertes.