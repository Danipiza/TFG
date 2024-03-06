## TFG: Optimización usando técnicas de cómputo de alto rendimiento aplicado a la IA
---
#### Estudiante: Daniel Pizarro Gallego (GII)

#### Dirigido por: Alberto Núñez Covarrubias
---
## Índice

1. [MPI](#mpi)
2. [Aprendizaje por Refuerzo](aprendizaje-por-refuerzo)
3. [Programación Evolutiva](programación-evolutiva)
4. [Aprendizaje no Supervisado](aprendizaje-no-supervisado)
5. [Aprendizaje Supervisados](#aprendizaje-supervisado)

## Python
Es uno de los lenguajes más populares para la IA debido a su sintaxis sencilla, amplia variedad de bibliotecas de IA (como TensorFlow, PyTorch, scikit-learn, etc.) y una gran comunidad de desarrolladores. Pero es un lenguaje bastante lento, lo que provoca que a la hora de ejecutar el código tarde mucho tiempo en finalizar.

Voy a estar programando en python, y probando maneras de reducir el tiempo de ejecución.

### Mejoras
- **No usar recursión**
- **Manejo de Interrupciones**
- **División del Espacio de Búsqueda:** Se puede reducir el tiempo de ejecucion de lineal a logaritmico, produciendo, potencias de 2 o 10, hilos.
- **Cálculo ideal del Número de Workers:** Crear y gestionar demasiados hilos pueden generar un costo adicional, tanto en espacio como en tiempo.

---

## MPI
[MPI](https://mpi4py.readthedocs.io/en/stable/) es un estándar para una biblioteca de paso de mensajes. El objetivo es comunicar procesos en ordenadores remotos.

Actualmente hay varias implementaciones: [Open MPI](http://www.open-mpi.org/), [MPICH](http://www.mpich.org/) , [MVAPICH](http://mvapich.cse.ohio-state.edu/), [IBM Platform MPI](http://www.ibm.com/systems/es/platformcomputing/products/mpi/), [Intel MPI](https://www.intel.com/content/www/us/en/developer/tools/oneapi/mpi-library.html)

MPI 2.0 tiene más de 100 funciones. Se intercambia información usando paso de mensajes.

### La Ley de Amdahl (1967)
```
Acceleración = 1/((1-p) + p/n)
```
**Memoria Compartida:** Lecturas en paralelo, escrituras con exclusión mutua (Mutex). **1 Nodo, n procesos.**

**Memoria Distribuida** Un proceso sólo tiene acceso a su espacio de memoria. El proceso **X le envía al proceso Y datos**. **n Nodos, n procesos.**

Taxonomía de Flynn
- SISD (Single Instruction, Single Data stream) 
- SIMD (Single Instruction, Multiple Data streams) 
- MISD (Multiple Instruction, Single Data stream), Poco común 
- MIMD (Multiple Instruction, Multiple Data streams)

## Single Program Multiple Data (SPMD) 
**1 programa** ejecutado en paralelo. El mismo programa se **copia a todos los nodos**. Cada proceso tiene su propio su ID (Rank) 

![MPI](https://github.com/Danipiza/TFG/assets/98972125/9725df3b-60ba-4d4d-9726-0f5087f5c37b)

---

## Funciones 

### Funciones de Entorno
**Comunicador** agrupa los procesos en “comunicadores”. Los procesos que intercambian mensajes comparten comunicador ```comm=MPI.COMM_WORLD```

**Inicializar**. Establecer un entorno de MPI. Se invoca automáticamente al importar mpi4py, se puede hacer manual si se desactiva la configuracion base.
```
mpi4py.rc.initialize = False
MPI.Init()
```

**Finalizar**. Terminar el procesamiento de MPI. Tiene que ser la ultima llamada MPI. Se invoca automáticamente, se puede hacer manual si se desactiva la configuracion base.
```
mpi4py.rc.finalize = False
MPI.Finalize()
```

**Size**. Para comprobar el número de procesos relacionados con el comunicador (también cuenta el master). ```comm.Get_size()```

**Rank**. Para comprobar el ID (rank) del proceso asociado a un comunicador [0,(size-1)] ```comm.Get_rank()```

**Status**. Se utiliza para almacenar información sobre el mensaje recibido. Origen del mensaje, tag asociado, tamaño del mensaje. Es un objeto Status que proporciona esta información.

**MPI.ANY_SOURCE**. Se utiliza en funciones de recibir mensajes, especifica que recibe el mensaje de cualquier destinatario.

**Tag**. Es una etiqueta asociada con el mensaje que se envía. Es una forma de etiquetar los mensajes y es útil cuando estás implementando una comunicación entre múltiples procesos y necesitas distinguir entre diferentes tipos de mensajes.


**Abortar**. Fuerza la finalización de todos los procesos MPI. ```MPI_Abort()```


### Funciones Punto a Punto
Proceso **emisor y receptor** del mensaje

**SÍNCRONA**: El proceso **emisor espera** a que se realice el envío del mensaje. Comunicación **bloqueante**

**Enviar (sinc)** Envía un mensaje de forma síncrona. El mensaje _data_ lo envia un proceso y lo recibe el _dest_.
```comm.send(data, dest=, status=)```

**Recibir (sinc)** Recibe un mensaje de forma síncrona. El mensaje _data_ lo guarda en una variable el proceso que recibe desde _source_.
```data = comm.recv(source=, tag=, status=)```


**ASÍNCRONA**: El proceso emisor envía el mensaje y **continúa su ejecución** sin asegurarse de que el proceso receptor haya solicitado el mensaje. Comunicación **no bloqueante**

**Enviar (asinc)**. Envía un mensaje de forma asíncrona. Mensaje lo puede recibir un proceso mediante MPI_Recv o MPI_IRecv
```comm.Isend(data, dest=destino)```

**Recibir (asinc)**. Recibe un mensaje de forma asíncrona
```
data = comm.Irecv(source=, tag=, status=)
data.Wait() # De esta forma espera a recibir el mensaje
```
 
![Master_Worker](https://github.com/Danipiza/TFG/assets/98972125/bb3bb7ab-b896-4638-a83b-ec256823baf5)

---

## Aprendizaje por Refuerzo
### Reinforcement Learning
Se basa en experiencias y simulaciones, con prueba y error, recibiendo recompensas con las acciones tomadas (también pueden ser negativas). Nadie le dice al agente que hacer, toma las decisiones con diferentes estrategias. En la etapa de entrenamiento suele ser de forma aleatoria. Una vez tiene un feedback del entrenamiento se toma las decisiones maximizando las recompensas obtenidas en experiencias pasadas.

### Algoritmo Q-Learning:
Mezcla entre programación dinámica y Monte Carlo. R=Matriz de recompensas.
- R=Matriz de recompensas.
- Q=Matriz (Estados x Acciones). Que acción elegir en cada estado. (mayor valor)

Aprende el camino si es una buena acción, Back Propagation (Como en redes neuronales).

S=estado actual. A=acción tomada. S’=Estado siguiente. Ai=una acción.

```Q(S, A) = (1−α)*Q(S, A) + α*(R(S, A) + γ*maxi Q(S’, Ai))```

### Hiperparametros:

- α (tasa de aprendizaje): 
Debería disminuir a medida que continúa adquiriendo una base de conocimientos cada vez mayor.
- γ (factor de descuento): 
A medida que se acerca cada vez más al valor límite, su preferencia por la recompensa a corto plazo debería aumentar, ya que no estará el tiempo suficiente para obtener la recompensa a largo plazo, lo que significa que su gamma debería disminuir.
- ϵ:  Evita que la acción siga siempre la misma ruta.
A medida que desarrollamos nuestra estrategia, tenemos menos necesidad de exploración y más explotación para obtener más utilidad de nuestra política, por lo que en vez de utilizar un valor fijo, a medida que aumentan los ensayos, épsilon debería disminuir. Al principio un épsilon alto genera más episodios de exploración y al final un épsilon bajo explota el conocimiento aprendido.





### Mejorar 
Se puede lograr con varias estrategias. El contexto del problema es muy importante.

### Paralelización del entorno: 
Entrenando un agente en un entorno complejo, se puede dividir el proceso de entrenamiento en varios workers/hilos.
- Ejecutar en varios “workers“ el programa en la misma celda.
-	Ejecutar en varios “workers” el programa en diferentes celdas.
-	Ejecutar varios “workers” asignando secciones del mapa.
-	Recorrer la matriz Q e ir actualizando los valores

  
### Explotación y evaluación simultáneas: 
Además de explorar el entorno, puedes utilizar hilos para realizar simultáneamente la explotación (es decir, tomar decisiones basadas en el conocimiento actual del agente) y la evaluación (es decir, medir el desempeño del agente en el entorno). Esto puede acelerar el proceso de aprendizaje al permitir que el agente ajuste su estrategia más rápidamente.

### Optimización de Hiperparámetros: 
alpha, beta y gamma son los hiperparámetros que se usan para almacenar las experiencias del agente. Con vairos workers/hilos con diferentes hiperparámetros así comprobando de forma paralela cual sería la mejor configuracion. EJ, con técnicas como la **búsqueda aleatoria** u **optimización bayesiana distribuida** para encontrar la mejor configuración de hiperparámetros para el modelo de aprendizaje por refuerzo.

### Implementación Eficiente de Algoritmos: 
Hay algoritmos de aprendizaje por refuerzo, que se pueden paralelizar manera eficiente.

 [**A3C (Asynchronous Advantage Actor-Critic)**](https://www.activeloop.ai/resources/glossary/asynchronous-advantage-actor-critic-a-3-c/#:~:text=A3C%2C%20or%20Asynchronous%20Advantage%20Actor,form%20of%20rewards%20or%20penalties.)  visto en la asignatura IA1, básicamente el agente recibe un feedback de la operación que ha ejecutado, dando recompensas (si es negativa es una penalización).
 
 [**PPO (Proximal Policy Optimization)**](https://openai.com/research/openai-baselines-ppo)

---

## Programación Evolutiva

La programación evolutiva es una técnica de optimización inspirada en la teoría de la evolución biológica. Se basa en el concepto de selección natural y evolución de las poblaciones para encontrar soluciones a problemas complejos.

Una población está compuesta por individuos. Un individuo tiene un cromosoma, que tiene uno o varios genes, que a su vez cada gen tiene 1 o varios alelos. Los individuos se pueden representar: 
-	Binarios: Cada alelo es un bit. Los rangos de números naturales en binario son de 2N, para codificar un 127 en binario se necesitan 27 bits. Y si queremos añadir números reales con una cierta precisión este número de bits aumenta.
-	Reales: Números reales, este es más fácil de manejar.

El **fenotipo** (Decodificación) de un individuo son los rasgos observables, es decir el valor numérico. 

El **genotipo** (Codificación) es la composición genética de un individuo.



### Plantilla básica de una Algoritmo Evolutivo
``` 
poblacion = iniciar_poblacion(tam_poblacion)
evaluar_poblacion(poblacion)
while(<<condición>>):
  seleccion = seleccionar_poblacion()
  # Reproducción
  cruzar_poblacion(seleccion, prob_cruce)
  mutar_poblacion(seleccion, prob_muta)
  3 Elegir que individuos pasan a la siguiente generacion
  eleccion_poblacion(poblacion, seleccionados)
  evaluar_poblacion()
```
![PEV](https://github.com/Danipiza/TFG/assets/98972125/6eeb6388-e177-4f5c-bd92-73631620d6c3)

- Inicializar Población:
Para inicializar la población, se pasa por parámetro el tamaño de la poblacion, y se inicializan todos los Individuos.

Los Individuos suelen ser un array de bits, por lo que se recorre el individuo, es decir, el cromosoma y con un numero random se genera cada alelo del cromosoma.

Cada individuo puede tener muchos bits, debido a un tamaño de cromosoma elevado. Si tenemos muchos individuos y el tamaño del cromosoma es muy grande se puede distribuir la carga
de trabajo entre varios workers/hilos para que generen una parte y envien al master lo generado.

- Evaluar Población:
Para evaluar la población, se reciben los individuos de la población y se calcula su fitness, como de buenos son estos individuos para el problema a resolver.

La funcion de aptitud calcula el fitness, recibiendo el array de bits de un individuo. 

Dependiendo del problema, puede ser un calculo rápido con el fenotipo asociado al individuo, o un cálculo que requiera recorrer todo el array de bits. Se puede distribuir la carga de trabajo entre varios workers/hilos para calcular el fitness de una parte de la población. (Como a la hora de inicializar)

- Seleccionar Población:
Para seleccionar la poblacion, hay varios métodos, ruleta, torneo, estocástico universal...

Se recibe el fitness de la población y el método se encarga de elegir individuos, puede elegir a los mejores o elegir de manera justa.

Por ejemplo en el método de ruleta se selecciona un número de individuos de la población de manera aleatoria, pero teniendo en cuenta su adaptabilidad, por lo que los mejores individuos tienen más probabilidades de ser escogidos. Se puede realizar un distribucion para que varios workers/hilos seleccionen una parte de la población.

- Cruzar Población:
Una vez seleccionados los individuos de la población, con una probabilidad de cruce que se pasa por parámetro se seleccionan 2 individuos aleatorios y se cruzan dependiendo de la probabilidad, si no se quedan como están.

Hay varios métodos para el cruce, unos mas simples y otros más complejos. Por ello se puede gestionar este proceso con workers/hilos que reciban una parte de los individuos seleccionados y devuelvan esa parte una vez realizada el cruce.

- Mutar Población:
Cuando ya se han cruzado los elementos seleccionados estos pasan a una etapa de mutación, en la cual con una probabilidad de mutación, se recorre los alelos de los individuos seleccionados y cruzados para aplicar diversidad.

Al igual que con el cruce hay varios métodos, simples y complejos, que se pueden paralelizar con workers/hilos. 


---

## Aprendizaje no Supervisado

1. [Aglomerativo](#algoritmo-de-clustering-jerárquico-aglomerativo)
2. [KMedias](algoritmo-de-kmedias)

### Algoritmo de clustering jerárquico aglomerativo

```
-	FASE 1: Crear la matriz de distancias inicial D 
Es una matriz simétrica (basta con usar una de las matrices triangulares) - 
-	FASE 2: Agrupación de Individuos 
    o	Partición inicial P0: Cada objeto es un cluster 
    o	Calcular la partición siguiente usando la matriz de distancias D
        	Elegir los dos clusters más cercanos. Serán la fila y la columna del mínimo de la matriz D 
        	Agrupar los dos en un cluster. Eliminar de la matriz la fila y columna de los clusters agrupados. Generar la nueva matriz de distancias D. 
            •	Añadir una fila y una columna con el cluster nuevo 
            •	Calcular la distancia del resto de clusters al cluster nuevo 
    o	Repetir paso 2 hasta tener sólo un cluster con todos los individuos • Representar el dendograma (árbol de clasificación) 
La complejidad con los enlaces simple y completo tienen un coste cúbico O(n3). Existen implementaciones más eficientes (𝑛2).
```

 
### Algoritmo de KMedias: 
**Algoritmos de clustering basados en particiones**

Se fija un valor k. 
1. Inicializar los k centros (o centroides) de los clusters de forma aleatoria.
- Generando puntos aleatorios en el espacio dimensional
- Seleccionando aleatoriamente individuos
2. Repite el siguiente proceso hasta que los centros no cambien.

**Fase de asignación:** Para cada individuo se le asigna el cluster más cercano. Requiere el uso de una distancia (normalmente euclídea, también se puede usar manhattan o Chebychev)

**Actualiza el centro de los clusters.** Se calcula con la media de los individuos del Como los clusters se generan aleatoriamente, no siempre va a dar un buen resultado a la primera. Por lo que se pasa por parámetro cuantas veces **se repite hasta encontrar el mejor**. Encontrar el **valor ideal para k**.


---

## Aprendizaje Supervisado
1. [KNN](#knn)
2. [Redes Neuronales](redes-neuronales)

### Validacion Cruzada
1. Los datos se dividen aleatoriamente en k subconjuntos iguales 
2. Se entrena el conjunto con (k-1) y se valida con el restante 
3. Se repite k veces el paso 2, cambiando el conjunto que se usa para validar 
4. Como medida de error final se suele presentar la media de las k medidas de error de validación (aunque puede ser interesante comprobar que las k medidas sean similares)

![Validacion_Cruzada](https://github.com/Danipiza/TFG/assets/98972125/3f08fd2b-495e-48e2-846b-05c04d1a60cf)

### KNN
Es simple pero potente y se basa en la idea de que los puntos de datos similares tienden a agruparse en el espacio de características.
	1. Empezar con un dataset con categorías conocidas.
	2. Añadir un nuevo individuo con categoría desconocida.
	3. Clasificar el individuo con los k vecinos más cercanos.
Se puede aplicar a mapas de calor

No hay una forma de determinar el mejor valor para k, por lo que hay que probar con varias ejecuciones. valores pequeños de k crea sonido. Valores grandes con pocos datos hará que siempre sea la misma categoría


### Redes Neuronales
![Esquema_red](https://github.com/Danipiza/TFG/assets/98972125/cf25aa2b-00e0-45e7-877f-d97f891f1ec4)
-	La primera columna es la capa de entrada de la variable. 
-	La última columna es la capa de salida con todas las posibles salidas. 
-	Las columnas intermedias son las capas ocultas

Cada neurona hace una operación simple. Suma los valores de todas las neuronas de la columna anterior. Estos valores multiplicados por un peso que determina la importancia de conexión entre las dos neuronas. Todas las neuronas conectadas tienen un peso que irán cambiando durante el proceso de aprendizaje. Además, un valor bias puede ser añado al valor calculado. No es un valor que viene de una neurona especifica y se escoge antes de la fase de aprendizaje. Puede ser útil para la red. Con el valor calculado se aplica a una función de activación, para obtener el valor final. Se suele usar para dar un valor entre [0-1].
Proceso de aprendizaje/entrenamiento:
Lo que queremos que haga la red neuronal, es que dado una entrada devuelva una salida. Al principio no va a ser así, solo por suerte devuelve la salida correcta. Por esto se genera la etapa de aprendizaje, en la que cada entrada tiene asociada una etiqueta, para explicar que salida debería de haber adivinado.
-	Acierta: los parámetros actuales se guardan, y se envía la siguiente entrada
-	Falla: los pesos son cambiados. Se suele usar backpropagation

