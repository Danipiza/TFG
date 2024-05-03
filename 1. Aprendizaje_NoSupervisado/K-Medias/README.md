# K-Medias

El objetivo es dividir los N o individuos en un número de clusters *k* (valor de entrada del algoritmo). Lo que hace este algoritmo es dividir nuestro espacio de representación d-dimensional en k regiones, siendo *d* las variables consideradas.

## Índice


1. [Algoritmo](#algoritmo)
2. [Mejoras (+ MPI)](Mejoras-(+-MPI))
3. [TODO](todo)

## Algoritmo

Inicializar los k centros (o centroides) de los clusters de forma aleatoria. 
- Generando puntos aleatorios en el espacio dimensional
- Seleccionando aleatoriamente individuos 

Repite el siguiente proceso hasta que los centros no cambien. 
1. Fase de asignación: Para cada individuo se le asigna el cluster más cercano. Requiere el uso de una distancia (normalmente Euclídea, también se puede usar Manhattan o Chebychev) 
2. Actualiza el centro de los clusters. Se calcula con la media de los individuos del

![KMedias1](https://github.com/Danipiza/TFG/assets/98972125/be767a2f-d925-4727-a94e-c7b841b8e2e3)



Como los clusters se generan aleatoriamente, no siempre va a dar un buen resultado a la primera. Por lo que se pasa por parámetro cuantas veces se repite hasta encontrar el mejor.

![kmediasCluster](https://github.com/Danipiza/TFG/assets/98972125/c9bc36f6-d27c-4a1c-a7c9-2bbe0bbfd13a)


### Encontrar el valor ideal para k puede tardar bastante.
Hay que hacer una búsqueda exhaustiva para encontrar el mejor valor para k.

![kmediasvariacion](https://github.com/Danipiza/TFG/assets/98972125/4a545b9b-b533-45e8-9be0-bae6007a7930)

Se puede comprobar el mejor valor para k, con un diagrama de codo, coeficiente de Daivies-Bouldin o Silhouette (este último es bastante lento de calcular).

![Calcular_Mejor_K](https://github.com/Danipiza/TFG/assets/98972125/00ffc48f-8498-4e10-8567-d5d9cdf81541)


Puede haber varias dimensiones por lo que el cálculo de la distancia se complica. distancia euclídea = raizcuadrada(x0^2 + x1^2 + ... + xn^2)



### Complejidad
- Complejidad Temporal: **O((K\*(N\*d))\*iter)** Para cada individuo de la población, *N*, se calcula la distancia mínima con cada cluster. Esto se repite por *iter* iteraciones.
- Complejidad Espacial: O(N\*d+K\*d) = **O(N\*d)** K es el número de clusters, por lo que necesitamos un array con K puntos en el espacio. La N es la población de individuos con las *d* dimensiones.


---



## Mejoras (+ MPI)

Búsqueda del k óptimo para una población.
### Parámetros de entrada:
- **maxClusters:** numero máximo de k que se va a probar.
- **times:** numero de veces que se repite el algoritmo para un k.
- **d:** dimensiones de cada individuo (cuanto mayor sea mayor más tardará)
- **población:** array con los individuos (*d* dimensiones)

Empieza con k=1 clusters y se repite el siguiente proceso hasta llegar a maxClusters:

```El algoritmo K-Medias se repite *times* veces, inicializando los centroides con individuos aleatorios de la población.```

Cuando finaliza una ejecución del algoritmo se evalúa para almacenar la mejor asignación, junto con sus centroides. Para así poder generar el diagrama de Codo y Davies Boulding y poder ver la k óptima.


### Divide la población entre los Workers 

#### inicialización
El Master envía a los Workers la parte de la población correspondiente. (Así como *maxClusters* y *times*)

#### Algoritmo (1 iteración para *times*)
- El Master genera los cluster aleatorios y se los envía a los workers.

Iterar hasta que no cambien los centroides
- Los workers ejecutan el algoritmo de KMedias para su parte de población.
- El Master recibe, de cada Worker, la suma total de sus individuos categorizados y el numero de individuos por cluster, para poder hacer la media y calcular los nuevos centroides. Si no cambian se acaba. Si cambian, el Master envía los nuevos clusters a los Workers.
- Cuando el Master finaliza, recibe las asignaciones de los Workers, los reagrupa y se encarga de evaluar la asignación y compara con la mejor evaluación para actualizar si es mejor.



#### Complejidad
- Complejidad Temporal Algoritmo: **O((K\*((N/numWorkers)\*d))\*iter)** Se divide la población entre los Workers.
- Complejidad Temporal Búsqueda: **O((((K\*((N/numWorkers)\*d))\*iter)\*times)\*maxClusters)** 
- Complejidad Espacial: **O(N\*d)** es la misma que sin mejora.


### Cada Worker hace una iteración

#### Inicialización
El Master envía a los Workers toda la población. (Así como *maxClusters* y *times*). Cada Worker ejecuta una interacción del algoritmo. Cuando termina un Worker, enviar la evaluación al Master y si es mejor que la actual le pide a ese Worker que envíe su asignación y centroides para encontrar la mejor *k*.


#### Complejidad 
- Complejidad Temporal Algoritmo: **O((K\*(N\*d))\*iter)** El algoritmo no mejora.
- Complejidad Temporal Búsqueda: **O(((((K\*(N\*d))\*iter)\*times)/numWorkers)\*maxClusters)** Al haber numWorkers ejecutando el algoritmo se reduce *times* y es más rápido.
- Complejidad Espacial: **O((N\*d)\*numWorkers)** Todos los Workers tienen la población entera.


---


## TODO



### validación cruzada?


### SPEEDUP

# COMPROBAR TODO