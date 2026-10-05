# Comparativa: Árbol de Decisiones vs. Red Neuronal Multicapa (MLP)

En el aprendizaje automático, resolver un problema depende mucho del metodo que se elia. Tanto el **árbol de decisiones** como la **red neuronal multicapa (MLP)** son utilizados, pero abordan la lógica de manera totalmente distinta.

---

## 1. ¿Cómo funciona cada uno?

### Árbol de Decisiones
Funciona como un **diagrama de flujo interactivo**. El modelo toma decisiones dividiendo los datos mediante preguntas secuenciales y reglas condicionales claras:
> *¿El ingreso es mayor a $20,000?*  
> ├── **Sí** $\rightarrow$ *¿Tiene historial crediticio limpio?* $\rightarrow$ **Aprobado**  
> └── **No** $\rightarrow$ **Rechazado**

### Red Neuronal Multicapa (MLP)
Funciona mediante **capas de neuronas artificiales interconectadas** (capa de entrada, capas ocultas y capa de salida). En lugar de reglas booleanas explícitas, cada neurona recibe valores, los multiplica por pesos numéricos, les suma un sesgo y les aplica una función de activación matemática para calcular una probabilidad o resultado final.

---

## 2. Diferencia Principal

* **Árbol de decisiones:** Divide los datos en bloques mediante condiciones directas sobre cada variable individual.
* **Red neuronal:** Modela limites de decisión curvas, continuas y complejas combinando todas las variables a la vez mediante álgebra y cálculo.

---

## 3. Pros y Contras

### Árbol de Decisiones

#### Pros:
* **Fácil de interpretar:** Cualquier persona puede inspeccionar el diagrama y entender exactamente por qué se tomó una decisión.
* **Poco preprocesamiento:** No necesita que los datos estén normalizados ni estandarizados; maneja datos numéricos y categóricos de forma natural.
* **Rápido y ligero:** Su entrenamiento requiere muy poca capacidad de cómputo.

#### Contras:
* **Tendencia al sobreajuste:** Si crece demasiado sin control, memoriza los datos de entrenamiento y falla con datos nuevos.
* **Inestabilidad:** Un pequeño cambio en los datos de entrada puede cambiar por completo la estructura del árbol.
* **Limitado en relaciones complejas:** Le cuesta modelar interacciones suaves y continuas entre muchas variables.

---

### Red Neuronal Multicapa (MLP)

#### Pros:
* **Alta capacidad de modelado:** Capaz de aprender prácticamente cualquier patrón o relación matemática no lineal compleja.
* **Escala excelente con muchos datos:** Con grandes volúmenes de información, suele superar ampliamente la precisión de un árbol individual.
* **Versatilidad:** Es la base para arquitecturas más avanzadas en visión por computadora, audio o texto.

#### Contras:
* **Caja negra:** Es muy difícil explicar el motivo exacto detrás de una predicción específica (difícil de auditar en sectores regulados como banca o medicina).
* **Requiere mucho preprocesamiento:** Exige normalización/escalado estricto de variables para converger adecuadamente.
* **Alto costo computacional:** Necesita más tiempo de entrenamiento, hardware más potente y ajuste cuidadoso de hiperparámetros (tasa de aprendizaje, épocas, funciones de activación).
* **Poco eficiente con datasets pequeños:** Tiende a rendir por debajo de modelos clásicos si no cuenta con suficiente volumen de datos.

---

## 4. Cuadro Comparativo Rápido

| Criterio | Árbol de Decisiones | Red Neuronal Multicapa (MLP) |
| :--- | :--- | :--- |
| **Lógica** | Reglas condicionales (*if-then*) | Transformaciones matemáticas continuas |
| **Interpretabilidad** | Muy alta | Muy baja |
| **Preprocesamiento requerido** | Mínimo | Obligatorio (escalado/normalización) |
| **Costo computacional** | Muy bajo | Medio a alto |
| **Uso ideal** | Reglas de negocio auditables, datos tabulares medianos | Patrones complejos, datasets masivos |