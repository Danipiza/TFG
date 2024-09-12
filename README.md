<hr>

<h1 align="center">
    Optimización de algoritmos de IA aplicando técnicas enfocadas al cómputo de alto rendimiento 
</h1>
<h2 align="center">
    Optimization of AI algorithms by applying high-performance computing techniques
</h2>

<br>

<div align="center">
  <img src="https://github.com/user-attachments/assets/ffad1fd9-b830-4bdf-936b-dc2295f9bfe0" alt="escudo_ucm" width="200">
</div>

<h3 align="center">
TRABAJO DE FIN DE GRADO
<br>
</h3>
<h3 align="center">
DANIEL PIZARRO GALLEGO
</h3>
<h4 align="center">
Director:
Alberto Núñez Covarrubias
</h4>
<br>
<h4 align="center">
Facultad de Informática
	
Universidad Complutense de Madrid
	
13 de septiembre del 2024
</h4>

<hr>

## Índice
1. [MPI](#mpi)
2. [Aprendizaje no Supervisado](#aprendizaje-no-supervisado)
3. [Aprendizaje por Refuerzo](#aprendizaje-por-refuerzo)
4. [Programación Evolutiva](#programación-evolutiva)
5. [Aprendizaje Supervisados](#aprendizaje-supervisado)


<h3> <img src="https://skillicons.dev/icons?i=python" alt="C Language Icon" width="20" height="20" /> Python </h3>

Es uno de los lenguajes más populares para la IA debido a su sintaxis sencilla, amplia variedad de bibliotecas de IA (como TensorFlow, PyTorch, scikit-learn, etc.) y una gran comunidad de desarrolladores. Pero es un lenguaje bastante lento, lo que provoca que a la hora de ejecutar el código demore bastante tiempo en finalizar.

Voy a estar programando en python, y probando maneras de reducir el tiempo de ejecución.


<hr>


## MPI
Es un estándar para una biblioteca de paso de mensajes, cuyo objetivo es facilitar la programación paralela en entornos distribuidos, permitiendo que múltiples procesos independientes se comuniquen para resolver tareas de manera eficiente.

Actualmente hay varias implementaciones: [Open MPI](http://www.open-mpi.org/), [MPICH](http://www.mpich.org/) , [MVAPICH](http://mvapich.cse.ohio-state.edu/), [IBM Platform MPI](http://www.ibm.com/systems/es/platformcomputing/products/mpi/), [Intel MPI](https://www.intel.com/content/www/us/en/developer/tools/oneapi/mpi-library.html). En este proyecto se usa [mpi4py](https://mpi4py.readthedocs.io/en/stable/).

### Single Program Multiple Data (SPMD) 
**1 programa** ejecutado en paralelo. El mismo programa se **copia a todos los nodos**. Cada proceso tiene su propio su ID (Rank) 

La principal diferencia entre la **memoria compartida** y **distribuida** radica en cómo se organizan y gestionan los recursos de memoria en sistemas de cómputo paralelos. La memoria compartida tiene una sola memoria que comparte entre todos los procesos, teniendo que ejecutar técnicas para garantizar la sincronización. En su contraparte, la memoria distribuida utiliza memorias independientes entre cada proceso, por lo que estos problemas no ocurren. Sin embargo, la comunicación entre procesos resulta ser más costosa en los sistemas distribuidos.


<div align="center">
   <img  src="https://github.com/Danipiza/TFG/blob/main/.Otros/Imagenes/MPI.png" width="600" height="300"/> 
</div>

<br>

Esquema básico para ejecutar un programa MPI en Python:
```python
 from mpi4py import MPI # Al importar la biblioteca en Python se genera el entorno.

 comm = MPI.COMM_WORLD     	# Comunicador
 status = MPI.Status()   	# Status
 myrank = comm.Get_rank() 	# id de cada proceso
 numProc = comm.Get_size() 	# Numero de procesadores

 if myrank==0:           	# Master
    # Carga el conjunto de datos. Los divide y envia.
    # Recibe todos los datos procesados.
 else:                   	# Workers
    # Recibe el subconjunto de datos que le asigna el Master.
    # Procesa los datos. Los envia.
```


### Carpeta con explicaciones y el código [AQUÍ](https://github.com/Danipiza/TFG/tree/main/0_MPI).
<hr>

## Aprendizaje no Supervisado

Los métodos no supervisados (unsupervised methods, en inglés) son algoritmos de aprendizaje automático que basan su proceso en un entrenamiento con datos sin etiquetar. Es decir, a priori, no se conoce ningún valor objetivo, ya sea categórico o numérico. La meta de este aprendizaje es encontrar patrones o estructuras en los datos proporcionados. Estos algoritmos son útiles en escenarios en los cuales hay escasez de datos etiquetados o éstos no están disponibles.

En este proyecto vamos a reducir el tiempo de ejecución de las técnicas de _clustering_ que se encargan de agrupar individuos basándose en alguna medida de similitud. Los algoritmos son los siguientes:

1. [Aglomerativo](#jerárquico-aglomerativo)
2. [KMedias](#algoritmo-kmedias)

### Jerárquico Aglomerativo
```python
FASE 1: Crear la matriz de distancias inicial D. Es una matriz simétrica (basta con usar una de las matrices triangulares) 
FASE 2: Agrupación de Individuos 
    o 2.1. Partición inicial P0: Cada objeto es un cluster 
    o 2.2. Calcular la partición siguiente usando la matriz de distancias D
         Elegir los dos clusters más cercanos. Serán la fila y la columna del mínimo de la matriz D 
         Agrupar los dos en un cluster. Eliminar de la matriz la fila y columna de los clusters agrupados.
	  Generar la nueva matriz de distancias D. 
	    • Añadir una fila y una columna con el cluster nuevo 
            • Calcular la distancia del resto de clusters al cluster nuevo 

	 Repetir este el paso 2.2. hasta tener sólo un cluster con todos los individuos
FASE 3 (OPCIONAL): Representar el dendograma.

La complejidad con los enlaces simple y completo tienen un coste cúbico O(N^3). Existen implementaciones más eficientes (N^2).
```
## Algoritmos secuenciales
- [Algoritmo](https://github.com/Danipiza/TFG/blob/main/1_Aprendizaje_NoSupervisado/Jerarquico_Aglomerativo/Aglomerative.py)

## Estrategias MPI implementadas
### Dividir la matriz entre los procesos
Divide la matriz entre todos los procesos. El proceso _master_ se encarga de gestionar la comunicación entre los procesos para dividr el algoritmo entre estos. Dependiendo de la distancia hay más o menos implementaciones.

Distancia por centroides:
- [Implementación](https://github.com/Danipiza/TFG/blob/main/1_Aprendizaje_NoSupervisado/Jerarquico_Aglomerativo/Aglomerative_MPI_Cent_E.py)

Distancias por enlace simple/completo, (complejidad mayor que la anterior distancia):
- El proceso que actualiza la fila trabaja solo.
	- [Implementación 1](https://github.com/Danipiza/TFG/blob/main/1_Aprendizaje_NoSupervisado/Jerarquico_Aglomerativo/Aglomerative_MPI_Simple_E_1.py)
- El proceso que actualiza la fila trabaja con todos los procesos _workers_.
	- [Implementación 2_0](https://github.com/Danipiza/TFG/blob/main/1_Aprendizaje_NoSupervisado/Jerarquico_Aglomerativo/Aglomerative_MPI_Simple_E_2_0.py)
 	- [Implementación 2_1](https://github.com/Danipiza/TFG/blob/main/1_Aprendizaje_NoSupervisado/Jerarquico_Aglomerativo/Aglomerative_MPI_Simple_E_2_1.py)
  	- [Implementación 2_2](https://github.com/Danipiza/TFG/blob/main/1_Aprendizaje_NoSupervisado/Jerarquico_Aglomerativo/Aglomerative_MPI_Simple_E_2_2.py)


### Carpeta con explicaciones y el código [AQUÍ](https://github.com/Danipiza/TFG/tree/main/1_Aprendizaje_NoSupervisado/Jerarquico_Aglomerativo).

<br>
 
### Algoritmo KMedias

```python
Fijar un valor k.

FASE 1: Inicializar los K centros de los clusters de forma aleatoria.
    • Generando puntos aleatorios en el espacio dimensional
    • Seleccionando aleatoriamente individuos
FASE 2: Repetir esta fase hasta que los centros no cambien.
    o 2.1. (Asignación): Calcular el cluster más cercano para cada individuo.
	Requiere el uso de una distancia (normalmente Euclídea o Manhattan).
    o 2.2. (Actualización): Calcular los nuevos centros con la asignación (de esta iteración) de los individuos.
	Se calcula con la media de los valores de los individuos de cada cluster.

Como los clusters se generan aleatoriamente, no siempre va a dar un buen resultado a la primera.
Por lo que conviene ejecutar varias veces este algoritmo para encontrar la mejor asignación.
```
## Algoritmos secuenciales
- [Algoritmo y búsqueda](https://github.com/Danipiza/TFG/blob/main/1_Aprendizaje_NoSupervisado/K-Medias/KMedias.py)

## Estrategias MPI implementadas
### Dividir la población
Divide la población de individuos matriz entre todos los procesos. El proceso _master_ se encarga de gestionar de calcular los nuevos centros en cada iteración.

Distancia Euclidea:
- [Implementación](https://github.com/Danipiza/TFG/blob/main/1_Aprendizaje_NoSupervisado/K-Medias/KMediasMPI_uno_E.py)

Distancia Manhattan:
- [Implementación](https://github.com/Danipiza/TFG/blob/main/1_Aprendizaje_NoSupervisado/K-Medias/KMediasMPI_uno_M.py)

### Búsqueda de la mejor asignación
Para la búsqueda se ejecuta un bucle principal con el número de centros maximo que se quiere estudiar, es decir, se ejecuta el algoritmo para los valores de _K_ entre _\[2, K_max\]_. En este bucle principal se repite 5 veces para encontar la mejor asignación para cada valor de _K_. Hay dos implementaciones, la estrategia MPI comentada en la subsección anterior, o ejecutar en varios procesos el algoritmo secuencial con diferentes valores de _K_, pero mismos centros.
- [Dividir la población](https://github.com/Danipiza/TFG/blob/main/1_Aprendizaje_NoSupervisado/K-Medias/KMediasMPI_busqueda_E_1.py)
- [Ejecuciones secuenciales en paralelo](https://github.com/Danipiza/TFG/blob/main/1_Aprendizaje_NoSupervisado/K-Medias/KMediasMPI_busqueda_E_2.py)

### Carpeta con explicaciones y el código [AQUÍ](https://github.com/Danipiza/TFG/tree/main/1_Aprendizaje_NoSupervisado/K-Medias).

<hr>

## Aprendizaje por Refuerzo
Se basa en experiencias y simulaciones, con prueba y error, recibiendo recompensas con las acciones tomadas (también pueden ser negativas). Nadie le dice al agente que hacer, este toma las decisiones con diferentes estrategias. Se realiza una etapa de entrenamiento para que aprenda a moverse por el entorno, tomando las decisiones que maximicen las recompensas obtenidas en experiencias pasadas.

Los algoritmos desarrollados en este proyecto son los siguientes:
1. [Q-Learning](#q-learning)
2. [DQN](#dqn)

### Q-Learning
Mezcla entre programación dinámica y Monte Carlo. R=Matriz de recompensas.
- R=Matriz de recompensas.
- Q=Matriz (Estados x Acciones). Que acción elegir en cada estado. (mayor valor)

### Entorno 
Para este algoritmo es un laberinto. Se entrena al agente para que consiga llegar desde un punto origen a uno destino en el menor número de acciones necesarias.

### Hiperparametros:
- α (tasa de aprendizaje): 
Debería disminuir a medida que continúa adquiriendo una base de conocimientos cada vez mayor.
- γ (factor de descuento): 
A medida que se acerca cada vez más al valor límite, su preferencia por la recompensa a corto plazo debería aumentar, ya que no estará el tiempo suficiente para obtener la recompensa a largo plazo, lo que significa que su gamma debería disminuir.
- ϵ (factor de exploración-explotación): Evita que la acción siga siempre la misma ruta.
A medida que desarrollamos nuestra estrategia, tenemos menos necesidad de exploración y más explotación para obtener más utilidad de nuestra política, por lo que en vez de utilizar un valor fijo, a medida que aumentan los ensayos, épsilon debería disminuir. Al principio un épsilon alto genera más episodios de exploración y al final un épsilon bajo explota el conocimiento aprendido.

La función que usa para almacenar las experiencias en la Q-Table es la siguiente:

```Q(S, A) = (1−α)*Q(S, A) + α*(R(S, A) + γ*maxi Q(S’, Ai))```

Siendo _S_ el estado actual, _A_ la acción tomada, _S’_ el estado siguiente y _Ai_ una acción de entre todas las acciones del agente.

## Algoritmos secuenciales
- [Algoritmo](https://github.com/Danipiza/TFG/blob/main/2_Aprendizaje_Por_Refuerzo/RL/RL_1.py)
- [Algoritmo con preprocesado](https://github.com/Danipiza/TFG/blob/main/2_Aprendizaje_Por_Refuerzo/RL/RL_2.py)

## Estrategias MPI implementadas

### Dividir el entorno entre los procesos
Al dividir el laberinto entre los procesos (primera mejora), cada proceso controla una zona, y se genera un flujo constante de episodios (iteraciones del algoritmo). Cuando un agente sale del dominio de un proceso, éste le manda un mensaje al proceso que controla esa parte del laberinto con la posición en la que entra
- [Implementación](https://github.com/Danipiza/TFG/blob/main/2_Aprendizaje_Por_Refuerzo/RL/RL_MPI_3.py)

### Ejecuciones en paralelo y juntar las experiencias.
El master recolecta las experiencias de los workers, haciendo la media de los Q-valor obtenidos de los procesos, calculando así las mejores acciones para cada estado.
- [Implementación 1](https://github.com/Danipiza/TFG/blob/main/2_Aprendizaje_Por_Refuerzo/RL/RL_MPI_2_1.py)
- [Implementación 2](https://github.com/Danipiza/TFG/blob/main/2_Aprendizaje_Por_Refuerzo/RL/RL_MPI_2_2.py)


### Búsqueda de hiper-parámetros
Igual que la mejora anterior, pero esta vez para encontrar hiper-parámetros. Cada proceso ejecuta combinaciones distintas y almacena en ficheros los resultados obtenidos (Fin, Bucle, ...)
- [Implementación](https://github.com/Danipiza/TFG/blob/main/2_Aprendizaje_Por_Refuerzo/RL/RL_MPI_1.py)

### Carpeta con explicaciones y el código [AQUÍ](https://github.com/Danipiza/TFG/tree/main/2_Aprendizaje_Por_Refuerzo/RL).
<br>

### DQN
Este algoritmo combina redes neuronales con la base de aprendizaje por refuerzo, eliminando así la Q-Table.

La estructura de la red neuronal depende del entorno del problema. Los valores de la capa oculta se pueden modificar dependiendo de las necesidades del programador, pero la capa de entrada y salida depende del problema. La entrada se adapta para recibir un estado del entorno, como por ejemplo una imagen representada como una matriz. La salida de la red tendrá tantos nodos como acciones tenga el agente. 

### Entorno
El juego Pacman, diseñado por la empresa _Namco_, y en particular la versión de _Atari 2600_. El juego consiste en recolectar todas las monedas del laberinto sin ser comido por un fantasma. Implementamos el juego -desde cero- para moldear según nuestros intereses la implementación y que el algoritmo DQN sea más eficiente y sencillo.

<div align="center">
  <img src="https://github.com/user-attachments/assets/ff437eec-2092-4d0c-9aad-0e1f43159c55" alt="pacman" width="400">
</div>

### Hiperparametros:
- Gamma (factor de descuento \[0, 1\]). Utilizado para saber cuánto resta a la recompensa adquirida al realizar una acción en un estado.
- Epsilon (tasa de exploración \[0, 1\]). Probabilidad utilizada para ejecutar una acción aleatoria o la mejor hasta el momento. 
- Learning rate (tasa de aprendizaje \[0, 1\]). Para la propagación hacia atrás de las redes neuronales. Esencialmente, mide cuánto cambian los pesos de los nodos al tener un fallo.

Además de estos parámetros, el algoritmo cuenta con otras variables para desarrollar las redes neuronales.
- Epsilon decay. Utilizado para no usar siempre el mismo valor de epsilon. Esta variable marca cuanto se reduce la variable epsilon entre episodios.
- Número de ejemplos de entrenamiento (batch size}. Se utiliza para actualizar los parámetros de la red neuronal durante una sola iteración del entrenamiento.
- Tamaño de la capa oculta. Marca el número de neuronas en cada capa.

## Algoritmos secuenciales
- [Algoritmo y Pacman](https://github.com/Danipiza/TFG/blob/main/2_Aprendizaje_Por_Refuerzo/DQN/DQN.py)


## Estrategias MPI implementadas

### Búsqueda de hiper-parámetros
Igual que la mejora anterior, pero esta vez para encontrar hiper-parámetros. Cada proceso ejecuta combinaciones distintas y almacena en ficheros los resultados obtenidos (Fin, Bucle, ...)
- [Implementación](https://github.com/Danipiza/TFG/blob/main/2_Aprendizaje_Por_Refuerzo/DQN/DQN_mpi.py)

### Mismas estrategias que en las [Redes Neuronales](#redes-neuronales)

### Carpeta con explicaciones y el código [AQUÍ](https://github.com/Danipiza/TFG/tree/main/2_Aprendizaje_Por_Refuerzo/DQN).
<hr>

## Programación Evolutiva

La programación evolutiva es una técnica de optimización inspirada en la teoría de la evolución biológica. Se basa en el concepto de selección natural y evolución de las poblaciones para encontrar soluciones a problemas complejos.

Una población está compuesta por individuos, que son sometida a métodos de evaluación, selección, cruce y mutación para, con el paso de las generaciones, maximizar o minimizar un valor fitness. Un individuo tiene un cromosoma, que tiene uno o varios genes, que a su vez cada gen tiene uno o varios alelos. Los individuos se pueden representar de la siguientes formas: 
- Binarios: Cada alelo es un bit. 
- Reales: Cada alelo es un número real. Estos individuos son más fáciles de manejar.
- Árboles: Cada alelo es un nodo del árbol.


### Plantilla básica de una Algoritmo Evolutivo
```python
poblacion = iniciar_poblacion(tam_poblacion)
evaluar_poblacion(poblacion)
while(<<condicion>>):
  seleccion = seleccionar_poblacion()
  # Reproducción
  cruzar_poblacion(seleccion, prob_cruce)
  mutar_poblacion(seleccion, prob_muta)  
  evaluar_poblacion()
```
## Algoritmos secuenciales
- [Terminal](https://github.com/Danipiza/TFG/blob/main/3_Programacion_Evolutiva/0_terminal/main.py)
- [GUI](https://github.com/Danipiza/TFG/blob/main/3_Programacion_Evolutiva/1_gui/main.py)

## Estrategias MPI implementadas

### Dividir la población
La población se divide entre los procesos generados. El _master_ se encarga de gestionar las comunicaciones para que la población evolucione.
- [Implementación](https://github.com/Danipiza/TFG/tree/main/3_Programacion_Evolutiva/2_MPI/1DividirPob.py)

### Modelo de islas
La población se divide en subpoblaciones repartidas entre los procesos ejecutados, para, en paralelo, evolucionar a la población general. Los procesos se comunican cada cierto tiempo para reiniciar las poblaciones con los mejores individuos de todos los procesos.
- [Implementación](https://github.com/Danipiza/TFG/tree/main/3_Programacion_Evolutiva/2_MPI/2ModeloIslas_1.py)

### Pipeline
Cada parte del algoritmo se divide entre los procesos. El _master_ genera subpoblaciones, y los workers ejecutados se encargan de evaluar, seleccionar, cruzar y mutar las poblaciones que reciben del proceso anterior. Una vez procesan los datos recibidos, los envían hacia adelante y esperan a recibir nuevos datos. Cada proceso se encarga de una parte, generando un flujo constante de mensajes entre los procesos.
- [General](https://github.com/Danipiza/TFG/blob/main/3_Programacion_Evolutiva/2_MPI/3PipeLine.py)
- [Binario \(4 procesos\)](https://github.com/Danipiza/TFG/blob/main/3_Programacion_Evolutiva/2_MPI/3PipeLineBin_1.py)
- [Binario \(7 procesos\)](https://github.com/Danipiza/TFG/blob/main/3_Programacion_Evolutiva/2_MPI/3PipeLineBin_2.py)
- [Real \(5 procesos\)](https://github.com/Danipiza/TFG/blob/main/3_Programacion_Evolutiva/2_MPI/3PipeLineReal_2.py)
- [Real \(10 procesos\)](https://github.com/Danipiza/TFG/blob/main/3_Programacion_Evolutiva/2_MPI/3PipeLineReal_3.py)


### Carpeta con explicaciones y el código [AQUÍ](https://github.com/Danipiza/TFG/tree/main/3_Programacion_Evolutiva).
<hr>


## Aprendizaje Supervisado
1. [KNN](#knn)
2. [Redes Neuronales](redes-neuronales)

### KNN
simple pero potente, resultando muy efectivo para tareas de clasificación y regresión. Se basa en la idea de que los puntos de datos similares tienden a agruparse en el espacio de características. Este algoritmo pertenece al paradigma de aprendizaje perezoso o basado en instancias.

```python
FASE 1: Inicializar las poblaciones categorizadas y a predecir, y la variable K
FASE 2: Agrupar un nuevo individuo
    o 2.1. Recorrer todos los individuos de la población categorizada, y almacenar las K individuos más cercanos.
    o 2.2. Asignar el cluster con más repeticiones al individuo actual.
    o 2.3. (opcional) Añadir el individuo actual a la población categorizada.

No hay una forma de determinar el mejor valor para k, por lo que hay que probar con varias ejecuciones. 
Valores pequeños de K crea sonido. 
Valores grandes con pocos datos hará que siempre sea la misma categoría     
```
## Algoritmos secuenciales
- [Algoritmo](https://github.com/Danipiza/TFG/blob/main/4_Aprendizaje_Supervisado/KNN/KNN.py)

## Estrategias MPI implementadas
Las estrategias se dividen en dos principales implementaciones, actualizando la población categorizada conforme se categorizan nuevos individuos, o no actualizando. Si se actualiza se obtienen mejores resultados en cuanto a predicciones se refiere, pero el tiempo de ejecución es mucho mayor.

### Dividir la población categorizada
Se divide la población categorizada entre los procesos para que estos trabajen de manera paralela en un mismo individuo. Es decir, cada _worker_ envía los _K_ vecinos más cercanos de su subpoblación categorizada.
No Actualiza:
- [Euclídea](https://github.com/Danipiza/TFG/blob/main/4_Aprendizaje_Supervisado/KNN/KNN_MPI_1_E_NoAct.py)
- [Manhattan](https://github.com/Danipiza/TFG/blob/main/4_Aprendizaje_Supervisado/KNN/KNN_MPI_1_M_NoAct.py)

Actualiza:
- [Euclídea](https://github.com/Danipiza/TFG/blob/main/4_Aprendizaje_Supervisado/KNN/KNN_MPI_1_E_Act.py)
- [Manhattan](https://github.com/Danipiza/TFG/blob/main/4_Aprendizaje_Supervisado/KNN/KNN_MPI_1_M_Act.py)


### Dividir la población a predecir
Se divide la población a predecir entre los procesos para que estos trabajen en paralelo de manera independiente. Es decir, cada _worker_ envía al proceso _master_ un individuo distinto al terminar un procesado.
No Actualiza:
- [Euclídea](https://github.com/Danipiza/TFG/blob/main/4_Aprendizaje_Supervisado/KNN/KNN_MPI_2_E_NoAct.py)
- [Manhattan](https://github.com/Danipiza/TFG/blob/main/4_Aprendizaje_Supervisado/KNN/KNN_MPI_2_M_NoAct.py)

Actualiza:
- [Euclídea](https://github.com/Danipiza/TFG/blob/main/4_Aprendizaje_Supervisado/KNN/KNN_MPI_1_2_Act.py)
- [Manhattan](https://github.com/Danipiza/TFG/blob/main/4_Aprendizaje_Supervisado/KNN/KNN_MPI_1_2_Act.py)



### Carpeta con explicaciones y el código [AQUÍ](https://github.com/Danipiza/TFG/tree/main/4_Aprendizaje_Supervisado/KNN).
<br>





### Redes Neuronales

Las redes neuronales son un modelo computacional inspirado en el funcionamiento y estructura de las neuronas del cerebro humano. Esencialmente, consisten en capas de nodos interconectados, llamadas neuronas artificiales. La red neuronal se compone de las siguientes capas:
- Capa de entrada, en la cual, habrá tantas neuronas como variables de entrada tenga el modelo de predicción.
- Capa oculta, representada con una o más capas internas. Cada una contiene un número determinado de neuronas.
- Capa de salida. Como en la entrada, tendrá un número de neuronas relacionadas con las variables de salida.

<div align="center">
  <img src="https://github.com/Danipiza/TFG/assets/98972125/cf25aa2b-00e0-45e7-877f-d97f891f1ec4" alt="escudo_ucm">
</div>




Cada neurona hace una operación simple. Suma los valores de todas las neuronas de la columna anterior. Estos valores multiplicados por un peso que determina la importancia de conexión entre las dos neuronas. Todas las neuronas conectadas tienen un peso que irán cambiando durante el proceso de aprendizaje. Además, un valor bias puede ser añado al valor calculado. Con el valor calculado se aplica a una función de activación, para obtener el valor final. 

Proceso de aprendizaje/entrenamiento:
```python
FASE 1: Inicializar los pesos de la red neuronal con los datos de inicializacion
FASE 2: Entrenamiento
    o 2.1. (Forward) Enviar un individuo por la red neuronal. Suma el valor recibido de la capa anterior multiplicada
	por los pesos de la capa actual con la siguiente. Así se determina la importancia de conexión entre las neuronas.
	Con el valor calculado se aplica a una función de activación y se pasa a la siguiente capa hasta llegar a la salida.
    o 2.2. (Backpropagation) Enviar el error cometido hacia atrás. El valor predicho calculado en la salida es comparado con
	la etiqueta, y se calcula el error. Este error se manda para atrás actualizando los pesos. Se suma la multiplicación
	del valor predicho en cada capa con la tasa de aprendizaje y el error.
```

## Algoritmos secuenciales
- [Algoritmo](https://github.com/Danipiza/TFG/blob/main/4_Aprendizaje_Supervisado/Redes_Neuronales/RN_1_2.py)
- [Búsqueda de hiper-parámetros](https://github.com/Danipiza/TFG/blob/main/4_Aprendizaje_Supervisado/Redes_Neuronales/RN_2_1.py)

## Estrategias MPI implementadas

### Pipeline
Al igual que en los algoritmos evolutivos cada proceso se encarga de una parte para generar un flujo constante de mensajes. En este caso cada worker se encarga de una capa.
- [Síncrono](https://github.com/Danipiza/TFG/blob/main/4_Aprendizaje_Supervisado/Redes_Neuronales/RN_MPI_1_3.py)
- [Asíncrono](https://github.com/Danipiza/TFG/blob/main/4_Aprendizaje_Supervisado/Redes_Neuronales/RN_MPI_1_4.py)

### Dividir el entrenamiento
Se divide la población de entrenamiento entre los procesos. Al final se juntan las experiencias haciendo la media. (No funciona correctamente, da malas predicciones)
- [Implementación](https://github.com/Danipiza/TFG/blob/main/4_Aprendizaje_Supervisado/Redes_Neuronales/RN_MPI_3_1.py)

### Búsqueda de hiper-parámetros
Al igual que en otros algoritmos, se ejecutan en paralelo ejecuciones secuenciales, en donde cada proceso almacena los resultados.
- [Implementación](https://github.com/Danipiza/TFG/blob/main/4_Aprendizaje_Supervisado/Redes_Neuronales/RN_MPI_2_1.py)

### Carpeta con explicaciones y el código [AQUÍ](https://github.com/Danipiza/TFG/edit/main/README.md).
<hr>
