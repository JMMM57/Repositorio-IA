# Red Neuronal: Perceptrón Multicapa (MLP) en C

## Descripción del Proyecto
Este proyecto consiste en la implementación y extensión de una red neuronal artificial en lenguaje **C**. 

Inicialmente se contaba con un **Perceptrón Simple** diseñado para aprender funciones lógicas básicas. Para mejorar su arquitectura y permitirle procesar estructuras más complejas, el código se actualizó a un **Perceptrón Multicapa (MLP)** de 2 capas.

---

## Cambios

1. **Implementación de una Capa Oculta (2 Capas):**
   - Se añadió una **capa oculta** con 2 neuronas intermedias, convirtiendo la red en una arquitectura $2 \to 2 \to 1$ (2 entradas, 2 neuronas ocultas, 1 salida).

2. **Algoritmo de Aprendizaje:**
   - Se implementó la regla de la cadena para calcular los gradientes de error y propagarlos desde la capa de salida hacia la capa oculta.
   - Se incorporó la derivada de la sigmoide (`out * (1 - out)`) para ajustar los pesos ($W$) y sesgos (*bias*) mediante gradiente descendente.

3. **Entrenamiento para la Compuerta Lógica AND:**
   - Se configuró la tabla de entrenamiento en el `main` para resolver la operación **AND** (`(1,1)->1`, `(1,0)->0`, `(0,1)->0`, `(0,0)->0`).

---

## Estructura de la Red
* **Entradas ($x_0, x_1$):** 2 valores binarios.
* **Capa Oculta:** 2 neuronas con activación Sigmoide.
* **Capa de Salida:** 1 neurona con activación Sigmoide.
* **Tasa de aprendizaje ($K$):** `0.1`
* **Épocas:** `100,000`

---

## Compilación y Ejecución

Para compilar y ejecutar el código utilizando el compilador **GCC**:

```bash
# Compilar el código enlazando la librería matemática (-lm)
gcc perceptron.c -o perceptron -lm

# Ejecutar el programa (Windows)
.\perceptron.exe