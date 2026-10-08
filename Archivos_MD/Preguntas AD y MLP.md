# Actividad: Árboles de Decisión y Redes Neuronales Multicapa

---

## Parte I. Conceptos y Definiciones

### Pregunta 1
**¿Qué es un árbol de decisión y cuál es su objetivo principal dentro de un problema de clasificación?**

* **Definición:** Un árbol de decisión es un modelo de aprendizaje automático que funciona de manera similar a un diagrama de flujo. Para tomar una decisión, realiza una serie de preguntas encadenadas sobre las características del dato por ejemplo: *¿el monto es mayor a $5,000?*.
* **Objetivo principal en clasificación:** Dividir un conjunto variado de datos en subgrupos cada vez más homogéneos, hasta asignar a cada registro una categoría definitiva mediante reglas lógicas y transparentes del tipo *“si ocurre X y luego ocurre Y, entonces pertenece a la clase Z”*.

---

### Pregunta 2
**Explique con sus propias palabras los siguientes elementos de un árbol de decisión:**

* **Nodo raíz:** Es el punto de partida del árbol la primera pregunta que se evalúa. Se selecciona porque es la variable que mejor divide el conjunto de datos desde el inicio.
* **Nodo interno:** Cualquier pregunta intermedia dentro del flujo del árbol. Evalúa una condición específica y dirige hacia un camino u otro según la respuesta.
* **Rama:** El enlace o camino que conecta los nodos. Representa el resultado directo de una condición.
* **Hoja:** El nodo terminal o punto de salida. No contiene más preguntas si no que  entrega directamente el resultado final o la clase asignada.

---

### Pregunta 3
**¿Qué es una red neuronal multicapa y qué función cumplen las siguientes capas?**

Una **red neuronal multicapa (MLP)** es un modelo computacional formado por capas de nodos interconectados. Su propósito es modelar relaciones numéricas complejas entre los datos de entrada y la salida esperada.

* **Capa de entrada:** Recibe directamente los datos o características originales del problema en formato numérico y los pasa hacia adelante sin transformaciones complejas.
* **Capa oculta:** Uno o más niveles intermedios donde ocurre el procesamiento principal. Aplica multiplicaciones numéricas (pesos) y funciones matemáticas para descubrir patrones abstractos que no son evidentes a simple vista.
* **Capa de salida:** Recibe los patrones procesados por las capas ocultas y los transforma en el veredicto final ya sea una probabilidad de pertenencia a una clase o un valor continuo.

---

### Pregunta 4
**¿Qué representan los pesos y los sesgos dentro de una red neuronal? Explique también por qué sus valores cambian durante el entrenamiento.**

* **Pesos ($w$):** Representan la **fuerza o importancia** que tiene una conexión entre dos neuronas. Si una variable influye mucho en el resultado, su peso asignado tendrá una mayor magnitud.
* **Sesgos ($b$):** Son valores constantes que se suman al cálculo de cada neurona. Permiten **desplazar la función de activación**, asegurando que la neurona pueda activarse o no según corresponda, incluso si las entradas son cero o muy bajas.
* **Por qué cambian durante el entrenamiento:** Al inicio, los pesos y sesgos se inicializan con valores al azar, por lo que el modelo comete muchos errores. Durante el entrenamiento, mediante algoritmos como retropropagación y descenso de gradiente, la red mide qué tan lejos estuvo de la respuesta correcta y ajusta gradualmente estos números para minimizar el margen de error.

---

### Pregunta 5
**¿Cuál es la principal diferencia entre la forma en que aprende un árbol de decisión y la forma en que aprende una red neuronal multicapa? Explique qué elementos aprende cada modelo.**

| Aspecto | Árbol de Decisión | Red Neuronal Multicapa |
| :--- | :--- | :--- |
| **Forma de aprender** | **Partición lógica recursiva:** Divide el espacio de datos paso a paso buscando el mejor umbral en una variable a la vez utilizando métricas de pureza como Gini. | **Optimización matemática continua:** Ajusta todos sus parámetros al mismo tiempo mediante cálculo diferencial para reducir una función de costo. |
| **Qué aprende** | Un conjunto estructurado de **umbrales y reglas condicionales** (*if/else*) sobre las variables originales. | Una matriz densa de **pesos y sesgos numéricos** que combinan las variables de entrada de forma no lineal. |

---

## Parte II. Análisis y Aplicación

### Pregunta 6
**Una institución bancaria desea desarrollar un sistema que detecte posibles compras fraudulentas con variables como monto, hora, ciudad, tipo de establecimiento, número de compras al día e historial.**

#### Ventajas y desventajas
* **Árbol de decisión:**
  * *Ventajas:* Alta interpretabilidad se puede revisar exactamente qué regla detonó la alerta y muy baja latencia en producción.
  * *Desventajas:* Dificultad para modelar patrones complejos entre múltiples variables continuas simultáneas y riesgo de sobreajuste si el árbol crece demasiado.
* **Red neuronal multicapa:**
  * *Ventajas:* Excelente capacidad para detectar correlaciones sutiles e interacciones no lineales entre el historial del usuario y el contexto de la transacción.
  * *Desventajas:* Funciona como una "caja negra" difícil justificar por qué se bloqueó una compra en específico y requiere mayor volumen de datos para entrenar.

#### Elección y justificación
Se seleccionaría la **red neuronal multicapa** como nmodelo principal debido a que los patrones de fraude son dinámicos y dependen de combinaciones multifactoriales complejas. No obstante, en un entorno de producción real suele respaldarse con un conjunto preliminar de reglas fijas coomo un árbol para bloqueos inmediatos indiscutibles por ejemplo: compras en dos ubicaciones diferentes con minutos de diferencia.

---

### Pregunta 7
**Una escuela quiere detectar estudiantes en riesgo de reprobar. Suponga que un árbol de decisión y una red neuronal obtienen prácticamente la misma precisión.**

**¿Qué otros factores tomaría en cuenta para elegir uno de los dos modelos? Justifique su respuesta.**


1. **Interpretabilidad y acción pedagógica:** Un tutor escolar no solo necesita la predicción, sino entender la causa falta de tareas, inasistencias o antecedentes previos para poder diseñar una estrategia de apoyo personalizada.
2. **Costo computacional y mantenimiento:** Un árbol de decisión consume mínimos recursos y es fácil de mantener o actualizar sin requerir infraestructura especializada.
3. **Transparencia ética:** Permite comunicar al estudiante y a sus tutores los motivos exactos del seguimiento sin caer en comclusiones erroneas.

* **Veredicto:** El **árbol de decisión** es la mejor opción; cuando el rendimiento empata, la simplicidad y la explicabilidad son prioridad.

---

### Pregunta 8
**Un hospital desarrolla un sistema para triaje prioritario. Una red neuronal obtiene mejores resultados que un árbol de decisión, pero resulta más difícil explicar cómo obtuvo su respuesta.**

**¿Considera que la mayor precisión es suficiente para elegir la red neuronal? Analice las consecuencias que podría tener esta decisión.**

* **Veredicto:** **No es suficiente.** En entornos médicos de soporte a la vida, una mayor precisión no justifica el uso de un modelo cuya lógica no puede comprobarse.
* **Consecuencias asociadas:**
  * **Riesgo en casos atípicos:** Si el sistema clasifica erróneamente a un paciente en estado crítico como baja prioridad, el personal médico no tiene manera de rastrear qué variable originó la falla.
  * **Rechazo por falta de confianza clínica:** El personal de salud difícilmente dara recomendaciones de una caja negra que contradigan su juicio profesional inmediato si el sistema no expone sus razones.
  * **Vulnerabilidad a correlaciones espurias:** Las redes pueden aprender patrones circunstanciales de los datos de entrenamiento como horarios de saturación del hospital en lugar de indicadores fisiológicos reales.

---

### Pregunta 9
**Una empresa de reparto quiere predecir si un pedido llegará tarde. Para determinado pedido, el árbol indica "Llegará a tiempo" y la red "Probablemente llegará tarde".**

**¿Cómo determinaría cuál de los dos modelos está realizando una mejor predicción? Explique qué información adicional debería analizar.**


1. **Nivel de certidumbre de la red:** Revisar la probabilidad estimada de la red distinguir que probabilidad de retraso se asigno.
2. **Inspección de la regla del árbol:** Revisar qué rama específica siguió el pedido en el árbol para comprobar si alguna variable crítica como clima o tráfico quedó fuera de los cortes de esa rama.
3. **Rendimiento histórico segmentado:** Comparar el desempeño previo de ambos modelos exclusivamente bajo condiciones similares a las del pedido en cuestión.
4. **Matriz de confusión y costo del error:** Evaluar qué fallo perjudica más la operación: reportar un retraso falso  o prometer entrega a tiempo y fallar al cliente.

---

### Pregunta 10
**Una empresa desarrolla dos sistemas para otorgamiento de crédito: un árbol de decisión (explicable) y una red neuronal (más precisa pero opaca).**

* **¿Cuál modelo utilizaría?:** El **árbol de decisión**.
* **Ventajas:** Cumplimiento con regulaciones financieras y de derechos del consumidor, facilidad de auditoría y reducción del riesgo de discriminación algorítmica.
* **Riesgos:** Menor tasa de acierto global frente a la red, lo que podría implicar rechazar a solicitantes viables *falsos rechazos* o asumir un margen ligeramente mayor de incumplimiento.
* **¿Es posible utilizar ambos?:** **Sí, mediante una arquitectura híbrida en cascada.** La red neuronal puede evaluar el nivel de riesgo en una primera etapa, mientras que un árbol de decisión o conjunto de reglas sobre ese puntaje verifica los criterios legales y genera los motivos formales de aprobación o rechazo.

---

## Conclusión: "No existe un algoritmo de Inteligencia Artificial que sea el mejor para todos los problemas"


* **Precisión vs. Interpretabilidad:** Los modelos con mayor capacidad matemática como las redes neuronales tienden a ser opacos, mientras que los modelos transparentes como los árboles ofrecen claridad a cambio de un techo de rendimiento ante datos complejos.
* **Cantidad de datos:** Las redes neuronales demandan grandes volúmenes de datos para generalizar bien; con conjuntos de datos reducidos o estructurados en tablas, los árboles suelen ser más estables y eficientes.
* **Complejidad del problema:** Datos estructurados con divisiones claras se resuelven de forma óptima con árboles; datos continuos, abstractos o no estructurados como imágenes, audio, texto exigen el uso de redes neuronales.
* **Consecuencias de una decisión incorrecta:** Cuando un error compromete vidas humanas, repercusiones legales o asignación de derechos, la trazabilidad del motivo de la decisión es más crítica que un incremento marginal en la precisión teórica.