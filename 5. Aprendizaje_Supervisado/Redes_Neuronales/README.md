# Red Neuronal

## TODO

## BUSQUEDA DE LA MEJOR TASA DE APRENDIZAJE (learning rate)

## CON HILOS MEJOR? MEMORIA COMPARTIDA EN VEZ DE DISTRIBUIDA

### Solucionar MPI1
- pesos?


### MPI0 Fine tunning:
Varios Workers ejecutan la clase RedNeuronal con diferentes parte del entrenamiento
y se juntan en uno al finalizar

[VIDEO](https://www.youtube.com/watch?v=V1-Hm2rNkik&ab_channel=KrishNaik)

La idea básica es tomar las capas de una red pre-entrenada y usarlas como base para una nueva red que se entrenará con los datos combinados. Esto se hace comúnmente en tareas de aprendizaje profundo cuando se tienen conjuntos de datos pequeños y se quiere aprovechar el conocimiento aprendido por una red entrenada en un conjunto de datos más grande.

El procedimiento típico es:

1. Tomar una red pre-entrenada (a menudo entrenada en un conjunto de datos grande como ImageNet o similar).
2. Quitar la última capa (o capas) de la red, que generalmente está relacionada con la clasificación específica del conjunto de datos original.
3. Agregar nuevas capas de salida a la red, adaptadas a la tarea específica que se está abordando.
4. Entrenar la red con el nuevo conjunto de datos, inicializando los pesos con los valores pre-entrenados.
5. Ajustar los pesos de toda la red (no solo las capas adicionales) en el nuevo conjunto de datos, utilizando técnicas de optimización como el descenso de gradiente estocástico.

Aunque no es tan simple como combinar directamente los pesos de dos redes neuronales entrenadas con diferentes conjuntos de datos, la transferencia de aprendizaje permite aprovechar el conocimiento previo de una red pre-entrenada y adaptarlo a una tarea específica con un nuevo conjunto de datos.


### Validacion cruzada?

---

---

---

Basado en la naturaleza, las Redes Neuronales se suelen representar como un cerebro, neuronas interconectadas con otras neuronas,  funcionando como una red. Una trozo de información fluye por muchas neuronas para dar una respuesta, como "mueve tu mano derecha".

El proceso en esta red es directa, una variable de entrada, (por ejemplo una fotografia de una playa) que despues de una serie de calculos, devuelve una salida (para el caso anterior devuelve "playa". Puede ser más especifico y devolver el nombre de la playa si ha sido entrenado para reconocer playas)

---

## Índice

1. [Explicacion General](Explicación-General)
2. [Algoritmo](#algoritmo)
3. [Mejoras (+ MPI)](Mejoras-(+-MPI))
4. [TODO](todo)

---


## Explicación General

Estas neuronas se __representan por columnas__. Estas neuronas están conectadas con las columnas anteriores y posteriores. Y hay diferentes redes que varían las arquitecturas. Se leen de izquierda a derecha. 
- La primera columna es la capa de entrada de la variable. 
- La última columna es la capa de salida con todas las posibles salidas.
- Las columnas intermedias son las capas ocultas.

![Esquema_red](https://github.com/Danipiza/TFG/assets/98972125/a440fcdd-86fc-4ab0-befe-cf02412b614b)

Cada neurona hace una operación simple. Suma los valores de todas las neuronas de la columna anterior. Estos valores multiplicados por un peso que determina la importancia de conexión entre las dos neuronas. Todas las neuronas conectadas tienen un peso que iran cambiando durante el proceso de aprendizaje.
Ademas, un valor bias puede ser añadido al valor calculado. No es un valor que viene de una neurona especifica y se escoge antes de la fase de aprendizaje. Puede ser util para la red.
Con el valor calculado se aplica a una funcion de activación, para obtener el valor final. Se suele usar para dar un valor entre [0-1].

![Perceptron](https://github.com/Danipiza/TFG/assets/98972125/0bdeadf4-cfe5-4994-90db-79c8cb2a694d)

Cuando todas las neuronas de una columna han terminado se pasa a la siguiente columna. Hasta llegar a la última, con valores que deberian de ser utilizables para determinar la salida deseada.

---

## ¿Como aprende la Red Neuronal?
Hay que preparar un montón de datos para entrenar a la red. Estos datos incluyen la entrada y la salida deseada para la red neuronal.

### Proceso de aprendizaje:
Lo que queremos que haga la red neuronal, es que dado una entrada devuelva una salida. Al principio no va a ser así, solo por suerte devuelve la salida correcta. Por esto se genera la etapa de aprendizaje, en la que cada entrada tiene asociada una etiqueta, para explicar que salida deberia de haber adivinado. 
Si acierta, los parametros actuales se guardan, y se envia la siguiente entrada. 
Si no acierta, es decir, la salida no es igual a la etiqueta dada con la entrada, los pesos son cambiados (mencionado anteriormente que estos valores son los unicos que cambian). Este proceso se puede ver como unas combinaciones que van cambiando cuando la salida es erronea.

Para determinar que peso modificar, se usa un proceso llamado "backpropagation", propagación hacia atrás en español. Como el nombre indica consiste en ir hacia atras en la red e inspeccionar cada conexión para comprobar como hubiera sido la salida con un cambio de peso.

Para finalizar este proceso de aprendizaje, tenemos un parametro para controlar como aprende la red neuronal, la tasa de aprendizaje. Determina la velocidad en la cual la red neuronal aprenderá, más bien, como modificar el peso, poco a poco, o mas rapido. Normalmente se usara 0.1 como parametro, es decir, un 10% de aprendizaje.

---

## Algoritmo

### Parámetros
Red Neuronal:
- Tamaño de la capa de Entrada (número de capas=1)
- Tamaño y número de capas Ocultas.
- Tamaño de la capa de Salida (número de capas=1)
- Tasa de aprendizaje (Learning Rate)
 
Entrenamiento:
- Población de entrenamiento (con las etiquetas de salida)
- Número de Repeticiones

Predeccion
- Población de prediccion

### Inicialización
Una vez asignados las variables, se inicializa la red neuronal. 
- **capas:** Array con el numero de nodos de cada capa de la red, empezando desde la capa de entrada y acabando en la de salida. Se inicializa con los parámetros asignados.

```capas=[2,10,10,1] tam. capa entrada=2, capas ocultas=2, tam. capas ocultas=[10,10] y tam. capa salida=1```
- **pesos:** Array tridimensional, con los pesos (float) de cada nodo de la red con todos los nodos de la capa siguiente. Se inicializa con parámetros aleatorios de [0-1] ```pesos[numCapa][nodoCapaAct][nodoCapaSig]```

### Entrenamiento
Fase de entrenamiento. Ejecuta *Numero de Repeticiones* veces la población de entrenamiento, cada individuo recorre la red neuronal y en la capa de salida devuelve el valor predicho, si es acertado no cambia, si no acierta recorre hacia atrás (back-propagation) la red neuronal cambiando los pesos.
```
forward(individuoEntrada):
    salida=[individuoEntrada]
    # Recorre todas las capas (menos la de salida) 
    for i in range(numCapas-1):
        ...
	# Recorre todos los nodos de la capa siguiente
	for j in range(capas[i+1]):
	    ...
	    suma=0
	    # Suma todos los nodos de la capa actual con los pesos
	    for k in range(capas[i]):
		...
	    salidas_capa[j]=sigmoide(suma) # Aplica funcion de activacion
    return salidas[-1] # La ultima salida calculada, es decir, la de la capa de salida

back_propagation(salida, etiqueta):
    # Calcula el error
    error=(salida-etiqueta)*sigmoide_derivado() # Función de activacion derivada para el entrenamiento
    if error==0: return #Iguales
    # Recorre hacia atras las capas, la capa de salida no la cambia por que no tiene pesos.
    for i in range(numCapas - 2, -1, -1):
    	...
	# Recorre todos los nodos de la capa actual
	for j in range(capas[i]):
	    suma=0
            # Suma todos los nodos de la capa siguiente (sin orden inverso, es decir, la derecha)
            for k in range(capas[i+1]):
		...
	    # Actualiza los nodos
            for k in range(capas[i+1]):
		pesos[i][j][k]+=tasaAprendizaje*errores[k]*self.salidas[i][j] # errores se va actualizando con el recorrido

```
### Predicción

Aplica la función **forward()** para cada individuo de la población de predicción, una vez entrenada la red devuelve la salida *correcta*.

### Complejidad
- Complejidad Temporal: **O((M\*rep)\*2N^3)** *M* es el tamaño de la poblacion de entrenamiento que se ejecuta *rep* veces, y en el peor caso, todos los individuos de la población pasan por foward y backpropagation con coste cúbico.
- Complejidad Espacial: **O(N^3)** porque los pesos se almacenan en un array tridimensional.

--- 

## Mejoras (+ MPI)

### Dividir la población de entrenamiento entre varios workers (No se puede ???)
No funciona ya que la red se tiene que estar actualizando conforme se pasa el entrenamiento, si se divide el entrenamiento, cada proceso se especializa en la parte que le toca pero no en las demas.
- Se puede hacer de manera que al predecir un individuo el master se encarga de mandar al worker mejor cualificado, o enviar a todos y predecir como el mejor.
- transferencia de aprendizaje" o "fine-tuning". [info](https://www.youtube.com/watch?v=V1-Hm2rNkik&ab_channel=KrishNaik)

#### Complejidad
- Complejidad Temporal: **O((M\*rep)\*2N^3)** *M* es el tamaño de la poblacion de entrenamiento que se ejecuta *rep* veces, y en el peor caso, todos los individuos de la población pasan por foward y backpropagation con coste cúbico.
- Complejidad Espacial: **O(N^3)** porque los pesos se almacenan en un array tridimensional.

### Dividir por capas los workers
El Master se encarga de la capa de entrada y el último Worker de la capa de salida. Las capas ocultas son gestionadas por los demas Workers disponibles. Así cada proceso se encarga de 1 o más capas y no toda la red.

- forward(): El Master envía entradas al worker con myrank (id del master)+1, este worker al siguiente con myrank+1 y así hasta llegar al último que gestiona la última capa, por lo que siempre se esta avanzando.
- back_propagation(): El mismo proceso pero al revés. El ultimo worker envia errores al worker anterior, y este a su anterior, asi hasta llegar al master. Cuando envia el error, el proceso que lo recibe actualiza sus pesos y envía el nuevo array de errores al siguiente proceso.

![RedesNeuronalesMPI](https://github.com/Danipiza/TFG/assets/98972125/085f5b1e-ab33-47f8-85f3-b5450aa1663b)

#### Complejidad
- Complejidad Temporal: **O((M\*rep)\*2N^2)?** 
- Complejidad Espacial: O(N^3+numWorker) = **O(N^3)** ocupa el mismo espacio pero cada worker gestiona una capa por lo que cada worker tiene sus pesos que vinculan con las siguientes capas, se añade numWorker porque cada uno necesita un espacio constante para almacenar el tamaño de la capa que hace borde para poder calcular los pesos y errores.


---

[INFO](https://towardsdatascience.com/first-neural-network-for-beginners-explained-with-code-4cfd37e06eaf)




