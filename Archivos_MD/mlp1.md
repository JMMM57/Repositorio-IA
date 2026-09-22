# Análisis de Experimento: Entrenamiento Mínimo (2 Saltos) en MLP

## 1. Objetivo del Experimento
Evaluar el comportamiento y la capacidad de generalización de la red neuronal (`MLPClassifier`) al ser entrenada únicamente con **2 saltos manuales** y dejarse ejecutando durante **15 minutos en modo automático**.

---

# Análisis de Experimento: Entrenamiento Mínimo (2 Saltos) en MLP

## 1. Objetivo del Experimento
Evaluar el comportamiento y la capacidad de generalización de la red neuronal (`MLPClassifier`) al ser entrenada únicamente con **2 saltos manuales** y dejarse ejecutando durante **15 minutos en modo automático**.

---

## 2. Comportamiento Esperado

```text
[2 Saltos en Manual] ──> [Presionar 'T'] ──> ¿Acumuló >= 80 muestras?
                                                    │
                         ┌──────────────────────────┴──────────────────────────┐
                         ▼                                                     ▼
                      [ No ]                                                [ Sí ]
                         │                                                     │
         Bloqueo por falta de datos                          ┌─────────────────┴─────────────────┐
     (El juego exige más muestras)                           ▼                                   ▼
                                                      [Clase Única]                    [Dos Clases]
                                                             │                                   │
                                                  Modelo Trivial (No-salta)            Modelo Sobreajustado (Overfitting)
                                                             │                                   │
                                                             └─────────────────┬─────────────────┘
                                                                               ▼
                                                                  [15 Minutos en Modo AUTO]
                                                                               │
                                                                   Impactos y reinicios continuos


---

## 3. Posibles Escenarios al Entrenar (Tecla `T`)

| Escenario | Condición | Resultado al presionar `T` | Comportamiento en Modo AUTO (`A`) |
| :--- | :--- | :--- | :--- |
| **A. Muestras Insuficientes** | Menos de 80 *frames* registrados (< 2 seg. de juego). | **Error:** *"Necesitas más datos (>= 80)"*. | No permite activar el modo automático. |
| **B. Modelo Trivial** | Se alcanzan 80 muestras, pero solo capturó la clase `0` (suelo). | **Aviso:** *"Modelo trivial entrenado: SIEMPRE NO-SALTA"*. | El personaje permanece inmóvil en el suelo y la bala lo golpea continuamente. |
| **C. Modelo Sobreajustado** | Se capturan muestras de `0` y `1`, pero con variabilidad mínima. | **Éxito aparente:** Genera matriz con `Accuracy test`. | El personaje salta a destiempo o no salta ante velocidades de bala no vistas, generando colisiones en bucle. |

---

## 4. Conclusiones Clave

* **Ausencia de Aprendizaje Continuo:** La red neuronal no aprende de sus fallos durante los 15 minutos en automático; solo utiliza los pesos calculados en el momento exacto en que presionaste `T`.
* **Falta de Generalización:** Como la velocidad de la bala es aleatoria (`random.randint(-12, -6)`), 2 saltos no ofrecen suficientes combinaciones de `[velocidad, distancia]` para que la red entienda el momento exacto de despegue.
* **Resultado Visual:** Un ciclo repetitivo de **impactos de bala, reinicios instantáneos d